from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .v1.views import (get_token_view, GenreViewSet, ReviewViewSet,
                       CommentViewSet, CategoryViewSet, TitleViewSet,
                       UserCreateViewSet, UserViewSet,)

v1_router = SimpleRouter()

v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register('categories', CategoryViewSet, basename='categories')

v1_router.register('users', UserViewSet)


auth_patterns = [
    path('auth/signup/', UserCreateViewSet.as_view()),
    path('auth/token/', get_token_view),
]

urlpatterns = [
    path('v1/', include(auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
