from api.permissions import AdminOnly

from django.core.mail import send_mail

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import User
from .serializers import (
    GetTokenSerializer,
    ProfileSerializer,
    UserSerializer,
)

from api_yamdb.settings import EMAIL_BACKEND

from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator 


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
        email = user.get('email')

        user = User.objects.get_or_create(
            username=username,
            email=email,
        )[0]

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation_code',
            f'Ваш код для завершения регистрации:  {confirmation_code}',
            EMAIL_BACKEND,
            [request.data.get('email')],
            fail_silently=False,
        )
        user.confirmation_code = confirmation_code
        user.save()

        return Response(request.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }


@api_view(['POST',])
@permission_classes([AllowAny])
def GetTokenView(request):
    serializer = GetTokenSerializer(data=request.data)
    username = request.data.get("username")
    confirmation_code = request.data.get("confirmation_code") 

    if serializer.is_valid():
        try:
            user = User.objects.get(username=username)
        except Exception:
            return Response("Пользователя с таким именем не существует", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    db_confirmation_code = user.confirmation_code
    if db_confirmation_code != confirmation_code:
        return Response("Пожалуйста, введите корректный код", status=status.HTTP_400_BAD_REQUEST)
    else:
        data = get_tokens_for_user(user)

        return Response(data)


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
