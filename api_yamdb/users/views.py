from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import User
from .serializers import (
    UserSerializer,
    GetTokenSerializer,
    ProfileSerializer,
    UserByAdminSerializer
)

from rest_framework import generics

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (TokenObtainSlidingView,)

from rest_framework import serializers


class UserCreateViewSet(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        confirmation_code = get_random_string(length=32)

        send_mail(
            'Confirmation_code',
            f'Ваш код для завершения регистрации:  {confirmation_code}',
            'from@example.com',
            [request.data.get('email')],
            fail_silently=False,
        )
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=confirmation_code, role='user')

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetTokenView(TokenObtainSlidingView):
    serializer_class = GetTokenSerializer


class ProfileView(APIView):
    def get(self, request):
        request_username = request.data.get('username')
        user = get_object_or_404(User, username=request_username)
        serializer = ProfileSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        request_username = request.data.get('username')
        user = get_object_or_404(User, username=request_username)
        print(user)
        serializer = ProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)


class UserCreateByAdminView(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserByAdminSerializer
    queryset = User.objects.all()

    def post(self, request):
        request_author = self.request.user

        # request_username = request.data.get('username')
        # print(f'zdes request_username - {request_username}')
        # user = get_object_or_404(User, username=request_username)

        if request_author.role != "admin":
            raise serializers.ValidationError(
                "У Вас нет прав на создание пользователей!"
            )

        data = request.data
        print(f'date = {data}')
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
