from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Institute, Expertise, Interest
from .serializers import InstituteSerializer, ExpertiseSerializer, InterestSerializer

class ListInstitutes(APIView):
    def get(self, request, country):
        queryset = Institute.objects.filter(country=country)
        serialized = InstituteSerializer(queryset, many=True)

        return Response(serialized.data)

class ListExpertise(APIView):
    def get(self, request):
        queryset = Expertise.objects.all()
        serialized = ExpertiseSerializer(queryset, many=True)
        return Response(serialized.data)

class ListInterests(APIView):
    def get(self, request):
        queryset = Interest.objects.all()
        serialized = InterestSerializer(queryset, many=True)
        return Response(serialized.data)