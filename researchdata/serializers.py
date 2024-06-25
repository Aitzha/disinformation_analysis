from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "gender", "birth_year", "ethnicity", "parent_edu"]


class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = ["user_id", "mac1", "mac2", "mac3", "mac4"]