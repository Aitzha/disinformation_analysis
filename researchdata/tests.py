from django.urls import reverse

from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

simple_user_data = {
        "user_id": 1,
        "gender": "female",
        "birth_year": 1997,
        "ethnicity": "white",
        "parent_edu": "high school/GED"
    }

user_data = {

}

class CheckAPITests(APITestCase):
    def test_checkAPI_returnSuccess(self):
        url = reverse('check_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SimpleUserAPITests(APITestCase):
    def test_userExist_returnCorrectUser(self):
        user = UserFactory.create()
        url = reverse('simple_user_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user_id'], user.user_id)

    def test_userDoNotExist_returnNotFound(self):
        url = reverse('simple_user_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendValidData_returnCreated(self):
        url = reverse('simple_user_api', kwargs={'user_id': 0})
        response = self.client.post(url, simple_user_data, format='json')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['user_id'], simple_user_data["user_id"])

        try:
            User.objects.get(user_id=simple_user_data["user_id"])
        except User.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(1, 1)

    def test_sendInvalidData_returnBadRequest(self):
        url = reverse('simple_user_api', kwargs={'user_id': 0})
        data = {
            'invalidField': 0,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)


class SimpleUserResponseAPITests(APITestCase):
    def test_userExistAndZeroResponses_returnEmptyList(self):
        user = UserFactory.create()
        url = reverse('simple_user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_userExistAndTwoResponses_returnTwoResponses(self):
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

    def test_userDoNotExist_returnNotFound(self):
        url = reverse('simple_user_response_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('simple_user_response_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class SimplePostAPITests(APITestCase):
    def test_userExist_returnSuccess(self):
        post = PostFactory.create()
        url = reverse('simple_post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post_id'], post.post_id)

    def test_userDoNotExist_returnNotFound(self):
        url = reverse('simple_post_api', kwargs={'post_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('simple_post_api', kwargs={'post_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class UserAPITests(APITestCase):
    def test_userAndPersonalityExist_returnSuccess(self):
        user = UserFactory.create()
        PersonalityFactory.create(user=user)
        url = reverse('user_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)

    def test_userDoNotExist_returnNotFound(self):
        url = reverse('user_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_personalityDoNotExist_returnNotFound(self):
        user = UserFactory.create()
        url = reverse('user_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('user_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class UserResponseAPITests(APITestCase):
    def test_userExistAndZeroResponses_returnSuccess(self):
        user = UserFactory.create()
        url = reverse('user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)
        self.assertEqual(len(response_data['responses']), 0)

    def test_userExistAndTwoResponses_returnSuccess(self):
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

    def test_userDoNotExist_returnNotFound(self):
        url = reverse('user_response_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('user_response_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class PostAPITests(APITestCase):
    def test_postExistAndNoResponse_returnSuccess(self):
        post = PostFactory.create()
        url = reverse('post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 0)

    def test_postExistAndTwoResponses_returnSuccess(self):
        user = UserFactory.create()
        post = PostFactory.create()
        ResponseFactory.create(user=user, post=post)
        ResponseFactory.create(user=user, post=post)
        url = reverse('post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 2)

    def test_postDoNotExist_returnNotFound(self):
        url = reverse('post_api', kwargs={'post_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('post_api', kwargs={'post_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class VariableAPITests(APITestCase):
    def test_variableExist_returnCorrectVariable(self):
        variable = VariableFactory.create(name="mac1")
        url = reverse("variable_api", kwargs={'name': variable.name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['name'], variable.name)

    def test_noVariablesExist_return404(self):
        url = reverse("variable_api", kwargs={'name': 'mac1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('variable_api', kwargs={'name': 'mac1'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class AllVariableAPITests(APITestCase):
    def test_noVariablesExist_returnEmptyList(self):
        url = reverse("all_variable_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_twoVariablesExist_returnTwoVariables(self):
        VariableFactory.create(name="mac1")
        VariableFactory.create(name="mac2")
        url = reverse("all_variable_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], "mac1")
        self.assertEqual(response_data[1]['name'], "mac2")

    def test_sendPostRequest_return405(self):
        url = reverse("all_variable_api")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class DetailedPostAPITests(APITestCase):
    def test_postExistAndNoResponse_returnSuccess(self):
        post = PostFactory.create()
        url = reverse('detailed_post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 0)

    def test_postExistAndTwoResponses_returnSuccess(self):
        user = UserFactory.create()
        post = PostFactory.create()
        ResponseFactory.create(user=user, post=post)
        ResponseFactory.create(user=user, post=post)
        url = reverse('detailed_post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 2)

    def test_postDoNotExist_returnNotFound(self):
        url = reverse('detailed_post_api', kwargs={'post_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('detailed_post_api', kwargs={'post_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class RankedUsersAPITests(APITestCase):
    def test_noUsersExist_returnSuccess(self):
        url = reverse('users_ranked_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_twoUsersExist_returnSuccess(self):
        UserFactory.create(user_id=0)
        UserFactory.create(user_id=1)
        url = reverse('users_ranked_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('users_ranked_api')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

