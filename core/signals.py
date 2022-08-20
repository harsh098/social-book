from .models import *
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user= user,
            id_user=user.id
        )
        
        profile.save()
        
        
    else:
        pass

@receiver(post_delete, sender=Profile)
def deleteProfile(sender, instance, **kwargs):
    user= instance.user
    user.delete()

@receiver(post_save, sender=LikePost)
def incLikes(sender, instance, created, **kwargs):
    if created:
        like = instance
        post = Post.objects.get(id=like.post_object.id)
        post.no_of_likes += 1
        post.save()

@receiver(post_delete, sender=LikePost)
def decLikes(sender, instance,  **kwargs):
    like = instance
    post = Post.objects.get(id=like.post_object.id)
    post.no_of_likes -= 1
    post.save()