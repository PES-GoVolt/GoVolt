from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.chargers.services import get_all_chargers,read_data,store_charge_points_fb,delete_all_charge_points_fb


class ChargerLocationApiView(APIView):
    def get(self,request):
        response_data = get_all_chargers()
        return Response(response_data,status=status.HTTP_200_OK)


class ChargerDataBaseApiView(APIView):
    def post(self,request):
        chargers = read_data()
        store_charge_points_fb(chargers)
        return Response({'message':'The chargers database was updated'},status=status.HTTP_200_OK)