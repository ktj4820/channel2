from unittest import mock

from django.core.urlresolvers import reverse

from channel2.account.models import User
from channel2.core.tests import BaseTestCase
from channel2.tag.enums import TagType
from channel2.tag.models import Tag
from channel2.video.models import Video


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
        self.assertEqual(response.status_code, 405)

    def test_staff_user_add_view_post_invalid(self):
        response = self.client.post(reverse('staff.user.add'))
        self.assertRedirects(response, reverse('staff.user'))

    def test_staff_user_add_view_post(self):
        response = self.client.post(reverse('staff.user.add'), {
            'email': 'newuser@example.com',
        })
        self.assertRedirects(response, reverse('staff.user'))

        user = User.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.token)


class StaffUserView(BaseStaffTests):

    def test_staff_user_view_get(self):
        response = self.client.get(reverse('staff.user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-user.html')


class StaffAnimeAddViewTests(BaseStaffTests):

    def test_staff_anime_add_view_get(self):
        response = self.client.get(reverse('staff.anime.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-anime-add.html')

    @mock.patch('channel2.staff.views.forms.StaffAnimeAddForm')
    def test_staff_anime_add_view_post_invalid(self, mock_form_cls):
        mock_form = mock.Mock()
        mock_form.is_valid.return_value = False
        mock_form.errors = []
        mock_form_cls.return_value = mock_form
        response = self.client.post(reverse('staff.anime.add'))
        self.assertRedirects(response, reverse('staff.anime.add'))

    @mock.patch('channel2.staff.views.forms.StaffAnimeAddForm')
    def test_staff_anime_add_view_post(self, mock_form_cls):
        tag = Tag.objects.get(name='Cowboy Bebop')

        mock_form = mock.Mock()
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = tag
        mock_form_cls.return_value = mock_form

        response = self.client.post(reverse('staff.anime.add'))
        self.assertRedirects(response, reverse('tag', args=[tag.id, tag.slug]))


class StaffTagAddViewTests(BaseStaffTests):

    def test_staff_tag_add_view_get(self):
        response = self.client.get(reverse('staff.tag.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-tag.html')
    
    def test_staff_tag_add_view_post_invalid(self):
        response = self.client.post(reverse('staff.tag.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-tag.html')

    def test_staff_tag_add_view_post(self):
        response = self.client.post(reverse('staff.tag.add'), {
            'name': 'New Tag',
            'type': TagType.ANIME,
            'markdown': 'Some markdown for the new tag.',
        })
        tag = Tag.objects.get(name='New Tag')
        self.assertRedirects(response, reverse('tag', args=[tag.id, tag.slug]))

        self.assertEqual(tag.type, TagType.ANIME)
        self.assertEqual(tag.markdown, 'Some markdown for the new tag.')
        self.assertEqual(tag.html, '<p>Some markdown for the new tag.</p>')
        self.assertFalse(tag.pinned)
        self.assertEqual(tag.order, None)


class StaffTagEditViewTests(BaseStaffTests):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.get(name='Action')

    def test_staff_tag_edit_view_get(self):
        response = self.client.get(reverse('staff.tag.edit', args=[self.tag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-tag.html')
    
    def test_staff_tag_edit_view_post_invalid(self):
        response = self.client.post(reverse('staff.tag.edit', args=[self.tag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-tag.html')
        
    def test_staff_tag_edit_view_post(self):
        response = self.client.post(reverse('staff.tag.edit', args=[self.tag.id]), {
            'name': 'New Tag Name',
            'type': TagType.COMMON,
            'markdown': 'Some new markdown for the tag',
        })
        tag = Tag.objects.get(id=self.tag.id)
        self.assertRedirects(response, reverse('tag', args=[tag.id, tag.slug]))

        self.assertEqual(tag.name, 'New Tag Name')
        self.assertEqual(tag.type, TagType.COMMON)
        self.assertEqual(tag.markdown, 'Some new markdown for the tag')
        self.assertEqual(tag.pinned, False)
        self.assertEqual(tag.order, None)
        self.assertEqual(tag.html, '<p>Some new markdown for the tag</p>')


class StaffTagAddVideoViewTests(BaseStaffTests):
    
    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.get(name='Action')

    def test_staff_tag_video_view_get(self):
        response = self.client.get(reverse('staff.tag.video.add', args=[self.tag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-tag-video-add.html')
    

class StaffTagVideoViewTests(BaseStaffTests):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.get(name='Action')
        self.video1 = Video.objects.create(file='test1.mp4', name='test1', tag=self.tag)
        self.video2 = Video.objects.create(file='test2.mp4', name='test2', tag=self.tag)

    def test_staff_tag_video_view_get(self):
        response = self.client.get(reverse('staff.tag.video', args=[self.tag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-tag-video.html')

    @mock.patch('channel2.video.models.remove_media_file')
    def test_staff_tag_video_view_post(self, mock_remove_media_file):
        response = self.client.post(reverse('staff.tag.video', args=[self.tag.id]), data={
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '2',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-DELETE': 'on',
            'form-0-id': self.video1.id,
            'form-0-name': 'test1',
            'form-1-episode': '02',
            'form-1-id': self.video2.id,
            'form-1-name': 'Test 2',
        })
        self.assertRedirects(response, reverse('staff.tag.video', args=[self.tag.id]))
        self.assertFalse(Video.objects.filter(id=self.video1.id).exists())

        video = Video.objects.get(id=self.video2.id)
        self.assertEqual(video.name, 'Test 2')
        self.assertEqual(video.episode, '02')
        self.assertEqual(mock_remove_media_file.call_count, 2)
        mock_remove_media_file.assert_has_any_call(self.video2.file)
        mock_remove_media_file.assert_has_any_call(self.video2.cover)


class StaffTagDeleteViewTests(BaseStaffTests):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.get(name='Action')

    def test_staff_tag_delete_view_get(self):
        response = self.client.get(reverse('staff.tag.delete', args=[self.tag.id]))
        self.assertEqual(response.status_code, 405)

    def test_staff_tag_delete_view_post(self):
        response = self.client.post(reverse('staff.tag.delete', args=[self.tag.id]))
        self.assertRedirects(response, reverse('tag.list'))
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())


class StaffVideoActivityViewTests(BaseStaffTests):

    def test_staff_video_activity_view_get(self):
        response = self.client.get(reverse('staff.video.activity'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-video-activity.html')


class StaffVideoAddViewTests(BaseStaffTests):

    def test_staff_video_add_view_get(self):
        response = self.client.get(reverse('staff.video.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-video-add.html')

    def test_staff_video_add_view_post_invalid(self):
        response = self.client.post(reverse('staff.video.add'), data={
            'form-0-ORDER': '1',
            'form-0-episode': '01',
            'form-0-filename': 'file1.mp4',
            'form-0-name': 'Cowboy Bebop - 01',
            'form-0-selected': 'on',
            'form-0-tag': 'Cowboy Bebop',
            'form-INITIAL_FORMS': '1',
            'form-MAX_NUM_FORMS': '1000',
            'form-MIN_NUM_FORMS': '0',
            'form-TOTAL_FORMS': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/staff-video-add.html')

    @mock.patch('channel2.staff.formsets.shutil')
    def test_staff_video_add_view_post(self, mock_shutil):
        response = self.client.post(reverse('staff.video.add'), data={
            'form-0-ORDER': '1',
            'form-0-episode': '30',
            'form-0-filename': 'file1.mp4',
            'form-0-name': 'Cowboy Bebop - 30',
            'form-0-selected': 'on',
            'form-0-tag': 'Cowboy Bebop',
            'form-1-ORDER': '2',
            'form-1-episode': '31',
            'form-1-filename': 'file2.mp4',
            'form-1-name': 'Cowboy Bebop - 31',
            'form-1-selected': 'on',
            'form-1-tag': 'Cowboy Bebop',
            'form-INITIAL_FORMS': '2',
            'form-MAX_NUM_FORMS': '1000',
            'form-MIN_NUM_FORMS': '0',
            'form-TOTAL_FORMS': '2'
        })
        self.assertRedirects(response, reverse('staff.video.add'))

        video = Video.objects.get(name='Cowboy Bebop - 30')
        self.assertEqual(video.tag.name, 'Cowboy Bebop')
        self.assertEqual(video.episode, '30')
        self.assertEqual(video.file, 'video/cowboy-bebop/cowboy-bebop-30.mp4')
        self.assertTrue(Video.objects.filter(name='Cowboy Bebop - 31').exists())
