from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default=None, null=True)
    description = models.TextField(max_length=200, default=None, null=True)
    rates = models.IntegerField(default=0, null=True)
    idols = models.CharField(max_length=1000,default=0, null=True)
    fans = models.CharField(max_length=1000,default=0, null=True)

    def __str__(self):
        return f'{self.user.username}'
