
from api.permissions import AdminOnly

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from .models import User
from .serializers import (
    GetTokenSerializer,
    ProfileSerializer,
    UserSerializer,
)


class UserCreateViewSet(generics.CreateAPIView):
    """ Вьюкласс создания нового пользователя auth/signup/ """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        username = user.get('username')
        if username == 'me':
            return Response(
                "username не может быть me",
                status=status.HTTP_400_BAD_REQUEST
            )

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


class GetTokenView(TokenObtainPairView):
    """ Вьюсет получения токена auth/token/ """
    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)


class ProfileView(APIView):
    """ Вьюсет для доступа к своему профилю v1/users/me/"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        serializer = ProfileSerializer(self.request.user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        requested_user = self.request.user

        serializer = ProfileSerializer(
            requested_user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            if requested_user.role == 'admin':
                serializer.save()
            else:
                serializer.save(role=requested_user.role)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Общий вьюсет для модели User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, AdminOnly,)
