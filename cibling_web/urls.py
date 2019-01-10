from django.urls import path
from . import views

urlpatterns=[
    path('', views.Timeline, name='web-timeline'),
    path('newsfeed/', views.Newsfeed, name='newsfeed'),
    path('timeline/', views.Timeline, name='web-timeline'),
    path('timeline-2/', views.PostListView.as_view(), name='web-timeline-list-view'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='web-timeline-detail-view'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='web-timeline-update-view'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='web-timeline-delete-view'),
    path('post/new/', views.PostCreateView.as_view(), name='web-timeline-post-create-view'),
    path('timeline/<int:pk>/', views.timeline_profile , name='timeline-profile'),
    path('timeline-about/<int:pk>/', views.timeline_profile_about, name='timeline-profile-about')
]