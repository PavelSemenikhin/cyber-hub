from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Модель користувача

class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=50, blank=True)
    favorite_games = models.ManyToManyField("tournaments.Game", blank=True, related_name="profiles")
    discord = models.CharField(max_length=100, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.nickname or self.user.username
