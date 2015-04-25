import shutil
import datetime
import os
from collections import namedtuple
import warnings

from django import db
from django.conf.global_settings import MEDIA_ROOT
from django.core.cache import cache
from django.core.management import call_command
from django.test.runner import DiscoverRunner
from django.test.testcases import TestCase
from django.test.utils import override_settings
import psycopg2

from channel2.account.models import User
from channel2.settings import BASE_DIR


class Channel2TestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        connection = db.connections['default']
        db_conf = connection.settings_dict
        db_conf['NAME'] = db_conf['TEST']['NAME']

        conn = psycopg2.connect(host=db_conf['HOST'], user=db_conf['USER'])
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute('drop database if exists {NAME};'.format(**db_conf))
        cur.execute('create database {NAME};'.format(**db_conf))
        cur.close()
        conn.close()

        connection.connect()

        call_command('migrate', interactive=False)
        call_command('datacreator')

    def teardown_databases(self, old_config, **kwargs):
        try:
            shutil.rmtree(MEDIA_ROOT)
        except FileNotFoundError:
            pass


def fast_set_password(self, raw_password):
    self.password = raw_password

def fast_check_password(self, raw_password):
    return self.password == raw_password


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'media-test'))
class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.test_start = datetime.datetime.now()

        cache.clear()

        User.set_password = fast_set_password
        User.check_password = fast_check_password

        self.user = User.objects.get(email='testuser@example.com')

        self.request = namedtuple('Request', 'user')
        self.request.user = self.user
        self.request.META = {'REMOTE_ADDR': '127.0.0.1'}

        self.client.login(email=self.user.email, password=self.user.password)

    def tearDown(self):
        self.test_stop = datetime.datetime.now()
        duration = (self.test_stop - self.test_start).microseconds // 1000
        if duration > 150:
            warnings.warn('{} is slower than 150ms: {}ms'.format(self._testMethodName, duration), RuntimeWarning)
        super().tearDown()
