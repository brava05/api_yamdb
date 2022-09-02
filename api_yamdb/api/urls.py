from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .v1.views import (GenreViewSet, GetTokenView, ReviewViewSet,
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

urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet.as_view()),
    path('v1/auth/token/', GetTokenView),
    path('v1/', include(v1_router.urls)),
]
