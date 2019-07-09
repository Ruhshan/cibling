from .models import Post, Comment
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"



class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"



