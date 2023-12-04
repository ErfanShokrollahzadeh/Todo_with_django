from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoSerializaer(serializers.ModelSerializer):
    def validate_priority(self, priority):
        if priority < 10 or priority > 20:
            raise serializers.ValidationError('Priority must be between 10 and 20')
        return priority

    # def validate(self, attrs):
    #     print(attrs)
    #     return super().validate(attrs)

    class Meta:
        model = Todo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializaer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'