"""Users serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
from django.core import validators
from django.core.validators import RegexValidator, FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password

import re
from itertools import cycle

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Models
from users.models import User


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     pass


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class UserSignUpSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=4, max_length=64)
    password_confirmation = serializers.CharField(min_length=4, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=100)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user



class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
