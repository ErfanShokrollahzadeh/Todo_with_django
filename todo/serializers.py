from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializaer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'