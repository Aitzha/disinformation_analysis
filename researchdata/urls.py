from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('api/', api.check, name='check_api'),
    path('api/simple/user/<int:user_id>', api.simple_user_info, name='simple_user_info_api'),
    path('api/simple/user_response/<int:user_id>', api.simple_user_responses, name='simple_user_response_api'),
    path('api/simple/post/<int:post_id>', api.simple_post_info, name='simple_post_info_api'),
    path('api/user/<int:user_id>', api.user_info, name='user_info_api'),
    path('api/user_response/<int:user_id>', api.user_responses, name='user_response_api'),
    path('api/post/<int:post_id>', api.post_info, name='post_info_api'),
    path('api/detailed/post/<int:post_id>', api.detailed_post_info, name='detailed_post_info_api'),
    path('api/ranked/users', api.users_ranked, name='users_ranked_api'),
]