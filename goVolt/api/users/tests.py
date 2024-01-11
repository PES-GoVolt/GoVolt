import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


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