from django.core.management.base import BaseCommand
from accounts.models import User
from company.models import Company
from location.models import Location, LocationImages


class Command(BaseCommand):
    help = 'Creates test objects'

    def add_arguments(self, parser):
        parser.add_argument('user', type=int, help='count of necessary users')
        parser.add_argument('company', type=int, help='count of companies for each user')
        parser.add_argument('employee', type=int, help='count of employees for each company')
        parser.add_argument('location', type=int, help='count of locations for each company')
        parser.add_argument('location_images', type=int, help='count of images for each location')

    def handle(self, *args, **kwargs):
        user = kwargs['user']
        company = kwargs['company']
        employee = kwargs['employee']
        location = kwargs['location']
        location_images = kwargs['location_images']

        User.objects.bulk_create(
            [User(username=f'user{i + 1}',
                  email=f'user{i + 1}@gmail.com',
                  password='password',
                  type='admin') for i in range(user)])

        print(f'Created {user} test users')

        companies = Company.objects.bulk_create(
            [Company(name=f'company{i + 1}',
                     email=f'company{i + 1}@gmail.com',
                     phone=f'9989996987{i + 1}',
                     owner=User.objects.get(username=f'user{i // company + 1}')) for i in range(company * user)])

        print(f'Created {company * user} test companies')

        j = 1
        for compani in companies:
            employees = User.objects.bulk_create(
                [User(username=f'testemployee{j}{(i + 1)}',
                      email=f'testemployee{j}{(i + 1)}@gmail.com',
                      password='password',
                      type='employee') for i in range(employee)])
            compani.employee.add(*employees)
            j += 1

        print(f'Added {employee} employees for {company * user} companies')

        Location.objects.bulk_create(
            [Location(name=f'location{i + 1}',
                      address=f'address{i + 1}',
                      company=Company.objects.get(name=f'company{i // location + 1}')) for i in
             range(company * location * user)])

        print(f'Created {company * location * user} test locations')

        LocationImages.objects.bulk_create(
            [LocationImages(title=f'locationimage{i + 1}',
                            location=Location.objects.get(name=f'location{i // location_images + 1}')) for i in
             range(company * location * user * location_images)])

        print(f'Created {company * location * user * location_images} test location images')
