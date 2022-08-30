from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Genre, Review, Comment, Category, Title
from .serializers import (ReviewSerializer, CommentSerializer,
                          CategorySerializer, TitleSerializer,
                          TitleReadSerializer, GenreSerializer)
from .permissions import (AdminOrReadOnly,
                          AuthorAdminModeratorOrReadAndPost,
                          AdminOrReadOnly_Object)
from .filters import TitleFilter


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Review
    для реализации CRUD-операций со списками всех отзывов.
    Права доступа: Доступно без токена.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadAndPost,)
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
    permission_classes = (AuthorAdminModeratorOrReadAndPost,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return Comment.objects.filter(review=review)

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
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, slug=pk)
        self.perform_destroy(category)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(CreateListViewSet):
    """
    Вьюсет для модели Genre.
    Получение списка всех жанров.
    Права доступа: Доступно без токена.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        queryset = Genre.objects.all()
        genre = get_object_or_404(queryset, slug=kwargs.get("slug"))
        self.perform_destroy(genre)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех произведений.
    Права доступа: Доступно без токена.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    permission_classes = (AdminOrReadOnly_Object,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        slug = self.request.data.get('category')
        category = Category.objects.get(slug=slug)
        return serializer.save(category=category)

    def perform_update(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        return serializer.save(category=category)

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg(
            "reviews__score")).order_by("id")

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleReadSerializer
