from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from playlist import serializers
from playlist.models import PlayList, Music
from playlist.serializers import MusicCreateSerializer, PlaySerializer, PlayListSerializer, PlayListCreateSerializer


class MusicListview(APIView):
    def get(self, request):
        musics = Music.objects.all( )
        serializer = MusicCreateSerializer(musics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MusicCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  





class PlayListview(APIView):
    def get(self, request):
        articles = PlayList.objects.all( )
        serializer = PlayListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlayListCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  


class PlayListDetailview(APIView):
    # 본인 게시글 가져오기
    def get(self, request, article_id):
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(PlayList, id=article_id)
        serializer = PlaySerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def put(self, request, article_id):
        article = get_object_or_404(PlayList, id=article_id)
        if request.user == article.user:
            serializer = PlayListCreateSerializer(article, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)



    def delete(self, request, article_id):
        article = get_object_or_404(PlayList, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response("삭제 완료", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)




# --------------------------------------------------------
  


