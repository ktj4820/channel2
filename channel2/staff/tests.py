from django.core.urlresolvers import reverse

from channel2.account.models import User
from channel2.core.tests import BaseTestCase
from channel2.staff.forms import StaffUserAddForm


class StaffUserAddViewTests(BaseTestCase):

    def test_staff_user_add_view_get_not_staff(self):
        self.user.is_staff = False
        self.user.save()

        response = self.client.get(reverse('staff.user.add'))
        self.assertEqual(response.status_code, 404)

    def test_staff_user_add_view_get(self):
        response = self.client.get(reverse('staff.user.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user-add.html')

    def test_staff_user_add_view_post_invalid(self):
        response = self.client.post(reverse('staff.user.add'), {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user-add.html')

    def test_staff_user_add_view_post(self):
        response = self.client.post(reverse('staff.user.add'), {
            'email': 'newuser@example.com'
        })
        self.assertRedirects(response, reverse('staff.user.add'))

        user = User.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.token)


class StaffUserAddFormtests(BaseTestCase):

    def test_staff_user_add_form(self):
        form = StaffUserAddForm(data={
            'email': 'newuser@example.com',
        })
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.email, 'newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.token)

    def test_staff_user_add_form_email_exists(self):
        form = StaffUserAddForm(data={
            'email': 'testuser@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [StaffUserAddForm.error_messages['email.exists']])
