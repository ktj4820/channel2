from unittest import mock

from channel2.core.management.commands.datacreator import anime_json
from channel2.core.tests import BaseTestCase
from channel2.staff.forms import StaffUserAddForm, StaffAnimeAddForm, StaffTagForm
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


class StaffTagFormTests(BaseTestCase):

    def test_tag_form_create(self):
        form = StaffTagForm(data={
            'name': 'New Tag',
            'type': 'common',
            'markdown': 'Some markdown for the new tag.',
        })
        self.assertTrue(form.is_valid(), form.errors)
        tag = form.save()

        self.assertEqual(tag.name, 'New Tag')
        self.assertEqual(tag.markdown, 'Some markdown for the new tag.')
        self.assertEqual(tag.html, '<p>Some markdown for the new tag.</p>')

    def test_tag_form_create_name_with_comma(self):
        form = StaffTagForm(data={
            'name': 'New Tag, with comma',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [StaffTagForm.error_messages['name_has_comma']])

    def test_tag_form_create_children_not_exists(self):
        form = StaffTagForm(data={
            'name': 'New Tag',
            'children': 'Invalid Tag',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['children'], [StaffTagForm.error_messages['tag_not_found'].format('Invalid Tag')])

    def test_tag_form_create_children(self):
        form = StaffTagForm(data={
            'name': 'New Tag',
            'type': 'common',
            'children': ', '.join([tag.name for tag in Tag.objects.all()]),
        })
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEqual(set(tag.children.all()), set(Tag.objects.all().exclude(id=tag.id)))

        form = StaffTagForm(instance=tag, data={
            'name': 'New Tag',
            'type': 'common',
            'children': '',
        })
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEqual(set(tag.children.all()), set())
