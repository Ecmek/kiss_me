from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

faker = Faker()


class UserCreationTest(APITestCase):
    """Регистрация пользователя"""

    def test_creation_male(self):
        data = {
            "gender": 'M',
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password()
        }
        response = self.client.post('/api/clients/create/', data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creation_female(self):
        data = {
            "gender": 'F',
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password()
        }
        response = self.client.post('/api/clients/create/', data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_creation(self):
        data = {
            "email": faker.email(),
            "password": faker.password()
        }
        response = self.client.post('/api/clients/create/', data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
