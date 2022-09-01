from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import User




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class GetTokenSerializer(serializers.Serializer):
    """ Сериалайзер для обработки данных при получении токена """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True) 


class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для обработки данных при создании юзера """

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Username не может быть me')
        return value 
