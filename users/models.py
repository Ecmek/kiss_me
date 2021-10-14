from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import BaseUserManager


class User(AbstractUser):

    class Gender(models.TextChoices):
        MALE = 'M', _('Мужской')
        FEMALE = 'F', _('Женский')

    username = None
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True, null=True,
        verbose_name='Аватар профиля',
    )
    gender = models.CharField(
        max_length=1, choices=Gender.choices,
        verbose_name='Половая принадлежность'
    )
    first_name = models.CharField(
        _('Имя'), max_length=150
    )
    last_name = models.CharField(
        _('Фамилия'), max_length=150
        )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.email
