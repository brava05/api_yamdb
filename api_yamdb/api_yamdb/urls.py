from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (TokenObtainSlidingView,)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/token/', TokenObtainSlidingView.as_view()),
    #path('api/v1/auth/signup/', TokenObtainSlidingView.as_view() )
]
