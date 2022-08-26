from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GenreViewSet, ReviewViewSet, CommentViewSet, CategoryViewSet, TitleViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)

jwt_patterns = [
    path('create/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/',
         TokenVerifyView.as_view(), name='token_verify')
]

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

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/jwt/', include(jwt_patterns))
]
