from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=11, blank=True, null=True)
    profileImage = models.ImageField(upload_to='profileImage/', blank=True, default='profileImages/default.jpg')

    def __str__(self):
        return self.username

