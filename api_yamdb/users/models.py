from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.TextField(
        'Роль',
        blank=True,
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
    # objects = UserManager()

    def __str__(self):
        return self.username

