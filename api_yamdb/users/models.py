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
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=20,
        blank=True,
        null=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=20,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    bio = models.CharField(
        verbose_name='Биография',
        max_length=100,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=CHOICES,
        default=USER,
        max_length=10
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    @property
    def is_admin(self):
        return any([
            self.role == ADMIN,
            self.is_superuser,
            self.is_staff,
        ])

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
