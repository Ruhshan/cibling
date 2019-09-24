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


class ProfileInfoSerializer(ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = "__all__"


class UserSerializer(ModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(view_name='timeline-profile')
    profile_image = serializers.ImageField(source="profile.image", read_only=True)

    class Meta:
        model = User
        fields = ["id","first_name","last_name", "profile_url","profile_image"]


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

class ProfileImageSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image"]

class ProfileCoverSeriaizer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ["cover_image"]
