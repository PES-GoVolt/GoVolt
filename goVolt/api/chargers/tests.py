from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

class ChargerLocationApiViewTest(TestCase):
    def test_charger_location_view(self):
        client = APIClient()
        url = reverse('chargers-loc') 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChargerDataBaseApiViewTest(TestCase):
    def test_charger_data_base_view(self):
        client = APIClient()
        url = reverse('chargers-database')
        response = client.post(url)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
