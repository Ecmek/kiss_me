from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .managers import BaseUserManager


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

    def save(self, *args, **kwargs):
        super().save()
        if not self.avatar:
            return
        img = Image.open(self.avatar.path)
        width, height = img.size
        watermark = Image.open(settings.WATERMARK_PATH)
        watermark.thumbnail(settings.WATERMARK_SIZE)
        mark_width, mark_height = watermark.size
        paste_mask = watermark.split()[3].point(
            lambda i: i * settings.TRANSPARENCY / 100
        )
        x = width - mark_width - settings.MARGIN
        y = height - mark_height - settings.MARGIN
        img.paste(watermark, (x, y), mask=paste_mask)
        img.save(self.avatar.path)


class Geolocation(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='geolocation',
        verbose_name='пользователь'
    )
    latitude = models.DecimalField(
        max_digits=11, decimal_places=8,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=11, decimal_places=8,
        verbose_name='Долгота'
    )

    class Meta:
        verbose_name = 'Геолокация'
        verbose_name_plural = 'Геолокации'

    def __str__(self) -> str:
        return f'{self.latitude}, {self.longitude}'
