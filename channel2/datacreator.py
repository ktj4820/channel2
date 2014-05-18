import argparse
import datetime
import os
import random
import sys

PROJECT_PATH = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-2])
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'channel2.settings'

from channel2.account.models import User
from channel2.core.utils import slugify
from channel2.tag.models import Tag
from channel2.video.models import Video

import django
django.setup()

#-------------------------------------------------------------------------------

def timed(func):
    """
    use @timed to decorate a function that will print out the time it took
    for this function to run.
    """

    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        finish = datetime.datetime.now()
        print('\t{} - {}'.format(func.__name__, finish-start))
        return result
    return inner

#-------------------------------------------------------------------------------

CONFIGURATION = {
    'default': {
        'TAGS': 100,
        'TAGS_PINNED': 5,
        'TAG_RELATION_FACTOR': (0, 5),
        'USERS': 3,
        'VIDEOS': 100,
    },
    'test': {
        'TAGS': 1,
        'TAGS_PINNED': 1,
        'TAG_RELATION_FACTOR': (1, 1),
        'USERS': 0,
        'VIDEOS': 1,
    }
}

#-------------------------------------------------------------------------------


class DataCreator:

    def __init__(self, configuration):
        self.config = CONFIGURATION[configuration]

    @timed
    def create_users(self):
        self.user = User(email='testuser@example.com', is_staff=True)
        self.user.set_password('password')
        self.user.save()

        self.user_list = []
        for i in range(1, self.config['USERS']+1):
            user = User(email='testuser{}@example.com'.format(i))
            user.set_password('password')
            user.save()
            self.user_list.append(user)

        return self.user

    @timed
    def create_tags(self):
        tag_list = []
        for i in range(1, self.config['TAGS_PINNED']+1):
            name = 'Pinned Tag {}'.format(i)
            slug = slugify(name)
            tag_list.append(Tag(name=name, slug=slug, pinned=True))
        for i in range(1, self.config['TAGS']+1):
            name = 'Tag {}'.format(i)
            slug = slugify(name)
            tag_list.append(Tag(name=name, slug=slug))
        Tag.objects.bulk_create(tag_list)

        tag_list = set(Tag.objects.all())
        for tag in tag_list:
            count = random.randint(*self.config['TAG_RELATION_FACTOR'])
            tag.children.add(*random.sample(tag_list, count))

    @timed
    def create_videos(self):
        tag_list = list(Tag.objects.all())
        video_list = []
        for i in range(1, self.config['VIDEOS']+1):
            name = 'Video {}'.format(i)
            slug = slugify(name)
            video_list.append(Video(name=name, slug=slug, tag=random.choice(tag_list)))
        Video.objects.bulk_create(video_list)

    def run(self):
        print('-'*70)
        print('datacreator.py started')
        start = datetime.datetime.now()

        self.create_users()
        self.create_tags()
        self.create_videos()

        finish = datetime.datetime.now()
        print('datacreator.py finished in {}'.format(finish-start))
        print('-'*70)


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Datacreator utility for Channel2')
    parser.add_argument('--config', dest='config', default='default', help='specify the configuration for datacreator to use (optional)')
    arg_dict = vars(parser.parse_args())

    dc = DataCreator(arg_dict['config'])
    dc.run()
