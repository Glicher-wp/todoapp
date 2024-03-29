from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    key = models.CharField(max_length=32, blank=True, null=True)
    token = models.CharField(max_length=64, blank=True, null=True)


    def __str__(self):
        return "Профиль пользователя %s % self.user.username"
