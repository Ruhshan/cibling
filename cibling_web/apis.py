from rest_framework.generics import ListAPIView
from .serializers import PostSerializer
from .models import Post
from django.db.models import Q



class ListPosts(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        author_ids = list(self.request.user.cibling_1.values_list("cibling_2__id", flat=True))
        author_ids.extend(list(self.request.user.cibling_2.values_list("cibling_1__id", flat=True)))
        author_ids.append(self.request.user.id)
        queryset = Post.objects.filter(author__in=author_ids).order_by('-time_posted')

        return queryset



