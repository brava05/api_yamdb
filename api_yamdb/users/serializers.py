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
    username_field = get_user_model().USERNAME_FIELD
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):

        user = get_object_or_404(User, username=attrs['username'])
        db_confirmation_code = user.confirmation_code
        provided_confirmation_code = self.initial_data.get('confirmation_code')
        if db_confirmation_code != provided_confirmation_code:
            raise serializers.ValidationError(
                "Пожалуйста, введите корректный confirmation_code"
            )

        token = self.get_token(user)
        data = OrderedDict()
        data["token"] = str(token)
        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class UserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для обработки данных при создании юзера """
    def create(self, validated_data):

        if "role" not in validated_data:
            return User.objects.create(role="user", **validated_data)
        else:
            return User.objects.create(**validated_data)

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
