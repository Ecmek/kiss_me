import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        with open(settings.BASE_DIR / 'test_data/test_users.csv',
                  'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            User.objects.bulk_create(User(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully load users'))
