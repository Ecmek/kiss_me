import os
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from match.models import Match

User = get_user_model()
faker = Faker()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
    EMAIL_FILE_PATH=tempfile.mkdtemp(),
)
class MacthTest(APITestCase):

    mark_true = {"mark": True}
    mark_false = {"mark": False}

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

    def auth_client(self, user):
        refresh = RefreshToken.for_user(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    def test_match_endpoint(self):
        client_user = self.auth_client(self.male)
        response = client_user.get(f'/api/clients/{self.female.id}/match/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        for key, value in data.items():
            self.assertEqual(getattr(self.female, key), value)

    def test_match_self(self):
        client_user = self.auth_client(self.male)
        response = client_user.post(f'/api/clients/{self.male.id}/match/', data=self.mark_false)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retry_match(self):
        client_user = self.auth_client(self.male)
        response = client_user.post(f'/api/clients/{self.female.id}/match/', data=self.mark_false)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client_user.post(f'/api/clients/{self.female.id}/match/', data=self.mark_false)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_matches(self):
        client_male = self.auth_client(self.male)
        client_female = self.auth_client(self.female)
        response = client_male.post(
            f'/api/clients/{self.female.id}/match/', data=self.mark_true
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Match.objects.filter(user=self.male, matching=self.female, mark=True).exists()
        )

        response = client_female.post(
            f'/api/clients/{self.male.id}/match/', data=self.mark_true
        )
        self.assertTrue(
            Match.objects.filter(user=self.female, matching=self.male, mark=True).exists()
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        count_emails = len(os.listdir(settings.EMAIL_FILE_PATH))
        self.assertNotEqual(count_emails, 0)
