from accounts.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Verifies user email by email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        if email in User.objects.values_list('email', flat=True):

            a = User.objects.get(email=email)
            if not a.email_verified:
                a.email_verified = True
                a.save()
                print(f'For user with username: {a.username} email verified')

            else:
                print(f'For user with username: {a.username} email is already verified')
        else:
            print(f'There is no user with such email')