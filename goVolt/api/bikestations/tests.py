from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class BikestationsLocationApiViewTest(TestCase):
    def test_bikestations_location_view(self):
        client = APIClient()
        url = reverse('bikestations-loc') 
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BikestationsDataBaseApiViewTest(TestCase):
    def test_bikestations_data_base_view(self):
        client = APIClient()
        url = reverse('bikestations-database')
        response = client.post(url)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
