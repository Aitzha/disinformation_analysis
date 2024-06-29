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

@api_view(['GET', 'POST'])
def simple_user(request, user_id):
    if request.method == 'POST':
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        return Response(serialized_user.data, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_user = UserSerializer(user)
    return Response(serialized_user.data)

@api_view(['GET'])
def simple_user_responses(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        responses = User_Response.objects.filter(user=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_responses = UserResponseSerializer(responses, many=True)
    return Response(serialized_responses.data)


@api_view(['GET', 'POST'])
def user(request, user_id):
    if request.method == 'POST':
        try:
            user_data = request.data['user']
            personality_data = request.data['personality']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Serialize user data
        serialized_user = UserSerializer(data=user_data)
        if serialized_user.is_valid():
            # Save the User instance
            user_instance = serialized_user.save()

            # Set the user field in personality data to the created user instance
            personality_data['user'] = user_instance.user_id
            serialized_personality = PersonalitySerializer(data=personality_data)

            if serialized_personality.is_valid():
                # Save the Personality instance
                serialized_personality.save()

                return Response({
                    'user': serialized_user.data,
                    'personality': serialized_personality.data
                }, status=status.HTTP_201_CREATED)
            else:
                # Handle invalid personality data
                user_instance.delete()
                return Response(serialized_personality.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle invalid user data
            return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(user_id=user_id)
        personality = Personality.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Personality.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_user = UserSerializer(user)
    serialized_personality = PersonalitySerializer(personality)
    combined_data = {"user": serialized_user.data,
                     "personality": serialized_personality.data}

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
                     "responses": serialized_responses.data}

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