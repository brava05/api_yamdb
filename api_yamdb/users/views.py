from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, GetTokenSerializer
from rest_framework import generics

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (TokenObtainSlidingView,)


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

