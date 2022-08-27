from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager


from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

#from .managers import UserManager


CHOICES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )


#CHOICES = (
#        ('user', 'user'),
#        ('moderator', 'moderator'),
#        ('admin', 'admin'),
#    )


class User(AbstractUser):
    role = models.CharField(
        'Роль',
        unique=False,
        max_length=10,
        blank=True,
        choices=CHOICES
    )


    bio = models.TextField(
        'Биография',
        blank=True,
    ) 

    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(
        max_length=25,
        blank=True,
    )  

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=50,
        blank=True,
    )   

    password = models.CharField(
        unique=False,
        max_length=100,
        blank=True,
    )
    
    # objects = CustomUserManager()

    def __str__(self):
        return self.username
