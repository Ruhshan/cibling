from users.serializers import UserSerializer, ProfileSerializer
from .models import Post, Comment
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        depth = 1
        fields = "__all__"



