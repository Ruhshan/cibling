from users.serializers import UserSerializer, ProfileSerializer
from .models import Post, Comment
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from django.utils.html import urlize

class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"


class MakeCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"



class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    detail_url = HyperlinkedIdentityField(view_name='post-detail-view')


    class Meta:
        model = Post
        depth = 1
        fields = "__all__"



