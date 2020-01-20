from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField

from django_private_chat.models import Dialog, Message
from users.serializers import UserSerializer, ProfileInfoSerializer


class DialogSerializer(ModelSerializer):
    owner = UserSerializer("owner")
    opponent = UserSerializer("opponent")
    profileinfo = ProfileInfoSerializer(read_only=True)
    last_message = ReadOnlyField()
    last_message_time = ReadOnlyField()

    unread = SerializerMethodField()

    class Meta:
        model = Dialog
        depth =1
        fields = '__all__'

    def get_unread(self, obj):
        res = obj.messages.filter(read=False).exclude(sender=self.context['request'].user).count()
        return res


class MessageSerializer(ModelSerializer):
    sender = UserSerializer("sender")
    class Meta:
        model = Message
        depth = 1
        fields = '__all__'