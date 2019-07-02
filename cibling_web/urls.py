from django.urls import path

from users.forgot_password_view import ForgotPasswordView
from . import views
from .find_cibling_views import FindCiblingPageView
urlpatterns=[
    path('', views.Newsfeed, name='newsfeed'),
    path('newsfeed/', views.Newsfeed, name='newsfeed'),
    #path('timeline/', views.Timeline, name='web-timeline'),
    #path('timeline-2/', views.PostListView.as_view(), name='web-timeline-list-view'),
    path('post/<int:pk>/', views.post_detail_view, name='post-detail-view'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='web-timeline-update-view'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='web-timeline-delete-view'),
    path('post/new/', views.PostCreateView.as_view(), name='web-timeline-post-create-view'),
    path('comment/<int:pk>/delete', views.delete_comment, name='delete-comment'),
    path('post/<int:pk>/delete', views.delete_post, name='delete-post'),
    path('timeline/<int:pk>/', views.timeline_profile , name='timeline-profile'),
    path('timeline-about/<int:pk>/', views.timeline_profile_about, name='timeline-profile-about'),
    path('timeline/ciblings/<int:pk>/', views.timeline_ciblings, name='timeline-ciblings'),
    path('timeline/album/<int:pk>/', views.timeline_album, name='timeline-album'),
    path('add-cibling/<int:pk>/', views.add_cibling, name='add-cibling'),
    path('accept-cibling/<int:pk>/', views.accept_cibling, name='accept-cibling'),
    path('cibling-requests/', views.cibling_request, name='cibling-requests'),
    path('about/', views.about, name='about'),
    path('find-ciblings/<int:pk>', views.find_ciblings, name='find-ciblings'),
    path('search-ciblings/', FindCiblingPageView.as_view(), name='search-ciblings'),
    #path('search/<slug:pk>/', views.search_result, name='search-result'),
    path('search/', views.search_result, name='search-result'),
    path('forgot-password', ForgotPasswordView.as_view(), name="forgot-password")
]