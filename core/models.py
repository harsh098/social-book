from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model() #prefer over django.contrib.auth.models.User to add custom Authentication models for AUTH_USER_MODEL
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to = 'profile_images', default= 'blank-profile-picture.png')
    location= models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    