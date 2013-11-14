from django.test import TestCase
from channel2.account.models import User


def fast_set_password(self, raw_password):
    self.password = raw_password

def fast_check_password(self, raw_password):
    return self.password == raw_password


class BaseTestCase(TestCase):
    """
    BaseTestCase class which other test classes can inherit from.
    This class provides a user and an authenticated session.
    """

    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()

        # monkey patching User model to speed up tests
        cls.original_set_password = User.set_password
        cls.original_check_password = User.check_password

        User.set_password = fast_set_password
        User.check_password = fast_check_password

        User.objects.all().delete()

        dc = DataCreator({
            'NUM_USERS': 1,
            'NUM_VIDEOS': 1,
        })
        dc.create_users()
        dc.create_labels()
        dc.create_videos()

        cls.user = dc.user

    @classmethod
    def tearDownClass(cls):
        User.set_password = cls.original_set_password
        User.check_password = cls.original_check_password
        super(BaseTestCase, cls).tearDownClass()

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.client.login(email='testuser@example.com', password='password')

