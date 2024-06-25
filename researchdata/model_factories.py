import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    user_id = 0
    gender = "male"
    birth_year = 2000
    ethnicity = "white"
    parent_edu = "advanced degree"

    class Meta:
        model = User

class PersonalityFactory(factory.django.DjangoModelFactory):
    user_id = factory.SubFactory(UserFactory)
    mac1 = 0
    mac2 = 0
    mac3 = 0
    mac4 = 0
    mac5 = 0
    mac6 = 0
    mac7 = 0
    mac8 = 0
    mac9 = 0
    mac10 = 0
    mac11 = 0
    smds1 = 0
    smds2 = 0
    smds3 = 0
    smds4 = 0
    smds5 = 0
    smds6 = 0
    smds7 = 0
    smds8 = 0
    smds9 = 0
    smds10 = 0
    smds11 = 0
    smds12 = 0
    risk1 = 0
    risk2 = 0
    risk3 = 0
    risk4 = 0
    risk5 = 0
    risk6 = 0
    risk7 = 0
    class Meta:
        model = Personality