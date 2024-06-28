from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "gender", "birth_year", "ethnicity", "parent_edu"]


class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = ["user_id", "mac1", "mac2", "mac3", "mac4", "mac5", "mac6", "mac7", "mac8", "mac9", "mac10", "mac11",
                  "smds1", "smds2", "smds3", "smds4", "smds5", "smds6", "smds7", "smds8", "smds9", "smds10", "smds11", "smds12",
                  "risk1", "risk2", "risk3", "risk4", "risk5", "risk6", "risk7"]


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Response
        fields = ["post_id", "user_id", "reason", "generalized_reason", "assumption", "correctness"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["post_id", "name", "nature"]


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ["name", "description", "range"]