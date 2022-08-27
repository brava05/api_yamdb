from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    UserCreateViewSet,
    GetTokenView,
    ProfileView,
    UserCreateByAdminView,
    UserViewSet
)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)


urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/users/me/', ProfileView.as_view()),
    path('v1/', include(v1_router.urls)),
    #path('v1/users/', UserCreateByAdminView.as_view()),
]
