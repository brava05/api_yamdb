from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from reviews.models import Genre, Review, Comment, Category, Title
from .serializers import ReviewSerializer, CommentSerializer, CategorySerializer
from .serializers import TitleSerializer, GenreSerializer
from .permissions import AdminOrReadOnly, AuthorAdminModeratorOrReadOnly, AuthorAdminModeratorOrReadAndPost
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

#     def validate
# title_id = (self.context['request'].parser_context['kwargs']['title_id'])

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
    pagination_class = LimitOffsetPagination,
    filter_backends = [filters.SearchFilter],
    search_fields = ('name',)

    def perform_destroy(self, instance):
        instance.delete()


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
    filter_backends = [filters.SearchFilter],
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех произведений.
    Права доступа: Доступно без токена.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        slug=serializer.data.get("category")
        print(slug)
        category = get_object_or_404(Category, slug=slug)
        print(category)
        # print("__6")
        serializer.save(category=category)
