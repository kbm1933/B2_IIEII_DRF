from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from playlist import serializers
from playlist.models import PlayList
from playlist.serializers import PlayListSerializer, PlayListCreateSerializer



class CustomPlaylistView(APIView):
    def get(self, request, list_id):
        playlists = PlayList.objects.all()

        serializer = PlayListSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, list_id):
        serializer = PlayListCreateSerializer(data=request.data)

        if serializer.is_valid():
            # user = request.user : custom user 모델 정의 후
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomPlaylistDetailView(APIView):
    pass


