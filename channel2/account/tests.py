from captcha.conf import settings
from captcha.models import CaptchaStore
from django.core.urlresolvers import reverse

from channel2.account.forms import AccountLoginForm
from channel2.account.models import User
from channel2.core.tests import BaseTestCase


class AccountLoginViewTestsAnonymous(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_account_login_view_get(self):
        response = self.client.get(reverse('account.login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-login.html')

    def test_account_login_view_post_invalid(self):
        response = self.client.post(reverse('account.login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-login.html')

    def test_account_login_view_post(self):
        response = self.client.post(reverse('account.login'), {
            'email': 'testuser@example.com',
            'password': 'password',
        })
        self.assertRedirects(response, reverse('home'))

    def test_account_login_view_post_next(self):
        response = self.client.post(reverse('account.login'), {
            'email': 'testuser@example.com',
            'password': 'password',
            'next': reverse('blog'),
        })
        self.assertRedirects(response, reverse('blog'))


class AccountLoginViewTestsAuthenticated(BaseTestCase):

    def test_account_login_view_get(self):
        response = self.client.get(reverse('account.login'))
        self.assertRedirects(response, reverse('home'))

    def test_account_login_view_post_invalid(self):
        response = self.client.post(reverse('account.login'))
        self.assertRedirects(response, reverse('home'))


class AccountLoginFormTests(BaseTestCase):

    def test_account_login_form(self):
        form = AccountLoginForm(request=self.request, data={
            'email': 'testuser@example.com',
            'password': 'password',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_account_login_form_case_insensitive(self):
        form = AccountLoginForm(request=self.request, data={
            'email': 'TESTUSER@EXAMPLE.COM',
            'password': 'password',
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
            'password': 'password',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['captcha'], ['This field is required.'])

        challenge, response = settings.get_challenge()()
        store = CaptchaStore.objects.create(challenge=challenge, response=response)

        form = AccountLoginForm(request=self.request, data={
            'email': 'testuser@example.com',
            'password': 'password',
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


class AccountActivateViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user.generate_token()
        self.user.save()
        self.client.logout()

    def test_account_activate_view_get(self):
        response = self.client.get(reverse('account.activate', args=[self.user.token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-activate.html')

    def test_account_activate_view_post_invalid(self):
        response = self.client.post(reverse('account.activate', args=[self.user.token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-activate.html')

    def test_account_activate_view_post(self):
        response = self.client.post(reverse('account.activate', args=[self.user.token]), {
            'password1': 'Pa55w0rD',
            'password2': 'Pa55w0rD',
        })
        self.assertRedirects(response, reverse('home'))

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('Pa55w0rD'))
        self.assertIsNone(user.token)


class AccountPasswordResetViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_account_password_reset_view_get(self):
        response = self.client.get(reverse('account.password.reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-password-reset.html')

    def test_account_password_reset_view_post_invalid(self):
        response = self.client.post(reverse('account.password.reset'), {
            'email': 'invaliduser@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-password-reset.html')

    def test_account_password_reset_view_post(self):
        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.token)

        response = self.client.post(reverse('account.password.reset'), {
            'email': self.user.email,
        })
        self.assertRedirects(response, reverse('account.login'))

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.token)


class AccountPasswordSetViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user.generate_token()
        self.user.save()
        self.client.logout()

    def test_account_password_set_view_get(self):
        response = self.client.get(reverse('account.password.set', args=[self.user.token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-password-set.html')

    def test_account_password_set_view_post_invalid(self):
        response = self.client.post(reverse('account.password.set', args=[self.user.token]), {
            'password1': '1234',
            'password2': '5678',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-password-set.html')

    def test_account_password_set_view_post(self):
        response = self.client.post(reverse('account.password.set', args=[self.user.token]), {
            'password1': 'pass',
            'password2': 'pass',
        })
        self.assertRedirects(response, reverse('home'))

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('pass'))
