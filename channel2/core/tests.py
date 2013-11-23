import shutil, tempfile
from django.db import connections
from django.test import TestCase
from django.test.runner import DiscoverRunner
from channel2 import settings
from channel2.account.models import User
from channel2.label.models import Label
from channel2.video.models import Video


def fast_set_password(self, raw_password):
    self.password = raw_password

def fast_check_password(self, raw_password):
    return self.password == raw_password


class Channel2TestSuiteRunner(DiscoverRunner):

    def copy_db(self, db_path):
        self.temp_db = tempfile.NamedTemporaryFile()
        shutil.copy2(db_path, self.temp_db.name)
        return self.temp_db.name

    def setup_databases(self, **kwargs):
        for alias in connections:
            connection = connections[alias]
            self.copy_db(settings.DATABASES[alias]['TEST_NAME'])
            connection.settings_dict['NAME'] = self.temp_db.name

    def teardown_databases(self, old_config, **kwargs):
        self.temp_db.close()


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()

        User.set_password = fast_set_password
        User.check_password = fast_check_password

        self.user = User.objects.get(email='testuser@example.com')
        self.user.set_password('password')
        self.user.save()

        self.label_list = Label.objects.all()
        self.video_list = Video.objects.all()

        self.client.login(email='testuser@example.com', password='password')


class TestRequest(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
