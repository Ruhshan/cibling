from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Institute
from .serializers import InstituteSerializer

class ListInstitutes(APIView):
    def get(self, request, country):
        queryset = Institute.objects.filter(country=country)
        serialized = InstituteSerializer(queryset, many=True)
        return Response(serialized.data)