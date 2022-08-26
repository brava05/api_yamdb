from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from rest_framework import filters, mixins, viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .models import User
from .serializers import (
    UserSerializer,
    GetTokenSerializer,
    ProfileSerializer,
    UserByAdminSerializer,
    UserSerializer
)



from api.permissions import AdminOnly

from rest_framework import generics

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import (TokenObtainSlidingView,)

from rest_framework import serializers


class UserCreateViewSet(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        username = user.get('username')
        if username == 'me':
            return Response("username не может быть me", status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = get_random_string(length=32)
        send_mail(
            'Confirmation_code',
            f'Ваш код для завершения регистрации:  {confirmation_code}',
            'from@example.com',
            [request.data.get('email')],
            fail_silently=False,
        )

        serializer.save(confirmation_code=confirmation_code, role='user')

        return Response(request.data, status=status.HTTP_200_OK)


class GetTokenView(TokenObtainSlidingView):
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)


class ProfileView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user

        serializer = ProfileSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        requested_user = self.request.user
        print(requested_user.role)

        serializer = ProfileSerializer(requested_user, data=request.data, partial=True)
        
        if serializer.is_valid():
            if requested_user.role == 'admin':
                serializer.save()
            else:
                serializer.save(role=requested_user.role)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateByAdminView(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserByAdminSerializer
    queryset = User.objects.all()

    def post(self, request):
        request_author = self.request.user


        if request_author.role != "admin":
            raise serializers.ValidationError(
                "У Вас нет прав на создание пользователей!"
            )

        data = request.data
        #print(f'date = {data}')
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')

        return Response(serializer.data, status=status.HTTP_201_CREATED)


#751987
# @list_route(url_path='(?P<username>\w+)')
class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Group"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination 
    permission_classes = (IsAuthenticated, AdminOnly,)
