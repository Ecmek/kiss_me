
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from .test_create import auth_client

User = get_user_model()
faker = Faker()


class MacthTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.male = User.objects.create(
            gender='M',
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            password=faker.password(),
        )
        cls.female = User.objects.create(
            gender='F',
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            password=faker.password(),
        )

    def setUp(self) -> None:
        self.male_client = auth_client(self.male)
        self.female_client = auth_client(self.female)

    def test_users_list_not_auth(self):
        response = self.client.get('/api/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_list_bad_method(self):
        response = self.female_client.post('/api/list/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_users_list_auth(self):
        response = self.male_client.get('/api/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count_users = User.objects.count()
        response_count = response.data.get('count')
        self.assertEqual(response_count, count_users)

    def test_test_search(self):
        response = self.male_client.get(f'/api/list/?search={self.female.first_name}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('results')[0]
        for key, value in data.items():
            self.assertEqual(getattr(self.female, key), value)

    def test_filterset_fields(self):
        response = self.male_client.get(f'/api/list/?gender={self.female.gender}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('results')[0]
        for key, value in data.items():
            self.assertEqual(getattr(self.female, key), value)
