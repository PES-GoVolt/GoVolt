from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
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
from api.users.services import get_auth_user, store_user, get_see_my_profile

class LoginApiView(APIView):
    @csrf_exempt
    def post(self, request):
        # Recuperamos las credenciales y autenticamos al usuario
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None or password is None:
            return Response({'message': 'It is necessary to enter Email and Password'},status=status.HTTP_400_BAD_REQUEST)

        result = get_auth_user(email, password)

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
            return Response({'message':'Successful Authentication'},status=status.HTTP_200_OK)

class LogOutApiView(APIView):
    @login_required
    @csrf_exempt
    def post(self, request):
        response = Response({'message': 'Logout successful'})
        response.delete_cookie('firebaseToken')  # Borra la cookie del token de Firebase
        return response

class RegisterApiView(APIView):
    @csrf_exempt
    def post(self, request):

        data = json.loads(request.body)

        print(data)

        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        if len(password) < 6:
                return Response({'message': 'Password must be at least 6 characters long'},status=status.HTTP_400_BAD_REQUEST)
        print("aqui")
        result = store_user(email, password, phone)

        print(result)
        if isinstance(result, Exception):
            # Verificar si result es una excepción
            return Response({"message": str(result)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Si result no es una excepción, es el resultado exitoso
            return Response({'message':'Successful Registration'},status=status.HTTP_200_OK)

class SeeProfileApiView(APIView):
    def get(self, request):
        return Response(get_see_my_profile(), status=status.HTTP_200_OK)