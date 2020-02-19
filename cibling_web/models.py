from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    content = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default=None, upload_to='post_pics/', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    youtubeId = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('web-timeline-detail-view', kwargs={'pk':self.pk})

class Comment(models.Model):
    text = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text

class Activity(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    time_posted = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    type = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text

class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postPhotos')
    image = models.ImageField(default=None, upload_to='post_pics/', null=True)