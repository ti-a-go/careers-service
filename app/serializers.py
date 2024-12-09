from django.contrib.auth.models import Group, User
from rest_framework import serializers

from app.models import CareerModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ListCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerModel
        fields = ["id", "username", "created_datetime", "title", "content"]


class CreateCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerModel
        fields = ["username", "title", "content"]


class UpdateCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerModel
        fields = ["title", "content"]


class DeleteCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerModel
        fields = []
