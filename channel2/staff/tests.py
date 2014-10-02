from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


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
