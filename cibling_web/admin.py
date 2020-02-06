from django.contrib import admin
from .models import Post, Comment, Activity, PostPhoto

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Activity)
admin.site.register(PostPhoto)
# Register your models here.
