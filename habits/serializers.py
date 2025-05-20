from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Habit


# Сериализатор для модели Habit
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant', 'related_habit',
            'periodicity', 'reward', 'duration', 'is_public'
        ]
        read_only_fields = ['user']

    def validate(self, data):
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Cannot set both reward and related habit.")
        if data.get('duration', 0) > 120:
            raise serializers.ValidationError("Duration cannot exceed 120 seconds.")
        if data.get('periodicity', 1) > 7:
            raise serializers.ValidationError("Periodicity cannot be more than 7 days.")
        if data.get('is_pleasant'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError("Pleasant habit cannot have reward or related habit.")
        if data.get('related_habit') and not data.get('related_habit').is_pleasant:
            raise serializers.ValidationError("Related habit must be pleasant.")
        return data


# Сериализаторы для регистрации и авторизации пользователей
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return data
