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
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    serialized_user = UserSerializer(user)
    return JsonResponse(serialized_user.data)

@csrf_exempt
def simple_user_responses(request, user_id):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        user = User.objects.get(user_id=user_id)
        responses = Response.objects.filter(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    serialized_responses = ResponseSerializer(responses, many=True)
    return JsonResponse(serialized_responses.data, safe=False)

@csrf_exempt
def simple_post_info(request, post_id):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post)
    return JsonResponse(serialized_post.data)


@csrf_exempt
def user_info(request, user_id):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        user = User.objects.get(user_id=user_id)
        personality = Personality.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    except Personality.DoesNotExist:
        return HttpResponse(status=404)

    serialized_user = UserSerializer(user)
    serialized_personality = PersonalitySerializer(personality)
    combined_data = {"user": serialized_user.data,
                     "personality": serialized_personality.data}

    return JsonResponse(combined_data)

@csrf_exempt
def user_responses(request, user_id):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        user = User.objects.get(user_id=user_id)
        responses = Response.objects.filter(user_id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    serialized_user = UserSerializer(user)
    serialized_responses = ResponseSerializer(responses, many=True)
    combined_data = {"user": serialized_user.data,
                     "responses": serialized_responses.data}

    return JsonResponse(combined_data)

@csrf_exempt
def post_info(request, post_id):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        post = Post.objects.get(post_id=post_id)
        true_assumption_responses = Response.objects.filter(post_id=post_id, post_status_opinion="True")
        false_assumption_responses = Response.objects.filter(post_id=post_id, post_status_opinion="False")
        questionable_assumption_responses = Response.objects.filter(post_id=post_id, post_status_opinion="dont know")
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post)

    # Extract user IDs of those who assumed the post is true, false and questionable
    true_assumption_user_ids = true_assumption_responses.values_list('user_id', flat=True)
    false_assumption_user_ids = false_assumption_responses.values_list('user_id', flat=True)
    questionable_assumption_user_ids = questionable_assumption_responses.values_list('user_id', flat=True)
    response_amount = len(true_assumption_user_ids) + len(false_assumption_user_ids) + len(questionable_assumption_user_ids)

    combined_data = {"post": serialized_post.data,
                     "total_response_amount": response_amount,
                     "true_assumption_user_ids": list(true_assumption_user_ids),
                     "false_assumption_user_ids": list(false_assumption_user_ids),
                     "questionable_assumption_user_ids": list(questionable_assumption_user_ids)}

    return JsonResponse(combined_data)

@csrf_exempt
def detailed_post_info(request, post_id):
    if request.method != "GET":
        return HttpResponse(status=405)

    try:
        post = Post.objects.get(post_id=post_id)
        true_assumption_responses = Response.objects.filter(post_id=post_id, post_status_opinion="True")
        false_assumption_responses = Response.objects.filter(post_id=post_id, post_status_opinion="False")
        questionable_assumption_responses = Response.objects.filter(post_id=post_id, post_status_opinion="dont know")
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post)
    serialized_true_assumption_responses = ResponseSerializer(true_assumption_responses, many=True)
    serialized_false_assumption_responses = ResponseSerializer(false_assumption_responses, many=True)
    serialized_questionable_assumption_responses = ResponseSerializer(questionable_assumption_responses, many=True)

    # Extract user IDs of those who assumed the post is true, false and questionable
    true_assumption_user_ids = true_assumption_responses.values_list('user_id', flat=True)
    false_assumption_user_ids = false_assumption_responses.values_list('user_id', flat=True)
    questionable_assumption_user_ids = questionable_assumption_responses.values_list('user_id', flat=True)
    response_amount = len(true_assumption_user_ids) + len(false_assumption_user_ids) + len(questionable_assumption_user_ids)

    combined_data = {"post": serialized_post.data,
                     "total_response_amount": response_amount,
                     "true_assumption_user_ids": list(true_assumption_user_ids),
                     "false_assumption_user_ids": list(false_assumption_user_ids),
                     "questionable_assumption_user_ids": list(questionable_assumption_user_ids),
                     "true_assumption_responses": serialized_true_assumption_responses.data,
                     "false_assumption_responses": serialized_false_assumption_responses.data,
                     "questionable_assumption_responses": serialized_questionable_assumption_responses.data}

    return JsonResponse(combined_data)

@csrf_exempt
def users_ranked(request):
    if request.method != "GET":
        return HttpResponse(status=405)

    users = User.objects.all()
    json = {}
    count = 0
    for user in users:
        user_data = {
            "user": UserSerializer(user).data,
            "correct_responses": len(Response.objects.filter(user_id=user.user_id, correctness=True))
        }
        json[count] = user_data
        count += 1

    return JsonResponse(json)