from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ProfileInfo, Profile

'''
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, institute=kwargs)
'''

'''
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
'''

@receiver(post_save, sender=Profile)
def create_profile_info(sender, instance, created, **kwargs):
    if created:
        ProfileInfo.objects.create(profile=instance)

@receiver(post_save, sender=Profile)
def save_profile(sender, instance, **kwargs):
    #print(instance)
    instance.profileinfo.save()
