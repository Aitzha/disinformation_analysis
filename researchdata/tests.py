import json
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from rest_framework.test import APIRequestFactory, APITestCase

from .model_factories import *
from .serializers import *

class ResearchTest(APITestCase):
    def test_checkAPI_returnSuccess(self):
        url = reverse('check_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_UserInfoAPI_returnSuccess(self):
        user = UserFactory.create()
        personality = PersonalityFactory.create(user_id=user)
        url = reverse('user_info_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_UserInfoAPI_returnNotFound(self):
        user = UserFactory.create()
        personality = PersonalityFactory.create(user_id=user)
        url = reverse('user_info_api', kwargs={'user_id': user.user_id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_UserInfoAPI_returnUser(self):
        user = UserFactory.create()
        personality = PersonalityFactory.create(user_id=user)
        url = reverse('user_info_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)