from accounts.models import User
from django.core.management.base import BaseCommand
import environ

env = environ.Env(
    # set casting default value
    DEBUG=(bool, False)
)


class Command(BaseCommand):
    help = 'Creates default superuser'

    def handle(self, *args, **kwargs):
        username = env('SUPERUSER_NAME')
        email = env('SUPERUSER_EMAIL')
        password = env('SUPERUSER_PASSWORD')
        # print(username, email, password)
        try:
            User.objects.create_user(username=username,
                                     email=email,
                                     password=password,
                                     email_verified=True,
                                     is_superuser=True,
                                     is_staff=True)
            user = User.objects.get(username=username)
            print(f'Superuser created with username: {user.username}')
        except:
            print(f'Cannot create superuser with username: {username} and email: {email}')
