# Kiss Me 
REST API - для сервиса знакомств.
### Описание
Данный проект предоставляет возможность просматривать различных пользователей, и ставить им симпатию. При взаимной симпатии участники получают об этом уведомление на почту.
### Технологии
Python, Django, DRF, DRF-Simple JWT, Django-filter, requests, beautifulsoup
### Запуск проекта в dev-режиме
- Клонировать репозиторий и перейти в него в командной строке:
- Установите и активируйте виртуальное окружение:

```
python3 -m venv venv

Для пользователей linux/Mac:
source venv/bin/activate
Для пользователей Windows:
source venv/Scripts/activate

python -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Перейдите в каталог с файлом manage.py выполните команды:
Выполнить миграции:
```
python manage.py migrate
```
Создайте супер-пользователя:
```
python manage.py createsuperuser
```
Соберите статику:
```
python manage.py collectstatic
```
Тестовые пользователи:
```
python manage.py load_users
```
Запуск проекта:
```
python manage.py runserver
```
### Parser bs4
В проекте присутствует парсер для сайта https://www.citilink.ru
Что бы его им пользоваться необходимо передать 3 параметра в менеджмент команду.
url_category, title_category, slug_category
```
python manage.py https://www.citilink.ru/catalog/setevye-hranilischa-nas/ Сетевые хранилища NAS setevye-hranilischa-nas
```
После этой комманды будет создана категория "Сетевые хранилища NAS" со слагом "setevye-hranilischa-nas" и в данную категорию будут добавлены товары.

Просмотреть их можно будет.
```
api/products/setevye-hranilischa-nas/
```

### Примеры REST API
Доступны всем пользователям.
```
api/clients/create/ - создание пользователя,
```
Доступ авторизованным пользователям.
```
api/clients/token/ - получить токен,
api/clients/token/refresh/ - обновление токена,
api/list/ - просмотр других пользователей,
api/clients/{user_id}/match - оценка пользователя
api/clients/get_geolocation/ - определяет геолокацию по IP,
api/clients/set_geolocation/ - устанавливают заданную геолокацию,
```
Так же в сервисе есть товары и категории.
```
api/category/ - все категории
api/products/{category_slug}/ - товары категории
```
Так же в проекте присутсвует пагинация(LimitOffsetPagination), поиск, фильтрация и сортировка, примеры ниже
```
api/list/?limit=10&offset=0 - Пагинация
api/list/?search=your_search - Поиск пользователя
api/list/?ordering=first_name - сортировка по имени(алфовитный порядок)
api/list/?gender=F - фильтрация по полу
```
Регистрация пользователя:
```
api/clients/create/
{
	"emal": "your_email",
	"password": "your_password",
	"first_name": "first_name",
	"last_name": "last_name",
	"gender": "M" or "F"
}
```
Доступ авторизованным пользователем доступен по jwt-токену, который можно получить выполнив POST запрос по адресу:
```
api/clients/token/
```
Передав в body данные пользователя:
```
{
	"email": "your_email",
	"password": "your_password"
}
```
Получив токен его нужно добавить в headers, после этого вам буду доступны все функции проекта:
```
Authorization: Bearer {your_token}
```

### Авторы
GerG
