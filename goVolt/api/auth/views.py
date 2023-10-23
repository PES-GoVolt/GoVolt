from django.shortcuts import render
from firebase_admin import auth, exceptions
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
from goVolt.settings import AUTH_DB

class LoginApiView(APIView):
    @csrf_exempt
    def post(self, request):
        # Recuperamos las credenciales y autenticamos al usuario
        email= request.data.get('email', None)
        password = request.data.get('password', None)
        print(email)
        print(password)
        if email is None or password is None:
            return Response({'message': 'Es necesario introducir Email y Contraseña'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            auth_user = AUTH_DB.sign_in_with_email_and_password(email, password)
        except ValueError as e:
            return Response({'error': str(e)})
        
        print(auth_user)

        if not auth_user:
            return Response({'message': 'Email o Contraseña incorrecto.'},status=status.HTTP_404_NOT_FOUND)

        # Si es correcto añadimos a la request la información de sesión
        if auth_user:
            # para loguearse una sola vez
            return Response({'message':'Email y Contraseña correctos.'},status=status.HTTP_200_OK)
            #return response.Response({'token': token.key}, status=status.HTTP_200_OK)

        # Si no es correcto devolvemos un error en la petición
        return Response(status=status.HTTP_404_NOT_FOUND)

class LogOutApiView(APIView):
    @login_required
    @csrf_exempt
    def post(self, request):
        # Cerrar la sesión del usuario
        # Esto puede variar dependiendo de cómo tengas configurada tu autenticación
        # En el ejemplo, se borra el token de autenticación almacenado en el cliente
        # para forzar el cierre de sesión
        response = JsonResponse({'message': 'Logout successful'})
        response.delete_cookie('firebaseToken')  # Borra la cookie del token de Firebase
        return response

class RegisterApiView(APIView):
    @csrf_exempt
    def post(self, request):

        data = json.loads(request.body)

        # Obtén los datos de registro del formulario o la solicitud POST
        #email = data.get('email')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        if len(password) < 6:
                return Response({'message': 'Password must be at least 6 characters long'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Crea una cuenta de usuario en Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                phone_number=phone,
            )

            # El usuario se ha registrado correctamente
            return Response({'message': 'Registration successful'},status=status.HTTP_200_OK)
        except ValueError as e:
            # Maneja cualquier error de autenticación
            return Response({'message': 'Registration failed: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)