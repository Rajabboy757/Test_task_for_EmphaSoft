from django.core.management.base import BaseCommand
from company.models import Company


class Command(BaseCommand):
    help = 'Creates test Companies'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='count of necessary employees')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        Company.objects.bulk_create(
            [Company(name=f'company{i + 1}',
                     email=f'company{i + 1}@gmail.com',
                     phone=f'9989996987{i + 1}',
                     owner_id=1) for i in range(count)]
        )

        print(f'Created {count} test Companies')
