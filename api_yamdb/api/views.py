from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.db.models import Avg

from reviews.models import Genre, Review, Comment, Category, Title
from .serializers import (ReviewSerializer, CommentSerializer,
                          CategorySerializer, TitleSerializer,
                          TitleReadSerializer, GenreSerializer)
from .permissions import (AdminOrReadOnly,
                          AuthorAdminModeratorOrReadOnly,
                          AuthorAdminModeratorOrReadAndPost)
from .pagination import CustomPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Review
    для реализации CRUD-операций со списками всех отзывов.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadAndPost,)
    throttle_classes = (AnonRateThrottle,)
    pagination_class = CustomPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Comment
    для реализации CRUD-операций c комментариями к отзывам.
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadAndPost,)
    pagination_class = CustomPagination

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


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def delete_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer
        category.delete()
        return Response(
            serializer.data,
            status=status.HTTP_204_NO_CONTENT
        )


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Получение списка всех жанров.
    Права доступа: Доступно без токена.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех произведений.
    Права доступа: Доступно без токена.
    """
    queryset = Title.objects.prefetch_related(
        'category', 'genre').annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        slug = self.request.data.get('category')
        category = Category.objects.get(slug)
        description = self.request.data.get('description')
        #slug = serializer.data.get("category")
        #print(slug)
        #category = get_object_or_404(Category, slug=slug)
        #print(category)
        # print("__6")
        #serializer.save(category=category)
        return serializer.save(
            category=category,
            description=description
        )

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
            return TitleReadSerializer
        return TitleSerializer
