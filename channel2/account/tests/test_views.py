from django.core.urlresolvers import reverse

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
        pass

    def test_account_logout_view_post(self):
        pass


class AccountLogoutViewTestsAuthenticated(BaseTestCase):

    def test_account_logout_view_get(self):
        pass

    def test_account_logout_view_post(self):
        pass
