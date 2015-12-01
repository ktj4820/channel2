from io import BytesIO
import os
import re

from PIL import Image
import requests

from channel2.core.utils import prepare_filepath
from channel2.settings import MEDIA_ROOT


month_to_season = {
    1: 'Winter',
    2: 'Winter',
    3: 'Winter',
    4: 'Spring',
    5: 'Spring',
    6: 'Spring',
    7: 'Summer',
    8: 'Summer',
    9: 'Summer',
    10: 'Fall',
    11: 'Fall',
    12: 'Fall',
}

season_order = {
    'Winter': 1,
    'Spring': 2,
    'Summer': 3,
    'Fall': 4,
}

season_re = re.compile(r'^(\d{4}) (Winter|Spring|Summer|Fall)$')


def convert_season(tag):
    match = season_re.match(tag)
    if not match: return tag

    year = match.group(1)
    season = season_order[match.group(2)]
    return '{} {}'.format(year, season)


def download_cover(tag, cover_url):
    r = requests.get(cover_url)

    ext = Image.open(BytesIO(r.content)).format.lower()
    cover = 'covers/tag/{}.{}'.format(tag.slug, ext)
    cover_path = os.path.join(MEDIA_ROOT, cover)
    prepare_filepath(cover_path)

    with open(cover_path, 'wb') as f:
        f.write(r.content)

    return cover
