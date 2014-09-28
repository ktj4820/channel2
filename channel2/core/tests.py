from collections import namedtuple
import os
import sys
import shutil

from django import db

from django.core.cache import cache
from django.core.management import call_command
from django.test.runner import DiscoverRunner
from django.test.testcases import TestCase
from django.test.utils import override_settings
import psycopg2

from channel2.account.models import User
from channel2.datacreator import DataCreator
from channel2.settings import BASE_DIR


MEDIA_ROOT = os.path.join(BASE_DIR, 'media-test')


def fast_set_password(self, raw_password):
    self.password = raw_password

def fast_check_password(self, raw_password):
    return self.password == raw_password


def suppress_output(f):
    def _suppress_output(*args, **kwargs):
        devnull = open(os.devnull, 'w')
        stdout, sys.stdout = sys.stdout, devnull
        f(*args, **kwargs)
        sys.stdout = stdout

    return _suppress_output


class Channel2TestSuiteRunner(DiscoverRunner):

    def create_testdb(self):
        call_command('migrate', interactive=False)
        dc = DataCreator('test')
        dc.run()

    def setup_databases(self, **kwargs):
        connection = db.connections['default']
        db_conf = connection.settings_dict
        db_conf['NAME'] = db_conf['TEST']['NAME']

        conn = psycopg2.connect(host=db_conf['HOST'], user=db_conf['USER'])
        conn.set_isolation_level(0)
        cur = conn.cursor()
        cur.execute('drop database if exists {NAME};'.format(**db_conf))
        cur.execute('create database {NAME};'.format(**db_conf))
        cur.close()
        conn.close()

        conn = psycopg2.connect(host=db_conf['HOST'], user=db_conf['USER'], database=db_conf['NAME'])
        cur_brain_test = conn.cursor()
        cur_brain_test.execute("create extension hstore;")
        cur_brain_test.close()
        conn.close()

        connection.connect()
        self.create_testdb()

    def teardown_databases(self, old_config, **kwargs):
        try:
            shutil.rmtree(MEDIA_ROOT)
        except FileNotFoundError:
            pass


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()

        cache.clear()

        User.set_password = fast_set_password
        User.check_password = fast_check_password

        self.user = User.objects.get(email='testuser@example.com')
        self.user.set_password('password')
        self.user.save()

        self.request = namedtuple('Request', 'user')
        self.request.user = self.user
        self.request.META = {'REMOTE_ADDR': '127.0.0.1'}

        self.client.login(email='testuser@example.com', password='password')

    def assertTemplateUsed(self, response, template_name):
        self.assertEqual(response.template_name, template_name)
