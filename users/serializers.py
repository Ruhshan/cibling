from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Institute, Expertise, Interest

class InstituteSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'


class ExpertiseSerializer(ModelSerializer):
    class Meta:
        model = Expertise
        fields = "__all__"


class InterestSerializer(ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"
