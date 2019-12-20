from rest_framework.generics import ListAPIView

from django_private_chat.models import Dialog
from django_private_chat.serializers import DialogSerializer


class DialogHistoryApiView(ListAPIView):
    serializer_class = DialogSerializer

    def get_queryset(self):
        from django.db.models import Q
        return Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
