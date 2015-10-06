from channel2.core.tests import BaseTestCase
from channel2.video.utils import get_episode


class VideoUtilTests(BaseTestCase):

    def test_get_episode(self):
        TEST_CASES = (
            ('a-certain-magical-index-01.mp4', '01'),
            ('[HorribleSubs] Mekakucity Actors - 07 [1080p].mp4', '07'),
            ('[Doki] Saki - 06 (848x480 h264 DVD AAC) [EAE93A6F].mp4', '06'),
            ('[UTW]_Fate_Zero_-_01_[BD][h264-720p_AC3][02A0491D].mp4', '01'),
            ('[Hiryuu] Maji de Watashi ni Koi Shinasai!! 03 [BD Hi10P 1280x720 H264 AAC] [B630C11B].mp4', '03'),
            ('[Exiled-Destiny]_Gate_Keepers_Ep02_(44D7406A)', '02')
        )

        for filename, expected in TEST_CASES:
            actual = get_episode(filename)
            self.assertEqual(expected, actual, filename)
