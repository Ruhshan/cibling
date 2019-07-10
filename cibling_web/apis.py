from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .serializers import PostSerializer
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
        #time.sleep(3)
        author_ids = list(self.request.user.cibling_1.values_list("cibling_2__id", flat=True))
        author_ids.extend(list(self.request.user.cibling_2.values_list("cibling_1__id", flat=True)))
        author_ids.append(self.request.user.id)
        queryset = Post.objects.filter(author__in=author_ids).order_by('-time_posted')

        return queryset


