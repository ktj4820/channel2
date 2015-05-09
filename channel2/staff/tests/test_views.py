from unittest import mock

from django.core.urlresolvers import reverse

from channel2.account.models import User
from channel2.core.tests import BaseTestCase
from channel2.tag.models import Tag


class BaseStaffTests(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.staff_user = User.objects.get(email='staffuser@example.com')
        logged_in = self.client.login(email=self.staff_user.email, password=self.staff_user.password)
        self.assertTrue(logged_in)


class StaffUserAddViewTests(BaseStaffTests):

    def test_staff_user_add_view_get_not_staff(self):
        self.client.login(email=self.user.email, password=self.user.password)
        response = self.client.get(reverse('staff.user.add'))
        self.assertEqual(response.status_code, 404)

    def test_staff_user_add_view_get(self):
        response = self.client.get(reverse('staff.user.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user-add.html')

    def test_staff_user_add_view_post_invalid(self):
        response = self.client.post(reverse('staff.user.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user-add.html')

    def test_staff_user_add_view_post(self):
        response = self.client.post(reverse('staff.user.add'), {
            'email': 'newuser@example.com',
        })
        self.assertRedirects(response, reverse('staff.user.add'))

        user = User.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.token)


class StaffAnimeAddViewTests(BaseStaffTests):

    def test_staff_anime_add_view_get(self):
        response = self.client.get(reverse('staff.anime.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-anime-add.html')

    @mock.patch('channel2.staff.views.StaffAnimeAddForm')
    def test_staff_anime_add_view_post_invalid(self, mock_form_cls):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = False
        mock_form.errors = []
        mock_form_cls.return_value = mock_form
        response = self.client.post(reverse('staff.anime.add'))
        self.assertRedirects(response, reverse('staff.anime.add'))

    @mock.patch('channel2.staff.views.StaffAnimeAddForm')
    def test_staff_anime_add_view_post(self, mock_form_cls):
        tag = Tag.objects.get(name='Cowboy Bebop')

        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = tag
        mock_form_cls.return_value = mock_form

        response = self.client.post(reverse('staff.anime.add'))
        self.assertRedirects(response, reverse('tag', args=[tag.id, tag.slug]))