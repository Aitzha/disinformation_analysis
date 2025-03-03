from django.urls import path
from . import api

urlpatterns = [
    path('api/', api.check, name='check_api'),

    path('api/user/<int:user_id>', api.user, name='user_api'),
    path('api/user/<int:user_id>/full', api.user, name='full_user_api'),
    path('api/post/<int:post_id>', api.post, name='post_api'),
    path('api/post/<int:post_id>/full', api.post, name='full_post_api'),
    path('api/user_response/<int:user_id>', api.user_responses, name='user_response_api'),
    path('api/variable/<str:name>', api.variable, name='variable_api'),
    path('api/variable', api.variable, name='all_variable_api'),
    path('api/ranked/users', api.users_ranked, name='users_ranked_api'),
    path('api/create/user', api.create_user, name='create_user_api')
]