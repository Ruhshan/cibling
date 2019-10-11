from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Institute, Expertise, Interest, Profile, Country, Subject, Offer, Language
from django.contrib.auth.models import User
from .serializers import InstituteSerializer, ExpertiseSerializer, InterestSerializer, ProfileSerializer, CountrySerializer, SubjectSerializer, UserSerializer
from .serializers import ProfileImageSerializer, ProfileCoverSeriaizer , OfferSerializer, LanguageSerializer
from postman.api import pm_write

import time

class ListInstitutes(APIView):
    def get(self, request, country):
        queryset = Institute.objects.filter(country=country)
        serialized = InstituteSerializer(queryset, many=True)

        return Response(serialized.data)


class ListExpertise(ListAPIView):
    serializer_class = ExpertiseSerializer
    queryset = Expertise.objects.all()


class ListOffer(ListAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


class ListLanguage(ListAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class ListInterests(APIView):
    def get(self, request):
        queryset = Interest.objects.all()
        serialized = InterestSerializer(queryset, many=True)
        return Response(serialized.data)


class ListProfiles(APIView):
    def get(self, request):
        search_text = self.request.query_params["q"]
        users = User.objects.annotate(name=Concat('first_name', Value(" "), 'last_name')).filter(
            name__icontains=search_text)
        queryset = Profile.objects.filter(user__in=users)
        serialized = ProfileSerializer(queryset, many=True, context={'request': request})

        return Response(serialized.data)

    def post(self, request):
        profiles = Profile.objects.all()

        country = self.request.data.get("country")
        institute = self.request.data.get("institute")
        subject = self.request.data.get("subject")
        expertise = self.request.data.get("expertise")
        offer = self.request.data.get("offer")
        interest = self.request.data.get("interest")

        if country:
            profiles = profiles.filter(institute__country=country)
        if institute:
            profiles = profiles.filter(institute=institute)
        if subject:
            profiles = profiles.filter(profileinfo__subject=subject)
        if expertise:
            profiles = profiles.filter(profileinfo__expertises=expertise)
        if offer:
            profiles = profiles.filter(profileinfo__offers=offer)
        if interest:
            profiles = profiles.filter(profileinfo__interests=interest)

        serialized = ProfileSerializer(profiles, many=True, context={'request': request})

        if profiles.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serialized.data)


class RetrieveProfile(APIView):
    def get(self, request, user):
        try:
            serializer = UserSerializer(User.objects.get(username=user),context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class SendMessage(APIView):
    def post(self, request):
        try:
            pm_write(sender=self.request.user,
                     recipient=User.objects.get(id=self.request.data["recipient"]),
                     subject=self.request.data["subject"],
                     body=self.request.data["body"])
            return Response("ok")

        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListCountries(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class ListSubjects(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class Me(APIView):
    def get(self, request):
        user = self.request.user
        serialized = UserSerializer(user,context={'request': request})

        return Response(serialized.data)


class ListCiblings(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):

        cibling_ids = list(self.request.user.cibling_1.values_list("cibling_2__id", flat=True))
        cibling_ids.extend(list(self.request.user.cibling_2.values_list("cibling_1__id", flat=True)))
        profiles = Profile.objects.filter(user__in=cibling_ids)

        return profiles


class UpdateProfilePic(UpdateAPIView):
    serializer_class = ProfileImageSerializer

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        if pk == self.request.user.id:
            return User.objects.get(id=pk).profile
        else:
            raise Http404


class UpdateCoverPic(UpdateAPIView):
    serializer_class = ProfileCoverSeriaizer

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        if pk == self.request.user.id:
            return User.objects.get(id=pk).profile
        else:
            raise Http404
