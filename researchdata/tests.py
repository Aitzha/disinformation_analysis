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

    def test_userInfoAPI_userAndPersonalityExist_returnSuccess(self):
        user = UserFactory.create()
        personality = PersonalityFactory.create(user=user)
        url = reverse('user_info_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)

    def test_userInfoAPI_userDoNotExist_returnNotFound(self):
        url = reverse('user_info_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_userInfoAPI_personalityDoNotExist_returnNotFound(self):
        user = UserFactory.create()
        url = reverse('user_info_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_userSimpleInfoAPI_userExist_returnSuccess(self):
        user = UserFactory.create()
        url = reverse('simple_user_info_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user_id'], user.user_id)

    def test_userSimpleInfoAPI_userDoNotExist_returnNotFound(self):
        url = reverse('simple_user_info_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

