from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from django_private_chat.models import Dialog, Message
from django_private_chat.serializers import DialogSerializer, MessageSerializer


class DialogHistoryApiView(ListAPIView):
    serializer_class = DialogSerializer

    def get_queryset(self):
        from django.db.models import Q
        return Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))


class MessagesApiView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        dialog_id = self.kwargs['dialog_id']
        return Message.objects.filter(dialog=dialog_id).order_by('id')


class DialogCreateApiView(APIView):
    def post(self, request):
        user = get_object_or_404(get_user_model(), username=request.data["opponent"])
        dialog, created = Dialog.objects.get_or_create(owner=self.request.user, opponent=user)

        serialized = DialogSerializer(dialog,context={'request': request}).data
        return Response(data=serialized, status=status.HTTP_200_OK)




