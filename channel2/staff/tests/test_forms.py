from unittest import mock

from channel2.core.management.commands.datacreator import anime_json
from channel2.core.tests import BaseTestCase
from channel2.staff.forms import StaffUserAddForm, StaffAnimeAddForm
from channel2.tag.enums import TagType
from channel2.tag.models import Tag


class MockResponse:

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class StaffUserAddFormTests(BaseTestCase):

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
        self.assertEqual(form.errors['email'], [StaffUserAddForm.error_messages['email_exists']])


class StaffAnimeAddFormTests(BaseTestCase):

    @mock.patch('channel2.staff.forms.requests')
    def test_clean_hummingbird_id_duplicate(self, mock_requests):
        mock_requests.get.return_value = MockResponse(anime_json)
        form = StaffAnimeAddForm(data={'hummingbird_id': '1'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['hummingbird_id'], ['"Cowboy Bebop" already exists'])

    @mock.patch('channel2.staff.forms.download_cover')
    @mock.patch('channel2.staff.forms.requests')
    def test_save(self, mock_requests, mock_download_cover):
        Tag.objects.all().delete()

        mock_requests.get.return_value = MockResponse(anime_json)
        mock_download_cover.return_value = '/new/path/to/cover'
        form = StaffAnimeAddForm(data={'hummingbird_id': '1'})
        self.assertTrue(form.is_valid())

        tag = form.save()
        self.assertEqual(tag.name, 'Cowboy Bebop')
        self.assertEqual(tag.slug, 'cowboy-bebop')
        self.assertEqual(tag.json, anime_json)
        self.assertEqual(tag.type, TagType.ANIME)
        self.assertTrue(Tag.objects.get(name='Action') in tag.children.all())


