from django.db import models


class Category(models.Model):

    title = models.CharField(
        max_length=200, null=False,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Url адрес категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='category_products',
        verbose_name='Категория'
    )
    price = models.DecimalField(
        max_digits=25, decimal_places=2,
        verbose_name='Цена товара'
    )
    title = models.CharField(
        max_length=200, null=False,
        verbose_name='Название товара',
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение товара',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
