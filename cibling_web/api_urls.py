from django.urls import path
from .apis import ListPosts, DeletePost, CommentView, CreatePostView

urlpatterns =[
    path('posts', ListPosts.as_view(), name='list-posts'),
    path('post/<int:pk>', DeletePost.as_view(), name="delete-post"),
    path('comment', CommentView.as_view(), name='make-comment'),
    path('post/create', CreatePostView.as_view(), name='crete-post')
]