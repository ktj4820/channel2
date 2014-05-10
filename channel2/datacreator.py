import argparse
from collections import defaultdict
import datetime
import os
import random
import sys

PROJECT_PATH = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-2])
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'channel2.settings'

from channel2.account.models import User
from channel2.label.models import Label
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
        'USERS': 3,
        'VIDEOS': 100,
    },
    'test': {
        'VIDEOS': 1,
        'USERS': 0,
    }
}

LABELS = (
    ('Anime', (
        ('Accel World', None),
        ('Another', None),
        ('C3', None),
        ('Chuunibyou demo Koi ga Shitai!', None),
        ('Eureka 7: AO', None),
        ('Hyouka', None),
        ('Jormungand', None),
        ('Kokoro Connect', None),
        ('Magi', None),
        ('PSYCHO-PASS', None),
        ('Sword Art Online', None),
        ('Usagi Drop', None),
    )),
    ('Movies', None),
    ('Documentaries', None),
    ('TV Series', None),
)

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
    def create_labels(self):
        self.label_list = []
        def create_label_list(parent, label_list):
            if not label_list:
                return
            for i, (label, children) in enumerate(label_list):
                label = Label.objects.create(name=label, parent=parent, pinned=(not parent), order=i)
                self.label_list.append(label)
                create_label_list(label, children)
        create_label_list(None, LABELS)

    @timed
    def create_videos(self):
        label_list = Label.objects.get(name='Anime').children.all()
        video_dict = defaultdict(list)

        for i in range(self.config['VIDEOS']):
            label = random.choice(label_list)
            episode = len(video_dict[label.name]) + 1
            video = Video.objects.create(
                name='{} {:02d}'.format(label.name, episode),
                label=label,
            )
            video_dict[label.name].append(video)

    def run(self):
        print('-'*70)
        print('datacreator.py started')
        start = datetime.datetime.now()

        self.create_users()
        self.create_labels()
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
