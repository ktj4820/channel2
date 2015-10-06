from unittest import mock

from channel2.core.tests import BaseTestCase
from channel2.staff.views import StaffVideoAddView
from channel2.video.models import Video


class StaffVideoFormSetTests(BaseTestCase):

    def test_clean_unique_filepaths(self):
        formset = StaffVideoAddView.get_formset_cls()(data={
            'form-0-ORDER': '1',
            'form-0-episode': '30',
            'form-0-filename': 'file1.mp4',
            'form-0-name': 'Cowboy Bebop - 30',
            'form-0-selected': 'on',
            'form-0-tag': 'Cowboy Bebop',
            'form-1-ORDER': '2',
            'form-1-episode': '30',
            'form-1-filename': 'file1.mp4',
            'form-1-name': 'Cowboy Bebop - 30',
            'form-1-selected': 'on',
            'form-1-tag': 'Cowboy Bebop',
            'form-INITIAL_FORMS': '2',
            'form-MAX_NUM_FORMS': '1000',
            'form-MIN_NUM_FORMS': '0',
            'form-TOTAL_FORMS': '2'
        })
        self.assertFalse(formset.is_valid())
        self.assertEqual(formset.non_form_errors(), ['Non-unique filepaths were generated from video names.'])

    def test_clean_filepaths_not_in_db(self):
        formset = StaffVideoAddView.get_formset_cls()(data={
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
        self.assertFalse(formset.is_valid())
        self.assertEqual(formset.non_form_errors(), ['Auto generated filepaths already exists in the database.'])

    @mock.patch('channel2.staff.formsets.shutil')
    def test_save(self, mock_shutil):
        formset = StaffVideoAddView.get_formset_cls()(data={
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
        self.assertTrue(formset.is_valid())
        formset.save()

        video = Video.objects.get(name='Cowboy Bebop - 30')
        self.assertEqual(video.tag.name, 'Cowboy Bebop')
        self.assertEqual(video.episode, '30')
        self.assertEqual(video.file, 'video/cowboy-bebop/cowboy-bebop-30.mp4')
        self.assertTrue(Video.objects.filter(name='Cowboy Bebop - 31').exists())


