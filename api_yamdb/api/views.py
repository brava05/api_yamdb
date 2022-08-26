from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Genre, Review, Comment, Category, Title
from .serializers import ReviewSerializer, CommentSerializer, CategorySerializer
from .serializers import TitleSerializer, GenreSerializer
from .permissions import AdminOrReadOnly, AuthorAdminModeratorOrReadOnly
from .pagination import CustomCommentPagination, CustomRewiewPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Review
    для реализации CRUD-операций со списками всех отзывов.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    throttle_classes = (AnonRateThrottle,)
    pagination_class = CustomRewiewPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет к модели Comment
    для реализации CRUD-операций c комментариями к отзывам.
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = CustomCommentPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
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
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination,
    filter_backends = [filters.SearchFilter],
    search_fields = ('name',)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter],
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination