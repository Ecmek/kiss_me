from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Match(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
    )
    matching = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='match',
        verbose_name='Оцениваемый'
    )
    mark = models.BooleanField()
    mark_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последного отметки'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'matching'],
                name='unique matches')
        ]
        verbose_name = 'Совпадение'
        verbose_name_plural = 'Совпадения'
