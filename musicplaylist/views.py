from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from musicplaylist.models import Music, PlayList
from musicplaylist.serializers import MusicSerializer, PlayListCustomSerializer, PlayListRecommendedSerializer, PlayListRecommendCreateSerializer, PlayListCreateSerializer
from drf_yasg.utils import swagger_auto_schema
import pandas as pd
from musicplaylist.models import Music
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# 테스트용 전체 음악 DB 보기 API
class MusicListview(APIView):
    def get(self, request, format=None):
        dbtest_musics = Music.objects.all().values()
        print(dbtest_musics)

        dbtest_musics_pandas = pd.DataFrame(dbtest_musics)
        print(dbtest_musics_pandas)

        # df.columns = ['id', 'music_title','music_artist','music_genre']
        # print(df.columns)

        counter_vector = CountVectorizer(ngram_range=(1,2), encoding = u'utf-8')
        c_vector_genres = counter_vector.fit_transform(dbtest_musics_pandas['music_genre'])
        c_vector_genres.shape
        counter_vector.vocabulary_

        print(c_vector_genres)

        similarity_genre = cosine_similarity(c_vector_genres, c_vector_genres)
        print(similarity_genre)

        similarity_genre.shape

        def recommend_music_list(dbtest_musics, sim_matrix, music_title, top=10):
            target_music_index = dbtest_musics[dbtest_musics['music_title']== music_title].index.values

            dbtest_musics['similarity'] = sim_matrix[target_music_index, :].reshape(-1,1)

            temp = dbtest_musics.sort_values(by='similarity', ascending=False)
            final_index = temp.index.values[ :top]
            return dbtest_musics.iloc[final_index]

        similar_music = recommend_music_list(dbtest_musics_pandas, similarity_genre,'우린 그렇게 사랑해서')
        similar_music_01 = similar_music[['music_title','similarity']]
        print(similar_music_01)

        musics = Music.objects.all( )
        serializer = MusicSerializer(musics, many=True)


        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MusicSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 1. API 선호하는 음악 선택 - 추후 get은 top 100 으로 변경
class PlayListUserSelect(APIView):
    def get(self, request, user_id, format=None):
        musicplaylist100 = Music.objects.all()
        music_serializer = MusicSerializer(musicplaylist100, many=True)
        return Response(music_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlayListRecommendCreateSerializer)
    def post(self, request, user_id, format=None):
        print(request.user)
        user_musicplaylist_create_serializer = PlayListRecommendCreateSerializer(data = request.data)
        if user_musicplaylist_create_serializer.is_valid(): 
            user_musicplaylist_create_serializer.save(playlist_user=request.user)
            return Response(user_musicplaylist_create_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_musicplaylist_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2 API 추천 플레이리스트 (추후 변동 예정 - 추천 플레이리스트를 갖고 오는것으로)
class PlayListRecommended(APIView):
    def get(self, request, user_id):
        user_musicplaylist = PlayList.objects.all()
        user_musicplaylist_recommend_serializer = PlayListRecommendedSerializer(user_musicplaylist, many=True)
        return Response(user_musicplaylist_recommend_serializer.data, status=status.HTTP_200_OK)



# 3. 유저 커스텀 플레이 리스트
class PlayListview(APIView):
    def get(self, request):
        playlist = PlayList.objects.all( )
        serializer = PlayListCustomSerializer(playlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlayListCreateSerializer)
    def post(self, request):
        serializer = PlayListCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(playlist_user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  

# 4. 유저 커스텀 플레이 리스트 수정 및 삭제
class PlayListDetailview(APIView):
    # 본인 게시글 가져오기
    def get(self, request, playlist_id):
        playlist = get_object_or_404(PlayList, id=playlist_id)
        serializer = PlayListCustomSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlayListCreateSerializer)
    def put(self, request, playlist_id):
        playlist = get_object_or_404(PlayList, id=playlist_id)
        if request.user == playlist.playlist_user:
            serializer = PlayListCreateSerializer(playlist, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)



    def delete(self, request, playlist_id):
        playlist = get_object_or_404(PlayList, id=playlist_id)
        print(playlist.playlist_user)
        if request.user == playlist.playlist_user:
            playlist.delete()
            return Response("삭제 완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)
