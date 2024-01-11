from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from firebase_admin import auth
from firebase_admin.auth import ExpiredIdTokenError
from rest_framework import authentication
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from api.users.services import store_user, get_see_my_profile, edit_user,increment_achievement,get_achievements, has_info_external
from rest_framework.permissions import IsAuthenticated
from api.users.authentication import FirebaseAuthentication



class AchievementsApiView(APIView):
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def post(self,request):
        achievement = request.data['achievement']
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        increment_achievement(firebase_token,achievement)
        return Response({"message":"Achievement incremented"},status=status.HTTP_200_OK)
    
    def get(self,request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]
        return Response(get_achievements(firebase_token),status=status.HTTP_200_OK)

class RegisterApiView(APIView):
    @csrf_exempt
    def post(self, request):

        data = json.loads(request.body)
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        email = data.get('email')
        phone = data.get('phone')
        username = data.get('username')

        result = store_user(firebase_token, email, phone, username)


        if (result.status_code != 200):
            code = result.status_code
            
            if code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": result.data.get('message')}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message':'Successful Registration'},status=status.HTTP_200_OK)

class SeeMyProfileApiView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    
    def get(self, request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        return Response(get_see_my_profile(firebase_token), status=status.HTTP_200_OK)
    
class EditMyProfileApiView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def post(self, request):

        data = json.loads(request.body)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        photo_url = data.get('photo_url')

        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        result = edit_user(firebase_token, first_name, last_name, phone, photo_url)

        if isinstance(result, Exception):
            # Verificar si result es una excepción
            error_message = result.args[1]
            error_data = json.loads(error_message)

            code = error_data['error']['code']
            msg = error_data['error']['message']

            if code == 200:
                st = status.HTTP_200_OK
            elif code == 400:
                st = status.HTTP_400_BAD_REQUEST
            elif code == 401:
                st = status.HTTP_401_UNAUTHORIZED
            elif code == 403:
                st = status.HTTP_403_FORBIDDEN
            elif code == 404:
                st = status.HTTP_404_NOT_FOUND
            elif code == 500:
                st = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"message": msg}, status=st)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message':'Successful Edit'},status=status.HTTP_200_OK)
        
class ExternalUserApiView(APIView):

    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]
    
    def get(self, request):
        firebase_token = request.headers.get("Authorization", "").split(" ")[1]

        return Response(has_info_external(firebase_token), status=status.HTTP_200_OK)