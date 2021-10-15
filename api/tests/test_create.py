from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
faker = Faker()


class UserCreationTest(APITestCase):
    """Регистрация пользователя"""

    def test_creation_male(self):
        users_count = User.objects.count()
        data = {
            "gender": 'M',
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password()
        }
        response = self.client.post('/api/clients/create/', data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_count + 1, User.objects.count())
        user = User.objects.first()
        data.pop('password')
        for key, value in data.items():
            self.assertEqual(getattr(user, key), value)

    def test_creation_female(self):
        users_count = User.objects.count()
        data = {
            "gender": 'F',
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password()
        }
        response = self.client.post('/api/clients/create/', data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_count + 1, User.objects.count())
        user = User.objects.first()
        data.pop('password')
        for key, value in data.items():
            self.assertEqual(getattr(user, key), value)

    def test_wrong_creation(self):
        users_count = User.objects.count()
        data = {
            "email": faker.email(),
            "password": faker.password()
        }
        response = self.client.post('/api/clients/create/', data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_count, User.objects.count())
