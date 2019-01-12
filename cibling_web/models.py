from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    #title = models.CharField(max_length=100)
    content = models.TextField()
    #hasImage = models.fields.BinaryField(default=False)
    time_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default=None, upload_to='post_pics/', null=True)
    #image_url = models.CharField(max_length=100, default='none')
    #time_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('web-timeline-detail-view', kwargs={'pk':self.pk})

class Comment(models.Model):
    text = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text