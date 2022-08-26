from django.urls import path

# from rest_framework.routers import DefaultRouter

from .views import (
    UserCreateViewSet,
    GetTokenView,
    ProfileView,
    UserCreateByAdminView
)


urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/users/me/', ProfileView.as_view()),
    path('v1/users/', UserCreateByAdminView.as_view()),
]
