from captcha.conf import settings
from captcha.models import CaptchaStore

from channel2.account.forms import AccountLoginForm
from channel2.core.tests import BaseTestCase


class AccountLoginFormTests(BaseTestCase):

    def test_account_login_form(self):
        form = AccountLoginForm(request=self.request, data={
            'email': 'testuser@example.com',
            'password': self.user.password,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_account_login_form_case_insensitive(self):
        form = AccountLoginForm(request=self.request, data={
            'email': 'TESTUSER@EXAMPLE.COM',
            'password': self.user.password,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_account_login_form_fail(self):
        for i in range(AccountLoginForm.LOGIN_ATTEMPT_LIMIT):
            form = AccountLoginForm(request=self.request, data={
                'email': 'testuser@example.com',
                'password': 'wrong-password',
            })
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['__all__'], [AccountLoginForm.error_messages['invalid_login']])

        form = AccountLoginForm(request=self.request, data={
            'email': 'testuser@example.com',
            'password': self.user.password,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['captcha'], ['This field is required.'])

        challenge, response = settings.get_challenge()()
        store = CaptchaStore.objects.create(challenge=challenge, response=response)

        form = AccountLoginForm(request=self.request, data={
            'email': 'testuser@example.com',
            'password': self.user.password,
            'captcha_0': store.hashkey,
            'captcha_1': store.response,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_account_login_is_active_false(self):
        self.user.is_active = False
        self.user.save()
        form = AccountLoginForm(request=self.request, data={
            'email': self.user.email,
            'password': self.user.password,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [AccountLoginForm.error_messages['inactive']])
