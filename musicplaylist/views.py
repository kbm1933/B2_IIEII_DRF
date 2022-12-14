from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from musicplaylist.models import Music, PlayList
from user.models import User
from musicplaylist.serializers import MusicSerializer, PlayListRecommendedSerializer, PlayListRecommendCreateSerializer, PlayListCustomSerializer, PlayListCreateSerializer, PlayListEditSerializer
from user.serializers import UserSerializer
from similarity import random_choice, recommend_music_list

# 1. API 선호하는 음악 선택 - 추후 get은 top 100 으로 변경
class PlayListUserSelect(APIView):
    def get(self, request, user_id, format=None):
        music_playlist100 = Music.objects.filter(id__lte=100)
        music_serializer = MusicSerializer(music_playlist100, many=True)
        return Response(music_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, format=None):
        user_musicplaylist_create_serializer = PlayListRecommendCreateSerializer(data = request.data)
        if user_musicplaylist_create_serializer.is_valid(): 
            user_musicplaylist_create_serializer.save(playlist_user=request.user, is_main=True)

             # 사용자 선택 곡 중 랜덤 한 곡 지정
            choice_music = random_choice(user_id) 
        
            # 랜덤 선택된 곡 유사도 계산, 추천리스트를 music_id값으로 저장
            similar_music = recommend_music_list(choice_music['music_title'])    
            similar_music_01 = similar_music[['id', 'music_title','music_artist', 'music_genre']]
            similar_lists = similar_music_01['id']
            similar_music_list = []
            for i in similar_lists:
                similar_music_list.append(i)
            
            recommended_serializer = PlayListRecommendCreateSerializer(data = {"playlist_select_musics":similar_music_list,
        "playlist_title" : "recommend playlist" })

            if recommended_serializer.is_valid(): 
                recommended_serializer.save(playlist_user=request.user)
                return Response("성공", status=status.HTTP_201_CREATED)
        else:
            return Response(user_musicplaylist_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2 API 추천 플레이리스트
class PlayListRecommended(APIView):
    def get(self, request, user_id):

        recommend_playlist = PlayList.objects.filter(playlist_title = "recommend playlist").last() #마지막 플레이리스트 = 추천된 플레이리스트
        recommend_playlist_serializer = PlayListRecommendedSerializer(recommend_playlist)
        print(recommend_playlist_serializer.data)

        # 뮤직 모델스도 갖고 와서 한번에 데이터에 넣어줬습니다.
        music_playlist100 = Music.objects.filter(id__lte=100)
        music_playlist100_serializer = MusicSerializer(music_playlist100, many=True)
        print(music_playlist100_serializer)
        
        data = {
            "recommend_playlist" : recommend_playlist_serializer.data,
            # 뮤직 top 100 추가
            "music_top100":music_playlist100_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
        

# 3. 유저 커스텀 플레이 리스트
class PlayListview(APIView):
    def get(self, request, user_id):
        playlist = PlayList.objects.filter(playlist_user_id = user_id)
        playlist_serializer = PlayListCustomSerializer(playlist, many=True)

        music_list = Music.objects.all()
        music_serializer = MusicSerializer(music_list, many=True)

        # 프로필 생성을 위해 유저 데이터를 가지고 왔습니다.
        user_data = User.objects.all()
        user_serializer = UserSerializer(user_data, many=True)

        data = {
            "playlist" : playlist_serializer.data,
            "music_list" :music_serializer.data,
            "user_profile":user_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
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
  
    def put(self, request, playlist_id):
        playlist = get_object_or_404(PlayList, id=playlist_id)
        if request.user == playlist.playlist_user:
            serializer = PlayListEditSerializer(playlist, data=request.data)

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