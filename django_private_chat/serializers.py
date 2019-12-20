from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField

from django_private_chat.models import Dialog
from users.serializers import UserSerializer, ProfileInfoSerializer


class DialogSerializer(ModelSerializer):
    owner = UserSerializer("owner")
    opponent = UserSerializer("opponent")
    profileinfo = ProfileInfoSerializer(read_only=True)
    last_message = ReadOnlyField()
    last_message_time = ReadOnlyField()


    class Meta:
        model = Dialog
        depth =1
        fields = '__all__'
