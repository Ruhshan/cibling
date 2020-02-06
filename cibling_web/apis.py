from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer, MakeCommentSerializer
from .models import Post, PostPhoto
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


class CreatePostView(APIView):
    def post(self, request):
        if request.data['content']:
            p = Post.objects.create(author=request.user, content=request.data['content'])
            p.save()

            for img in request.data['images']:
                decoded = decode_base64_file(img['val'])
                postImg = PostPhoto.objects.create(post = p, image=decoded)
                postImg.save()
        return Response("ok", status=status.HTTP_201_CREATED)



def decode_base64_file(data):

    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension, )

        return ContentFile(decoded_file, name=complete_file_name)


#
# import decode_base64_file
#
# p = Post(content='My Picture', image=decode_based64_file(your_base64_file))
# p.save()