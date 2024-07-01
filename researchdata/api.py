from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from collections import OrderedDict

@csrf_exempt
def check(request):
    return HttpResponse(status=200)

@api_view(['GET'])
def user(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_user = UserSerializer(user)
    combined_data = {"user": serialized_user.data}

    if request.path.endswith("/full"):
        try:
            personality = Personality.objects.get(user_id=user_id)
        except Personality.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_personality = PersonalitySerializer(personality)
        combined_data["personality"] = serialized_personality.data

    return Response(combined_data)

@api_view(['GET'])
def post(request, post_id):
    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_post = PostSerializer(post)
    combined_data = {"post": serialized_post.data}

    if request.path.endswith("/full"):
        true_assumption_responses = User_Response.objects.filter(post_id=post_id, assumption="True")
        false_assumption_responses = User_Response.objects.filter(post_id=post_id, assumption="False")
        questionable_assumption_responses = User_Response.objects.filter(post_id=post_id, assumption="questionable")

        # Extract user IDs of those who assumed the post is true, false and questionable
        true_assumption_user_ids = true_assumption_responses.values_list('user_id', flat=True)
        false_assumption_user_ids = false_assumption_responses.values_list('user_id', flat=True)
        questionable_assumption_user_ids = questionable_assumption_responses.values_list('user_id', flat=True)
        response_amount = len(true_assumption_user_ids) + len(false_assumption_user_ids) + len(questionable_assumption_user_ids)
        combined_data['total_response_amount'] = response_amount
        combined_data['true_assumption_user_ids'] = list(true_assumption_user_ids)
        combined_data['false_assumption_user_ids'] = list(false_assumption_user_ids)
        combined_data['questionable_assumption_user_ids'] = list(questionable_assumption_user_ids)

        serialized_true_assumption_responses = UserResponseSerializer(true_assumption_responses, many=True)
        serialized_false_assumption_responses = UserResponseSerializer(false_assumption_responses, many=True)
        serialized_questionable_assumption_responses = UserResponseSerializer(questionable_assumption_responses, many=True)
        combined_data['true_assumption_responses'] = serialized_true_assumption_responses.data
        combined_data['false_assumption_responses'] = serialized_false_assumption_responses.data
        combined_data['questionable_assumption_responses'] = serialized_questionable_assumption_responses.data

    return Response(combined_data)

@api_view(['GET'])
def user_responses(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        responses = User_Response.objects.filter(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_user = UserSerializer(user)
    serialized_responses = UserResponseSerializer(responses, many=True)
    combined_data = {"user": serialized_user.data,
                     'responses': serialized_responses.data}

    return Response(combined_data)

@api_view(['GET'])
def variable(request, name=None):
    if name is None:
        variables = Variable.objects.all()
        serialized_variables = VariableSerializer(variables, many=True)
        return Response(serialized_variables.data)
    try:
        variable = Variable.objects.get(name=name)
    except Variable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_variable = VariableSerializer(variable)
    return Response(serialized_variable.data)

@api_view(['GET'])
def users_ranked(request):
    users = User.objects.all()
    user_data_list = []
    for user in users:
        user_data = {
            "user": UserSerializer(user).data,
            "correct_responses": len(User_Response.objects.filter(user_id=user.user_id, correctness=True))
        }
        user_data_list.append(user_data)

    user_data_list.sort(key=lambda x: x['correct_responses'], reverse=True)
    json = OrderedDict()
    for index, user_data in enumerate(user_data_list):
        json[index] = user_data

    return Response(json)

@api_view(['GET', 'POST'])
def create_user(request):
    if request.method == 'POST':
        try:
            user_data = request.data['user']
        except KeyError:
            return create_only_personality(request)

        try:
            personality_data = request.data['personality']
        except KeyError:
            return create_only_user(user_data)

        return create_user_and_personality(user_data, personality_data)

    return Response(status=status.HTTP_200_OK)


def create_only_personality(request):
    try:
        personality_data = request.data['personality']
    except KeyError:
        return Response({
            'error': "personality section does not exist"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(user_id=personality_data['user'])
    except User.DoesNotExist:
        return Response({
            'error': "no user by that id",
            'personality': personality_data
        }, status=status.HTTP_400_BAD_REQUEST)

    serialized_personality = PersonalitySerializer(data=personality_data)
    if serialized_personality.is_valid():
        try:
            Personality.objects.get(user=personality_data['user'])
        except Personality.DoesNotExist:
            serialized_personality.save()

            return Response({
                'personality': personality_data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": "personality for this user already exist",
            'personality': personality_data
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'error': "personality data is not valid",
            'personality': personality_data
        }, status=status.HTTP_400_BAD_REQUEST)

def create_only_user(user_data):
    serialized_user = UserSerializer(data=user_data)
    if serialized_user.is_valid():
        serialized_user.save()

        return Response({
            'user': user_data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'error': "user data is not valid",
            'user': user_data
        }, status=status.HTTP_400_BAD_REQUEST)

def create_user_and_personality(user_data, personality_data):
    serialized_user = UserSerializer(data=user_data)
    if not serialized_user.is_valid():
        return Response({
            'error': "user data is not valid",
            'user': user_data
        }, status=status.HTTP_400_BAD_REQUEST)

    user_instance = serialized_user.save()
    personality_data['user'] = user_instance.user_id

    serialized_personality = PersonalitySerializer(data=personality_data)
    if not serialized_personality.is_valid():
        user_instance.delete()
        return Response({
            'error': "personality data is not valid",
            'personality': personality_data
        }, status=status.HTTP_400_BAD_REQUEST)

    serialized_personality.save()

    return Response({
        'user': user_data,
        'personality': personality_data
    }, status=status.HTTP_201_CREATED)
