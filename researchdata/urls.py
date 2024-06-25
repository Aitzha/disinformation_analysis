from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('api/', api.check, name='check_api'),
    path('api/user/<int:user_id>', api.user_info, name='user_info_api')
]