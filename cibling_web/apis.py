from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer, MakeCommentSerializer
from .models import Post
import time


class PostResultPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ListPosts(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostResultPagination

    def get_queryset(self):
        # time.sleep(3)
        author_ids = list(self.request.user.cibling_1.values_list("cibling_2__id", flat=True))
        author_ids.extend(list(self.request.user.cibling_2.values_list("cibling_1__id", flat=True)))
        author_ids.append(self.request.user.id)
        queryset = Post.objects.filter(author__in=author_ids).order_by('-time_posted')

        return queryset


class DeletePost(APIView):
    def delete(self, request, pk, format=None):
        print(pk)
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentView(APIView):
    def post(self, request):
        try:
            serialized = MakeCommentSerializer(data=request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

