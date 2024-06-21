import json
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from rest_framework.test import APIRequestFactory, APITestCase

class ResearchTest(APITestCase):
    def test_checkAPI_returnSuccess(self):
        url = reverse('check_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)