from django.core.urlresolvers import reverse
from channel2.account.models import User
from channel2.core.tests import BaseTestCase
from channel2.staff.forms import StaffAccountCreateForm


class StaffAccountCreateFormTests(BaseTestCase):

    def test_staff_account_create_form(self):
        form = StaffAccountCreateForm(data={
            'email': 'newuser@example.com',
        })
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.token)
        self.assertTrue(user.password)

    def test_staff_account_create_form_duplicate_email(self):
        form = StaffAccountCreateForm(data={
            'email': 'testuser@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['That email address is already registered.'])


class StaffUserListViewTests(BaseTestCase):

    def test_staff_user_list_view_get(self):
        response = self.client.get(reverse('staff.user.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user-list.html')

    def test_staff_user_list_view_post_invalid(self):
        response = self.client.post(reverse('staff.user.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user-list.html')

    def test_staff_user_list_view_post(self):
        response = self.client.post(reverse('staff.user.list'), {
            'email': 'newuser@example.com',
        })
        self.assertRedirects(response, reverse('staff.user.list'))
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
