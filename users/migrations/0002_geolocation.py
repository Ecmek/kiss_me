# Generated by Django 3.2.8 on 2021-10-15 19:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Долгота')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='geolocation', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Геолокация',
                'verbose_name_plural': 'Геолокации',
            },
        ),
    ]
