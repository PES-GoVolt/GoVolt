from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.bikestations.services import store_data_stations, read_data_stations, delete_all_bikestations_fb, get_all_bikestations
from rest_framework.permissions import IsAuthenticated
from api.users.autentication import FirebaseAuthentication

class BikeStationsApiView(APIView):
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    def get(self,request):
        return Response(get_all_bikestations(),status=status.HTTP_200_OK)

class BikeStationsDatabaseApiView(APIView):
    
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    def post(self,request):
        bikestations = read_data_stations()
        store_data_stations(bikestations)
        return Response({'message':'The bike stations database was updated'},status=status.HTTP_201_CREATED)
