from channel2.core.tests import BaseTestCase
from channel2.tag.utils import convert_season


class TestTagUtils(BaseTestCase):

    def test_convert_season_no_match(self):
        self.assertEqual('no match', convert_season('no match'))

    def test_convert_season(self):
        self.assertEqual('2015 1', convert_season('2015 Winter'))
        self.assertEqual('2015 2', convert_season('2015 Spring'))
        self.assertEqual('2015 3', convert_season('2015 Summer'))
        self.assertEqual('2015 4', convert_season('2015 Fall'))
