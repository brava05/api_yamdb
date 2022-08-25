from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from users.views import UserCreateViewSet, GetTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', UserCreateViewSet.as_view()),
    path('api/v1/auth/token/', GetTokenView.as_view()),
    #path('api/v1/users/me/', FillProfile.as_view()),
]
