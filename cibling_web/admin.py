from django.contrib import admin
from .models import Post, Comment, Activity

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Activity)
# Register your models here.
