from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

@csrf_exempt
def check(request):
    return HttpResponse(status=200)

@csrf_exempt
def simple_user_info(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serialized_user = UserSerializer(user)

        return JsonResponse(serialized_user.data)

@csrf_exempt
def simple_user_responses(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        user_responses = Response.objects.filter(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serialized_responses = ResponseSerializer(user_responses, many=True)

        return JsonResponse(serialized_responses.data, safe=False)

@csrf_exempt
def user_info(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        personality = Personality.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    except Personality.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serialized_user = UserSerializer(user)
        serialized_personality = PersonalitySerializer(personality)

        combined_data = {"user": serialized_user.data,
                         "personality": serialized_personality.data}

        return JsonResponse(combined_data)