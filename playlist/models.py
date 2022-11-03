from django.db import models
from user.models import User

# Create your models here.

class Music(models.Model):
    singer = models.CharField(max_length=50)
    music_title = models.CharField(max_length=50)

    def __str__(self):
        return str(self.music_title)

        
class PlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # music = models.ForeignKey(Music, on_delete=models.CASCADE)
    select_musics = models.ManyToManyField(Music, related_name="select_musics_set")
    title = models.CharField(max_length=50)
    content = models.TextField()

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # 좋아요
    likes = models.ManyToManyField(User, related_name="like_playlists")

    def __str__(self):
        return str(self.title)


