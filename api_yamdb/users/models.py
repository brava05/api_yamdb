from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):

    SIMPLE_USER = 'user'
    MODERATOR = 'moderator'
    ADMINISTRATOR = 'admin'
    ROLE_CHOICES = [
        (SIMPLE_USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMINISTRATOR, 'admin'),
    ]

    role = models.CharField(
        'Роль',
        max_length=50,
        unique=False,
        blank=True,
        choices=ROLE_CHOICES,
        default=SIMPLE_USER,
    )

    def is_upperclass(self):
        return self.role in {
            self.SIMPLE_USER,
            self.MODERATOR,
            self.ADMINISTRATOR
        }

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    email = models.EmailField(unique=True)

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=50,
        blank=True,
    )

    password = models.CharField(
        _('password'),
        max_length=128,
        unique=False,
        blank=True,
    )

    def __str__(self):
        return self.username
