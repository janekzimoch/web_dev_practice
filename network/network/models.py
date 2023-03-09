from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="followed_users")
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_posts')
    users_liked = models.ManyToManyField(User, related_name="liked_posts")
    text_title = models.TextField()
    text_body = models.TextField()
    time_published = models.CharField(max_length=32)
    num_likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "users_liked": [u.id for u in self.users_liked.all()],
            "text_title": self.text_title,
            "text_body": self.text_body,
            "time_published": self.time_published,
        }