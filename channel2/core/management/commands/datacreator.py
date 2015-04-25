import datetime
import sys

from django.core.management.base import BaseCommand

from channel2.account.models import User


def timed(func):
    """
    use @timed to decorate a function that will print out the time it took
    for this function to run.
    """

    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        sys.stdout.write('\t{} '.format(func.__name__))
        sys.stdout.flush()
        result = func(*args, **kwargs)
        finish = datetime.datetime.now()
        sys.stdout.write('- {}\n'.format(finish - start))
        return result

    return inner


class Command(BaseCommand):

    @timed
    def create_users(self):
        def create_user_helper(email, name, is_active=True, **kwargs):
            user = User(email=email, name=name, is_active=is_active, **kwargs)
            user.set_password('password')
            user.save()
            return user

        self.user = create_user_helper('testuser@example.com', 'Test User')
        self.staff_user = create_user_helper('staffuser@example.com', 'Staff User')

    def handle(self, *args, **options):
        print('-'*70)
        print('datacreator.py started')
        start = datetime.datetime.now()

        self.create_users()

        finish = datetime.datetime.now()
        print('datacreator.py finished in {}'.format(finish-start))
        print('-'*70)
