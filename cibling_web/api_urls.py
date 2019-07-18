from django.urls import path
from .apis import ListPosts, DeletePost

urlpatterns =[
    path('posts', ListPosts.as_view(), name='list-posts'),
    path('post/<int:pk>', DeletePost.as_view(), name="delete-post")
]