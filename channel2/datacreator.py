from collections import defaultdict
import datetime, os, random, sys
from channel2.label.models import Label

sys.path.append(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0])
os.environ['DJANGO_SETTINGS_MODULE'] = 'channel2.settings'

from channel2.account.models import User
from channel2.video.models import Video

#-------------------------------------------------------------------------------

DEFAULT_CONF = {
    'NUM_USERS': 3,
    'NUM_VIDEOS': 100,
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

    def __init__(self, conf=DEFAULT_CONF):
        self.conf = conf
        self.start = None
        self.end = None

    def datacreator_start(self):
        print('----------------------')
        print('datacreator.py started')
        self.start = datetime.datetime.now()

    def datacreator_end(self):
        self.end = datetime.datetime.now()
        print('datacreator.py finished in %s' % (self.end-self.start))
        print('-----------------------')

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

    #---------------------------------------------------------------------------

    @timed
    def create_users(self):
        self.user = User(email='testuser@example.com', first_name='Test', last_name='User', is_staff=True)
        self.user.set_password('password')
        self.user.save()

        self.user_list = []
        for i in range(1, self.conf['NUM_USERS']+1):
            user = User(email='testuser{}@example.com'.format(i), first_name='Test{}'.format(i), last_name='User',)
            user.set_password('password')
            user.save()
            self.user_list.append(user)

        return self.user

    @timed
    def create_labels(self):

        def create_tag_list(parent, tag_list):
            if not tag_list: return
            for i, (tag, children) in enumerate(tag_list):
                tag = Label.objects.create(tag=tag, parent=parent, pinned=(not parent), order=i)
                create_tag_list(tag, children)

        create_tag_list(None, LABELS)

    @timed
    def create_videos(self):
        tag_list = Label.objects.get(tag='Anime').children.all()
        video_dict = defaultdict(list)

        for i in range(self.conf['NUM_VIDEOS']):
            tag = random.choice(tag_list)
            episode = len(video_dict[tag.tag]) + 1
            video = Video.objects.create(
                name='{} {:02d}'.format(tag.tag, episode),
                tag=tag,
            )
            video_dict[tag.tag].append(video)

    #---------------------------------------------------------------------------

    def run(self):
        self.datacreator_start()

        self.create_users()
        self.create_labels()
        self.create_videos()

        self.datacreator_end()


if __name__ == '__main__':
    dc = DataCreator()
    dc.run()

