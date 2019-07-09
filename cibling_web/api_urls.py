from django.urls import path
from .apis import ListPosts

urlpatterns =[
    path('posts', ListPosts.as_view(), name='list-posts')
]