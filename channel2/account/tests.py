from django.core.urlresolvers import reverse
from channel2.account.models import User
from channel2.core.tests import BaseTestCase


class AccountViewTests(BaseTestCase):
    
    def test_account_login_view_get(self):
        response = self.client.get(reverse('account.login'))
        self.assertRedirects(response, reverse('video.list'))

    def test_account_login_view_post(self):
        response = self.client.post(reverse('account.login'))
        self.assertRedirects(response, reverse('video.list'))

    def test_account_logout_view_get(self):
        response = self.client.get(reverse('account.logout'))
        self.assertEquals(response.status_code, 405)

    def test_account_logout_view_post(self):
        response = self.client.post(reverse('account.logout'))
        self.assertRedirects(response, reverse('account.login'))


class AccountViewTestsAnonymous(BaseTestCase):

    def setUp(self):
        super(AccountViewTestsAnonymous, self).setUp()
        self.client.logout()

    def test_account_login_view_get(self):
        response = self.client.get(reverse('account.login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-login.html')

    def test_account_login_view_post_failed(self):
        response = self.client.post(reverse('account.login'), {
            'email': 'wronguser@example.com',
            'password': 'password',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-login.html')

    def test_account_login_view_post(self):
        response = self.client.post(reverse('account.login'), {
            'email': 'testuser@example.com',
            'password': 'password',
        })
        self.assertRedirects(response, reverse('video.list'))

    def test_account_logout_view_get(self):
        response = self.client.get(reverse('account.logout'))
        self.assertEquals(response.status_code, 405)

    def test_account_logout_view_post(self):
        response = self.client.post(reverse('account.logout'))
        self.assertRedirects(response, reverse('account.login'))

    def test_account_activate_view_get(self):
        self.user.generate_token()
        self.user.save()

        response = self.client.get(reverse('account.activate', args=[self.user.token]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-activate.html')

    def test_account_activate_view_post_invalid(self):
        self.user.generate_token()
        self.user.save()

        response = self.client.post(reverse('account.activate', args=[self.user.token]), {
            'password1': '1234',
            'password2': '5678',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-activate.html')

    def test_account_activate_view_post(self):
        self.user.generate_token()
        self.user.save()

        response = self.client.post(reverse('account.activate', args=[self.user.token]), {
            'password1': '12345678',
            'password2': '12345678',
        })
        self.assertRedirects(response, reverse('video.list'))

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('12345678'))
        self.assertFalse(user.token)
