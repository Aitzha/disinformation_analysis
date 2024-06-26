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

    def test_simpleUserInfoAPI_userExist_returnSuccess(self):
        user = UserFactory.create()
        url = reverse('simple_user_info_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user_id'], user.user_id)

    def test_simpleUserInfoAPI_userDoNotExist_returnNotFound(self):
        url = reverse('simple_user_info_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_simpleUserInfoAPI_sendPostRequest_returnNotFound(self):
        url = reverse('simple_user_info_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


    def test_simpleUserResponseAPI_userExistAndZeroResponses_returnSuccess(self):
        user = UserFactory.create()
        url = reverse('simple_user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_simpleUserResponseAPI_userExistAndTwoResponses_returnSuccess(self):
        user = UserFactory.create()
        post1 = PostFactory.create(post_id=0)
        post2 = PostFactory.create(post_id=1)
        ResponseFactory.create(user=user, post=post1)
        ResponseFactory.create(user=user, post=post2)
        url = reverse('simple_user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

    def test_simpleUserResponseAPI_userDoNotExist_returnNotFound(self):
        url = reverse('simple_user_response_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_simpleUserResponseAPI_sendPostRequest_returnNotFound(self):
        url = reverse('simple_user_response_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


    def test_simplePostInfoAPI_userExist_returnSuccess(self):
        post = PostFactory.create()
        url = reverse('simple_post_info_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post_id'], post.post_id)

    def test_simplePostInfoAPI_userDoNotExist_returnNotFound(self):
        url = reverse('simple_post_info_api', kwargs={'post_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_simplePostInfoAPI_sendPostRequest_returnNotFound(self):
        url = reverse('simple_post_info_api', kwargs={'post_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


    def test_userInfoAPI_userAndPersonalityExist_returnSuccess(self):
        user = UserFactory.create()
        PersonalityFactory.create(user=user)
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

    def test_userInfoAPI_sendPostRequest_returnNotFound(self):
        url = reverse('user_info_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def test_userResponseAPI_userExistAndZeroResponses_returnSuccess(self):
        user = UserFactory.create()
        url = reverse('user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)
        self.assertEqual(len(response_data['responses']), 0)

    def test_userResponseAPI_userExistAndTwoResponses_returnSuccess(self):
        user = UserFactory.create()
        post1 = PostFactory.create(post_id=0)
        post2 = PostFactory.create(post_id=1)
        ResponseFactory.create(user=user, post=post1)
        ResponseFactory.create(user=user, post=post2)
        url = reverse('user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)
        self.assertEqual(len(response_data['responses']), 2)

    def test_userResponseAPI_userDoNotExist_returnNotFound(self):
        url = reverse('user_response_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_userResponseAPI_sendPostRequest_returnNotFound(self):
        url = reverse('user_response_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def test_postInfoAPI_postExistAndNoResponse_returnSuccess(self):
        post = PostFactory.create()
        url = reverse('post_info_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 0)

    def test_postInfoAPI_postExistAndTwoResponses_returnSuccess(self):
        user = UserFactory.create()
        post = PostFactory.create()
        ResponseFactory.create(user=user, post=post)
        ResponseFactory.create(user=user, post=post)
        url = reverse('post_info_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 2)

    def test_postInfoAPI_postDoNotExist_returnNotFound(self):
        url = reverse('post_info_api', kwargs={'post_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_postInfoAPI_sendPostRequest_returnNotFound(self):
        url = reverse('post_info_api', kwargs={'post_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
