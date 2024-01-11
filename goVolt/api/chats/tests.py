from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class MessagesAPIViewTest(TestCase):
    def test_send_message(self):
        client = APIClient()
        url = reverse('messages-view')
        data = {
            "content" : "Hello",
            "room_name" : "random_room",
            "sender" : "Hi"
        }
        response = client.post(url,data, format= 'json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_get_messages_room(self):
        client = APIClient()
        url = reverse('messages-view')
        data = {
            "room_name": "qwerty3"
        }
        response = client.get(url, params=data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
class ChatsAPIViewTest(TestCase):
    def test_create_chat(self):
        client =APIClient()
        url = reverse('chats-view')
        url_login = reverse('login')
        data  = {
            "user_uid" : "e8SVfGTaNlPGNYI57WNCKXh6F2f2",
            "room_name": "qwerty"
        }
        login_data = {
            "email": "pes123@gmail.com",
            "password": "pes1234"
        }
        response_login = client.post(url_login, data=login_data, format='json')
        self.assertEqual(response_login.status_code, 200)

        # Create chat
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 201)
        
    def test_update_timestamp(self):
        client =APIClient()
        url = reverse('chats-view')
        url_login = reverse('login')
        data  = {
            "id_chat" : "4Pqs1Wa0u3dMIx1HQpWd"
        }
        login_data = {
            "email": "pes123@gmail.com",
            "password": "pes1234"
        }
        response_login = client.post(url_login, data=login_data, format='json')
        self.assertEqual(response_login.status_code, 200)
        response = client.put(url,data=data,format='json')
        self.assertEqual(response.status_code,200)

    def get_chats_user(self):
        client = APIClient()
        url = reverse('chats-view')
        url_login = reverse('login')

        login_data = {
            "email": "pes123@gmail.com",
            "password": "pes1234"
        }
        response_login = client.post(url_login, data=login_data, format='json')
        self.assertEqual(response_login.status_code, 200)
        response = client.get(url)
        self.assertEqual(response.status_code,200)
