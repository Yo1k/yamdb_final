from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор '),
        (USER, 'Пользователь'),
    ]

    bio = models.TextField(
        blank=True
    )
    confirmation_code = models.CharField(
        _('confirmation_code'),
        blank=True,
        max_length=128,
    )
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
    )
    role = models.CharField(
        choices=USER_ROLES,
        default=USER,
        max_length=10,
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    def clean(self):
        super().clean()
        email_validator = EmailValidator()
        email_validator(self.email)

    def __str__(self):
        return (
            f'username={self.username}, '
            f'email={self.email}, '
            f'role={self.role}'
        )
