from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Institute, Expertise, Interest, Profile, Country, Subject, ProfileInfo
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


class ProfileInfoSerializer(ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = "__all__"

class ProfileSerializer(ModelSerializer):
    user = UserSerializer("user")
    profileinfo = ProfileInfoSerializer(read_only=True)
    class Meta:
        model = Profile
        depth = 1
        fields = "__all__"


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


