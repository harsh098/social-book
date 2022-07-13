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
def deleteProfile(sender, instance, created, **kwargs):
    user= instance.user
    user.delete()
