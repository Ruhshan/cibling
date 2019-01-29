from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post, Comment, Activity

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



@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        type = 'post'
        user = instance.author
        snip = instance.content
        snip = snip[:20]
        text = user.username + ' has added a new post \"' + snip +'...\"'
        a= Activity.objects.create(actor=instance.author, post=instance,text=text, type=type)
        a.save()

@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    if created:
        type = 'comment'
        user = instance.author
        snip = instance.text
        snip = snip[:20]
        text = user.username + ' has added a new comment \"' + snip +'...\"'
        a = Activity.objects.create(actor=instance.author, post=instance.post, text=text, type=type)
        a.save()

