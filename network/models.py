from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        "User", blank=True, related_name="user_following"
    )
    followers = models.ManyToManyField(
        "User", blank=True, related_name="user_followers"
    )


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    text = models.TextField(max_length=250)
    likes = models.ManyToManyField(User, related_name="likes", default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
