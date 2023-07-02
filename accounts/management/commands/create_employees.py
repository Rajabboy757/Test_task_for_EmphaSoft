from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Creates test employees'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='count of necessary employees')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        User.objects.bulk_create(
            [User(username=f'employee{i + 1}',
                  email=f'employee{i + 1}@gmail.com',
                  password='password',
                  type='employee') for i in range(count)])

        print(f'Created {count} test employees')
