from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


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

    def __str__(self):
        return self.username
