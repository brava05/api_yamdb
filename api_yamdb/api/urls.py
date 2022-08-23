from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet, CategoryViewSet


v1_router = DefaultRouter()
v1_router.register('reviews', ReviewViewSet, basename='reviews')
v1_router.register(
    'reviews/(?P<post_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register('categories', CategoryViewSet, basename='categories')

