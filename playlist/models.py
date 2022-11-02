from django.db import models
# from user.models import User

# Create your models here.
class PlayList(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  
    list = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.list)