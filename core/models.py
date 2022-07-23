from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model() #prefer over django.contrib.auth.models.User to add custom Authentication models for AUTH_USER_MODEL
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to = 'profile_images', default= 'blank-profile-picture.png')
    location= models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'post-images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.user
