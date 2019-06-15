from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Institute

class InstituteSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'