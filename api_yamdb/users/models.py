from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


ANONIMOUS = 'anonimous'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


CHOICES = [
    ('anon', ANONIMOUS),
    ('admin', ADMIN),
    ('moderator', MODERATOR),
    ('user', USER)
]


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Неоходимо указать email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', ADMIN)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
    )
    bio = models.CharField(
        'Биография',
        max_length=100,
        blank=True,
        null=True
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
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
