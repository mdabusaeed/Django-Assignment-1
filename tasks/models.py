from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_participants')  
    rsvp_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvped_events', blank=True)

    def __str__(self):
        return self.name



    

