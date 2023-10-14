from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.chargers.services import get_chargers_by_codi_prov,get_all_chargers


class ChargerLocationApiView(APIView):
    def get(self,request):
        response_data = get_all_chargers()
        return Response(response_data,status=status.HTTP_200_OK)


    