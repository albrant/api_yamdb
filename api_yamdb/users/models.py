from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = [
    ('anon', 'anonimus'),
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    email = models.CharField(
        'Электронная почта',
        max_length=100,
        unique=True,
        null=False,
        blank=False
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    # добавила роль, но вопрос, а как быть с суперпользователем.
    # Он всегда админ, но админ не всегда суперпользователь
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=10,
        null=True,
        blank=True
    )
    agree_code = models.CharField(
        'Код подтверждения',
        max_length=200,
        null=True,
        blank=True
    )
