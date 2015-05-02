from django.core.urlresolvers import reverse

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
            'password': self.user.password,
        })
        self.assertRedirects(response, reverse('home'))

    def test_account_login_view_post_next(self):
        response = self.client.post(reverse('account.login'), {
            'email': 'testuser@example.com',
            'password': self.user.password,
            'next': reverse('tag.list'),
        })
        self.assertRedirects(response, reverse('tag.list'))


class AccountLoginViewTestsAuthenticated(BaseTestCase):

    def test_account_login_view_get(self):
        response = self.client.get(reverse('account.login'))
        self.assertRedirects(response, reverse('home'))

    def test_account_login_view_post_invalid(self):
        response = self.client.post(reverse('account.login'))
        self.assertRedirects(response, reverse('home'))


class AccountLogoutViewTestsAnonymous(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_account_logout_view_get(self):
        response = self.client.get(reverse('account.logout'))
        self.assertRedirects(response, reverse('account.login'))

    def test_account_logout_view_post(self):
        response = self.client.post(reverse('account.logout'))
        self.assertRedirects(response, reverse('account.login'))


class AccountLogoutViewTestsAuthenticated(BaseTestCase):

    def test_account_logout_view_get(self):
        response = self.client.get(reverse('account.logout'))
        self.assertRedirects(response, reverse('home'))

    def test_account_logout_view_post(self):
        response = self.client.post(reverse('account.logout'))
        self.assertRedirects(response, reverse('account.login'))


class AccountActivateViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user.generate_token()
        self.user.save()
        self.client.logout()

    def test_account_activate_view_get(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.get(reverse('account.activate', args=[self.user.token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-activate.html')

    def test_account_activate_view_post_invalid(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse('account.activate', args=[self.user.token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-activate.html')

    def test_account_activate_view_post(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse('account.activate', args=[self.user.token]), {
            'password1': 'Pa55w0rD',
            'password2': 'Pa55w0rD',
        })
        self.assertRedirects(response, reverse('home'))

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('Pa55w0rD'))
        self.assertIsNone(user.token)

    def test_account_activate_view_get_is_active(self):
        response = self.client.get(reverse('account.activate', args=[self.user.token]))
        self.assertEqual(response.status_code, 404)

    def test_account_activate_view_post_is_active(self):
        response = self.client.post(reverse('account.activate', args=[self.user.token]))
        self.assertEqual(response.status_code, 404)


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

    def test_account_password_set_view_get_inactive(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.get(reverse('account.password.set', args=[self.user.token]))
        self.assertEqual(response.status_code, 404)

    def test_account_password_set_view_post_inactive(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse('account.password.set', args=[self.user.token]))
        self.assertEqual(response.status_code, 404)
