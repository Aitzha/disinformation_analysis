from django.urls import reverse

from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

user_data = {
    "user_id": 1,
    "gender": "female",
    "birth_year": 1997,
    "ethnicity": "white",
    "parent_edu": "high school/GED"
}

invalid_user_data = {
    "user_id": 1
}

personality_data = {
    "user": 1,
    "mac1": 5,
    "mac2": 4,
    "mac3": 1,
    "mac4": 2,
    "mac5": 3,
    "mac6": 2,
    "mac7": 2,
    "mac8": 2,
    "mac9": 3,
    "mac10": 1,
    "mac11": 1,
    "smds1": 2,
    "smds2": 3,
    "smds3": 2,
    "smds4": 4,
    "smds5": 4,
    "smds6": 5,
    "smds7": 5,
    "smds8": 2,
    "smds9": 3,
    "smds10": 3,
    "smds11": 4,
    "smds12": 4,
    "risk1": 9,
    "risk2": 7,
    "risk3": 8,
    "risk4": 2,
    "risk5": 8,
    "risk6": 3,
    "risk7": 1
}

invalid_personality_data = {
    "user": 1
}

full_user_data = {
    "user": user_data,
    "personality": personality_data
}

full_user_data_with_invalid_user = {
    "user": invalid_user_data,
    "personality": personality_data
}

full_user_data_with_invalid_personality = {
    "user": user_data,
    "personality": invalid_personality_data
}


class CheckAPITests(APITestCase):
    def test_checkAPI_returnSuccess(self):
        url = reverse('check_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class FullUserAPITests(APITestCase):
    def test_userAndPersonalityExist_returnSuccess(self):
        user = UserFactory.create()
        PersonalityFactory.create(user=user)
        url = reverse('full_user_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)

    def test_noUserExist_returnNotFound(self):
        url = reverse('full_user_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_noPersonalityExist_returnNotFound(self):
        user = UserFactory.create()
        url = reverse('full_user_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnMethodNotAllowed(self):
        url = reverse('full_user_api', kwargs={'user_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class FullPostAPITests(APITestCase):
    def test_postExistAndNoResponse_returnCorrectPost(self):
        post = PostFactory.create()
        url = reverse('full_post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 0)

    def test_postExistAndTwoResponses_returnCorrectJson(self):
        user1 = UserFactory.create(user_id=1)
        user2 = UserFactory.create(user_id=2)
        post = PostFactory.create()
        ResponseFactory.create(user=user1, post=post, assumption="True")
        ResponseFactory.create(user=user2, post=post, assumption="False")
        url = reverse('full_post_api', kwargs={'post_id': post.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['post']['post_id'], post.post_id)
        self.assertEqual(response_data['total_response_amount'], 2)
        self.assertEqual(len(response_data['true_assumption_user_ids']), 1)
        self.assertEqual(len(response_data['false_assumption_user_ids']), 1)
        self.assertEqual(len(response_data['questionable_assumption_user_ids']), 0)
        self.assertEqual(len(response_data['true_assumption_responses']), 1)
        self.assertEqual(len(response_data['false_assumption_responses']), 1)
        self.assertEqual(len(response_data['questionable_assumption_responses']), 0)

    def test_noPostExist_returnNotFound(self):
        url = reverse('full_post_api', kwargs={'post_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnMethodNotAllowed(self):
        url = reverse('full_post_api', kwargs={'post_id': 0})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class FullUserResponseAPITests(APITestCase):
    def test_userExistAndZeroResponses_returnSuccess(self):
        user = UserFactory.create()
        url = reverse('full_user_response_api', kwargs={'user_id': user.user_id})
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
        url = reverse('full_user_response_api', kwargs={'user_id': user.user_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user.user_id)
        self.assertEqual(len(response_data['responses']), 2)

    def test_noUserExist_returnNotFound(self):
        url = reverse('full_user_response_api', kwargs={'user_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_sendPostRequest_returnNotFound(self):
        url = reverse('full_user_response_api', kwargs={'user_id': 0})
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


class RankedUsersAPITests(APITestCase):
    def test_noUsersExist_returnEmptyJson(self):
        url = reverse('users_ranked_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_twoUsersExist_returnCorrectJson(self):
        UserFactory.create(user_id=0)
        user = UserFactory.create(user_id=1)
        post = PostFactory.create()
        ResponseFactory.create(user=user, post=post)
        url = reverse('users_ranked_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data['0']['user']['user_id'], 1)
        self.assertEqual(response_data['1']['user']['user_id'], 0)

    def test_sendPostRequest_returnMethodNotAllowed(self):
        url = reverse('users_ranked_api')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class CreateUserAPITests(APITestCase):
    def test_sendValidUserData_returnCreated(self):
        url = reverse('create_user_api')
        response = self.client.post(url, {"user": user_data}, format='json')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], user_data["user_id"])

        try:
            User.objects.get(user_id=user_data["user_id"])
        except User.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(1, 1)

    def test_sendInvalidUserData_returnBadRequest(self):
        url = reverse('create_user_api')
        response = self.client.post(url, {"user": invalid_user_data}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_sendNoUserData_returnBadRequest(self):
        url = reverse('create_user_api')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 400)

    def test_sendValidPersonalityDataAndUserExist_returnCreated(self):
        UserFactory.create(user_id=user_data["user_id"])
        url = reverse('create_user_api')
        response = self.client.post(url, {"personality": personality_data}, format='json')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['personality']['user'], personality_data["user"])

        try:
            Personality.objects.get(user=user_data["user_id"])
        except Personality.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(1, 1)

    def test_sendValidPersonalityDataAndNoUserExist_returnBadRequest(self):
        url = reverse('create_user_api')
        response = self.client.post(url, {"personality": personality_data}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_sendInvalidPersonalityData_returnBadRequest(self):
        url = reverse('create_user_api')
        response = self.client.post(url, {"personality": personality_data}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_sendValidFullUserData_returnCreated(self):
        url = reverse('create_user_api')
        response = self.client.post(url, full_user_data, format='json')
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['user']['user_id'], full_user_data["user"]['user_id'])
        self.assertEqual(response_data['personality']['user'], full_user_data["personality"]['user'])

        try:
            User.objects.get(user_id=user_data["user_id"])
            Personality.objects.get(user=user_data["user_id"])
        except User.DoesNotExist:
            self.assertEqual(1, 2)
        except Personality.DoesNotExist:
            self.assertEqual(1, 2)
        self.assertEqual(1, 1)

    def test_sendInvalidUserAndValidPersonality_returnBadRequest(self):
        url = reverse('create_user_api')
        response = self.client.post(url, full_user_data_with_invalid_user, format='json')
        self.assertEqual(response.status_code, 400)

    def test_sendValidUserAndInvalidPersonality_returnBadRequest(self):
        url = reverse('create_user_api')
        response = self.client.post(url, full_user_data_with_invalid_personality, format='json')
        self.assertEqual(response.status_code, 400)