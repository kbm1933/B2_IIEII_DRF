from dataclasses import field
from rest_framework import serializers
from playlist.models import PlayList

class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        # models.py 정의된 model 호출 (거기에 저장되는 objects 가져올거니까)
        model = PlayList
        
        # 모든 objects 가져올거니까 all
        fields = '__all__'



class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ("list",)