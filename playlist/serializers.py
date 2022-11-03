from rest_framework import serializers
from playlist.models import PlayList, Music


class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        # fields가 한개더라도 무조건 ',' 붙여줘야 함 -> 안그러면 str로 인식
        fields = '__all__'



# ----------------------------------------------------------------



class PlaySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    # ArticleSerializer가 선언된 게시글의 좋아요를 누른 사용자를 볼때 단순 id가 아닌 사용자의 id를 string:문자로 가져오게 할 수 있다.
    likes = serializers.StringRelatedField(many=True)

    # 여기서 정의된 user의 email이 위에 user값에 들어가게 된다
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = PlayList
        fields = '__all__'




class PlayListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ("title", "select_musics","content")




class PlayListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()


    def get_user(self, obj):
        return obj.user.email

    def get_likes_count(self, obj):
        return obj.likes.count()


    class Meta:
        model = PlayList
        fields = ("pk", "title", "select_musics", "update_at", "user", "likes_count")

