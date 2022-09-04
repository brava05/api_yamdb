from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Review, Category, Title
from api_yamdb.settings import EMAIL_BACKEND
from users.models import User
from .serializers import (GetTokenSerializer, ReviewSerializer,
                          CommentSerializer, CategorySerializer,
                          TitleSerializer, TitleReadSerializer,
                          GenreSerializer, UserSerializer,)
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorAdminModeratorOrReadAndPost,
                          AdminOnly)
from ..filters import TitleFilter


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Общий класс микинов для наследования
    вьюсетов CategoryViewSet и GenreViewSet.
    """
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Review
    для реализации CRUD-операций со списками всех отзывов.
    Права доступа: Доступно без токена.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadAndPost,
        IsAuthenticatedOrReadOnly,
    )
    throttle_classes = (AnonRateThrottle,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Comment
    для реализации CRUD-операций c комментариями к отзывам по id.
    """
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadAndPost,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   title__id=self.kwargs.get('title_id'),
                                   id=self.kwargs.get('review_id')
                                   )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get('title_id')
        )
        serializer.save(review=review, author=self.request.user)


class CategoryViewSet(CreateListViewSet):
    """
    Вьюсет для модели Category.
    Получение списка всех категорий.
    Права доступа: Доступно без токена.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = "slug"


class GenreViewSet(CreateListViewSet):
    """
    Вьюсет для модели Genre.
    Получение списка всех жанров.
    Права доступа: Доступно без токена.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех произведений.
    Права доступа: Доступно без токена.
    """
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")
    ).order_by("id")
    serializer_class = TitleSerializer

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleReadSerializer


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

        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )

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


@api_view(['POST', ])
@permission_classes([AllowAny])
def get_token_view(request):
    serializer = GetTokenSerializer(data=request.data)
    username = request.data.get("username")
    confirmation_code = request.data.get("confirmation_code")

    if serializer.is_valid(raise_exception=True):
        try:
            user = get_object_or_404(User, username=username)
        except Exception:
            return Response(
                "Пользователя с таким именем не существует",
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.confirmation_code != confirmation_code:
        return Response(
            "Пожалуйста, введите корректный код",
            status=status.HTTP_400_BAD_REQUEST
        )

    data = get_tokens_for_user(user)
    return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, AdminOnly,)

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        if request.method == "GET":
            serializer = UserSerializer(self.request.user, many=False)
            return Response(serializer.data)

        serializer = UserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=True):
            if self.request.user.role == User.ADMINISTRATOR:
                serializer.save()
            else:
                serializer.save(role=self.request.user.role)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
