from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import json
from unittest.mock import patch
from rest_framework.response import Response

class LoginApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.users.views.get_auth_user')
    def test_successful_authentication(self, mock_get_auth_user):
        # Configurar el comportamiento esperado del mock
        mock_get_auth_user.return_value = Response({'message': "OK"},status=200)

        # Datos de prueba para la autenticación
        data = {'email': 'test@example.com', 'password': 'testpassword'}

        # Hacer la solicitud a la vista
        url = reverse('login')
        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea exitosa (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar el contenido de la respuesta
        self.assertEqual(response.data['message'], 'Successful Authentication')


    @patch('api.users.views.get_auth_user')
    def test_failed_authentication(self, mock_get_auth_user):
        # Configurar el comportamiento esperado del mock para una autenticación fallida
        mock_get_auth_user.return_value = Response({'message': "UNAUTHORIZED TEST"},status=401)

        # Datos de prueba para la autenticación
        data = {'email': 'test1@example.com', 'password': 'hola1234556'}

        # Hacer la solicitud a la vista
        url = reverse('login')

        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea un error de autenticación (HTTP 401 UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class LogOutApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.users.views.logout')
    def test_successful_logout(self, mock_logout):
        # Configurar el comportamiento esperado del mock
        mock_logout.return_value = Response({'message': "OK"}, status=200)

        # Hacer la solicitud a la vista
        url = reverse('logout')
        response = self.client.post(url, format='json')

        # Verificar que la respuesta sea exitosa (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar el contenido de la respuesta
        self.assertEqual(response.data['message'], 'Successful Logout')

    @patch('api.users.views.logout')
    def test_failed_logout(self, mock_logout):
        # Configurar el comportamiento esperado del mock para un cierre de sesión fallido
        mock_logout.return_value = Response({'message': "UNAUTHORIZED TEST"}, status=401)

        # Hacer la solicitud a la vista
        url = reverse('logout')
        response = self.client.post(url, format='json')

        # Verificar que la respuesta sea un error de cierre de sesión (HTTP 401 UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RegisterApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.users.views.store_user')
    def test_successful_registration(self, mock_store_user):
        # Configurar el comportamiento esperado del mock
        mock_store_user.return_value = Response({'message': "OK"}, status=200)

        # Datos de prueba para el registro
        data = {'email': 'test@example.com', 'password': 'testpassword', 'phone': '123456789'}

        # Hacer la solicitud a la vista
        url = reverse('register')
        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea exitosa (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar el contenido de la respuesta
        self.assertEqual(response.data['message'], 'Successful Registration')

    @patch('api.users.views.store_user')
    def test_failed_registration(self, mock_store_user):
        # Configurar el comportamiento esperado del mock para un registro fallido
        mock_store_user.return_value = Response({'message': "ERROR TEST"}, status=400)

        # Datos de prueba para el registro
        data = {'email': 'test@example.com', 'password': 'testpassword', 'phone': '123456789'}

        # Hacer la solicitud a la vista
        url = reverse('register')
        response = self.client.post(url, data, format='json')

        # Verificar que la respuesta sea un error de registro (HTTP 400 BAD REQUEST)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SeeMyProfileApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.users.views.get_see_my_profile')
    def test_see_my_profile(self, mock_get_see_my_profile):
        # Configurar el comportamiento esperado del mock
        mock_get_see_my_profile.return_value = {
            'first_name': 'John',
            'last_name': 'Doe',
            'photo_url': 'http://example.com/photo.jpg',
            'phone': '123456789',
            'email': 'john.doe@example.com'
        }

        # Hacer la solicitud a la vista
        url = reverse('see-my-profile')
        response = self.client.get(url, format='json')

        # Verificar que la respuesta sea exitosa (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar el contenido de la respuesta
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['photo_url'], 'http://example.com/photo.jpg')
        self.assertEqual(response.data['phone'], '123456789')
        self.assertEqual(response.data['email'], 'john.doe@example.com')

class EditMyProfileApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('api.users.views.edit_user')
    def test_edit_my_profile(self, mock_edit_user):
        # Configurar el comportamiento esperado del mock
        mock_edit_user.return_value = Response({'message': "OK"}, status=200)

        # Datos de prueba para la edición de perfil
        data = {
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
            'phone': '123456789',
            'photo_url': 'http://example.com/newphoto.jpg'
        }

        # Hacer la solicitud a la vista
        url = reverse('edit-my-profile')
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        # Verificar que la respuesta sea exitosa (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar el contenido de la respuesta
        self.assertEqual(response.data['message'], 'Successful Edit')