from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from musicplaylist.models import Music, PlayList
from musicplaylist.serializers import MusicSerializer, PlayListRecommendedSerializer, PlayListRecommendCreateSerializer, PlayListCustomSerializer, PlayListCreateSerializer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import pandas as pd


# 1. API 선호하는 음악 선택 - 추후 get은 top 100 으로 변경
class PlayListUserSelect(APIView):
    def get(self, request, user_id, format=None):
        musicplaylist100 = Music.objects.filter(id__lte=100)
        music_serializer = MusicSerializer(musicplaylist100, many=True)
        return Response(music_serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(request_body=PlayListRecommendCreateSerializer)
    def post(self, request, user_id, format=None):
        user_musicplaylist_create_serializer = PlayListRecommendCreateSerializer(data = request.data)
        if user_musicplaylist_create_serializer.is_valid(): 
            user_musicplaylist_create_serializer.save(playlist_user=request.user, is_main=True)
            return Response(user_musicplaylist_create_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_musicplaylist_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2 API 추천 플레이리스트
class PlayListRecommended(APIView):
    def get(self, request, user_id):
        # top100 music
        musicplaylist100 = Music.objects.filter(id__lte=100)
        music_serializer = MusicSerializer(musicplaylist100, many=True)

        # 추천리스트
        dbtest_musics = Music.objects.all().values()
        dbtest_musics_pandas = pd.DataFrame(dbtest_musics)
       
       # 장르 데이터 벡터화
        counter_vector = CountVectorizer(ngram_range=(1,2), encoding=u'utf-8')
        c_vector_genres = counter_vector.fit_transform(dbtest_musics_pandas['music_genre'])
        c_vector_genres.shape
        counter_vector.vocabulary_
        
        similarity_genre = cosine_similarity(c_vector_genres, c_vector_genres)
        similarity_genre.shape

        # 유사도 구하는 함수
        def recommend_music_list(dbtest_musics, sim_matrix, music_title, top=10):
            target_music_index = dbtest_musics[dbtest_musics['music_title'] == music_title].index.values

            dbtest_musics['similarity'] = sim_matrix[target_music_index, :].reshape(-1,1)

            temp = dbtest_musics.sort_values(by='similarity', ascending=False)
            final_index = temp.index.values[ :top]
            return dbtest_musics.iloc[final_index]
                
        # 사용자가 취향으로 선택한 플레이 리스트에서 한곡을 랜덤 선택 (제목)
        myselect = PlayList.objects.get(playlist_user=user_id, is_main=True)   # 사용자의 대표 플레이 리스트
        print(myselect)
        print(user_id)
        print(request.user)
        myselect_title = myselect.playlist_select_musics.values("music_title")
        myselect_list = list(myselect_title)

        choice_music = random.choice(myselect_list)

        # 랜덤 선택된 곡 유사도 계산, 추천리스트를 music_id값으로 저장
        similar_music = recommend_music_list(dbtest_musics_pandas, similarity_genre, choice_music['music_title'])
        similar_music_01 = similar_music[['id', 'music_title','music_artist', 'music_genre']]
        similar_lists = similar_music_01['id']

        similar_music_list = []
        for i in similar_lists:
            similar_music_list.append(i)
        
        recommended_serializer = PlayListRecommendedSerializer(data = {"playlist_select_musics":similar_music_list})

        if recommended_serializer.is_valid(): 
            recommended_serializer.save(playlist_user=request.user)
            return Response(music_serializer.data+recommended_serializer.data, status=status.HTTP_201_CREATED) # 오류날 가능성 높음, 하나의 응답에 두개의 시리얼라이저 가능?
        else:
            return Response(recommended_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# 3. 유저 커스텀 플레이 리스트
class PlayListview(APIView):
    def get(self, request):
        playlist = PlayList.objects.all( )
        serializer = PlayListCustomSerializer(playlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(request_body=PlayListCreateSerializer)
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

    # @swagger_auto_schema(request_body=PlayListCreateSerializer)
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

