from django.urls import path
from . import views

urlpatterns=[
    path('', views.Newsfeed, name='newsfeed'),
    path('newsfeed/', views.Newsfeed, name='newsfeed'),
    #path('timeline/', views.Timeline, name='web-timeline'),
    #path('timeline-2/', views.PostListView.as_view(), name='web-timeline-list-view'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='web-timeline-detail-view'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='web-timeline-update-view'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='web-timeline-delete-view'),
    path('post/new/', views.PostCreateView.as_view(), name='web-timeline-post-create-view'),
    path('timeline/<int:pk>/', views.timeline_profile , name='timeline-profile'),
    path('timeline-about/<int:pk>/', views.timeline_profile_about, name='timeline-profile-about'),
    path('timeline/ciblings/<int:pk>/', views.timeline_ciblings, name='timeline-ciblings'),
    path('add-cibling/<int:pk>/', views.add_cibling, name='add-cibling'),
    path('accept-cibling/<int:pk>/', views.accept_cibling, name='accept-cibling'),
    path('cibling-requests/', views.cibling_request, name='cibling-requests'),
    path('about/', views.about, name='about')
]