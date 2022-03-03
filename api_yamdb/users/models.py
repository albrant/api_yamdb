from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = [
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    # добавила роль, но вопрос, а как быть с суперпользователем. Он всегда админ, но админ не всегда суперпользователь
    role = models.CharField(choices=CHOICES)
