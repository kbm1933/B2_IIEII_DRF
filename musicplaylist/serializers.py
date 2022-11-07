from rest_framework import serializers
from musicplaylist.models import Music, PlayList

# 1. [GET] 음악 리스트 조회에 쓰이는 Serializer
class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

# 1. [POST] API - 선호하는 음악 선택에서 플레이리스트 create 만드는 것
class PlayListRecommendCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayList
        fields = ("playlist_select_musics","playlist_title" )
        
class TestSerializer(serializers.ModelSerializer): #추천 곡 id > 제목, 가수, url 바꿔줌
    class Meta:
        model = Music
        fields = ['id','music_title', 'music_artist', 'music_img']

# 2. API - 추천 플레이리스트 에서 쓰이는 Seriazlier
class PlayListRecommendedSerializer(serializers.ModelSerializer):
    playlist_select_musics = TestSerializer(many=True)
    class Meta:
        model = PlayList
        fields = ("playlist_select_musics",)

# 3,4 API - 유저가 만든 플레이리스트 및 상세 get 용 seriailizer
class PlayListCustomSerializer(serializers.ModelSerializer):
    playlist_user = serializers.SerializerMethodField()
    playlist_likes = serializers.SerializerMethodField()
    playlist_select_musics = TestSerializer(many=True)

    def get_playlist_user(self, obj):
        return obj.playlist_user.email

    def get_playlist_likes(self, obj):
        return obj.playlist_likes.count()

    class Meta:
        model = PlayList
        fields = ("id", "playlist_content", "playlist_title", "playlist_select_musics", "playlist_update_at", "playlist_user", "playlist_likes")

# 3. API - 유저가 만든 플레이리스트 및 상세 create 용 seriailizer
class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ("playlist_title", "playlist_select_musics","playlist_content")

# 4. API - 유저가 만든 플레이리스트 수정용
class PlayListEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ("playlist_title","playlist_content")