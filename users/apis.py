from django.db.models import Q, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Institute, Expertise, Interest, Profile, Country, Subject
from django.contrib.auth.models import User
from .serializers import InstituteSerializer, ExpertiseSerializer, InterestSerializer, ProfileSerializer, CountrySerializer, SubjectSerializer
from postman.api import pm_write


class ListInstitutes(APIView):
    def get(self, request, country):
        queryset = Institute.objects.filter(country=country)
        serialized = InstituteSerializer(queryset, many=True)

        return Response(serialized.data)


class ListExpertise(ListAPIView):
    serializer_class = ExpertiseSerializer
    queryset = Expertise.objects.all()


class ListInterests(APIView):
    def get(self, request):
        queryset = Interest.objects.all()
        serialized = InterestSerializer(queryset, many=True)
        return Response(serialized.data)

class ListProfiles(APIView):
    def get(self, request):
        search_text =self.request.query_params["q"]
        users = User.objects.annotate(name=Concat('first_name', Value(" "), 'last_name')).filter(
            name__icontains=search_text)
        queryset = Profile.objects.filter(user__in=users)
        serialized = ProfileSerializer(queryset, many=True)

        return Response(serialized.data)


class SendMessage(APIView):
    def post(self, request):

        print(self.request.data)
        try:

            pm_write(sender=self.request.user,
                     recipient=User.objects.get(id=self.request.data["recipient"]),
                     subject=self.request.data["subject"],
                     body=self.request.data["body"])
            return Response("ok")

        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListCountries(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class ListSubjects(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

