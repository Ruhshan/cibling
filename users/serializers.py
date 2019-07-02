from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Institute, Expertise, Interest, Profile, Country
from django.contrib.auth.models import User

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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name","last_name"]


class ProfileSerializer(ModelSerializer):
    user = UserSerializer("user")
    class Meta:
        model = Profile
        fields = "__all__"


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"