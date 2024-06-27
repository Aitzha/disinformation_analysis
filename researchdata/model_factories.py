import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    user_id = 0
    gender = "female"
    birth_year = 2000
    ethnicity = "white"
    parent_edu = "advanced degree"

    class Meta:
        model = User

class PersonalityFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    mac1 = mac2 = mac3 = mac4 = mac5 = mac6 = mac7 = mac8 = mac9 = mac10 = mac11 = 0
    smds1 = smds2 = smds3 = smds4 = smds5 = smds6 = smds7 = smds8 = smds9 = smds10 = smds11 = smds12 = 0
    risk1 = risk2 = risk3 = risk4 = risk5 = risk6 = risk7 = 0
    class Meta:
        model = Personality

class PostFactory(factory.django.DjangoModelFactory):
    post_id = 0
    name = "Example post name"
    nature = True

    class Meta:
        model = Post

class ResponseFactory(factory.django.DjangoModelFactory):
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    reason = "Some reason"
    generalized_reason = "Seems legit"
    assumption = "True"
    correctness = True

    class Meta:
        model = User_Response