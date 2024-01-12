from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


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

class NearestChargerApiViewTestCase(TestCase):
    def test_nearest_chargers(self):
        client = APIClient()
        url = reverse('chargers-nearest')

        data = {
            'longitud': 41.389498,
            'latitud': 2.110234
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class GetChargerInfoApiView(TestCase):
    def test_get_charger_by_id(self):
        charger_id = "44182248"

        client = APIClient()
        url = reverse('charger-detail', args=[charger_id])

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        charger = response.data
        self.assertEqual(charger['charger_id'], "44182248")