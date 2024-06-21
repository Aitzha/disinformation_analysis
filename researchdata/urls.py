from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    path('api/', api.check, name='check_api'),
]