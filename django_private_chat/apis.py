from rest_framework.generics import ListAPIView

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
        return Message.objects.filter(dialog=dialog_id)