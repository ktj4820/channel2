from io import BytesIO
import os

from PIL import Image
import requests

from channel2.core.utils import prepare_filepath
from channel2.settings import MEDIA_ROOT


month_to_season = {
    1: 'Winter',
    2: 'Winter',
    3: 'Spring',
    4: 'Spring',
    5: 'Spring',
    6: 'Summer',
    7: 'Summer',
    8: 'Summer',
    9: 'Fall',
    10: 'Fall',
    11: 'Fall',
    12: 'Winter',
}

def download_cover(tag, cover_url):
    r = requests.get(cover_url)

    ext = Image.open(BytesIO(r.content)).format.lower()
    cover = 'covers/tag/{}.{}'.format(tag.slug, ext)
    cover_path = os.path.join(MEDIA_ROOT, cover)
    prepare_filepath(cover_path)

    with open(cover_path, 'wb') as f:
        f.write(r.content)

    return cover
