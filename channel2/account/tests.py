from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class AccountLoginViewTests(BaseTestCase):

    def test_account_login_view_get(self):
        response = self.client.get(reverse('account.login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account-login.html')
