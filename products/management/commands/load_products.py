import os
import random
import time

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.conf import settings

from products.models import Category, Product


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)
        parser.add_argument('title', type=str)
        parser.add_argument('slug', type=str)

    def handle(self, *args, **options):
        url = options['url']
        title = options['title']
        slug = options['slug']
        category, created = Category.objects.get_or_create(title=title, slug=slug)
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 OPR/80.0.4170.40'}
        if not os.path.exists(settings.BASE_DIR / 'media/products'):
            os.mkdir(settings.BASE_DIR / 'media/products')
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            pagination = soup.find('div', class_='PaginationWidget__wrapper-pagination')
            last_page = int(pagination.find_all('a')[-2].text.replace(' ', '').replace('\n', ''))
            products_list = []
            for i in range(1, last_page + 1):
                print(f'Обрабатывается страница №{i}')
                response = requests.get(f'{url}?p={i}', headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                products_card = soup.find_all('div', class_='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')
                for product in products_card:
                    product_price = product.find('span', class_='ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price').text.replace(' ', '').replace('\n', '')
                    product_title = product.find('div', class_='ProductCardHorizontal__header-block').find('a').text
                    product_image = product.find('img')['src']
                    image = requests.get(product_image)
                    image_name = product_image.split('/')[-1]
                    path = settings.BASE_DIR / 'media/products'
                    image_path = f'products/{image_name}'
                    with open(f'{path}/{image_name}', 'wb') as file:
                        file.write(image.content)
                    product = Product(
                                title=product_title,
                                price=float(product_price),
                                image=image_path,
                                category=category
                            )
                    products_list.append(product)
                time.sleep(random.randint(1, 3))
            Product.objects.bulk_create(products_list)
            self.stdout.write(self.style.SUCCESS('Данные успешно добавлены в БД'))
        except Exception as e:
            print(f'Хьюстон у нас проблемы\n{e}')
