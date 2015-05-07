import datetime
import sys

from django.core.management.base import BaseCommand

from channel2.account.models import User
from channel2.tag.enums import TagType
from channel2.tag.models import Tag
from channel2.video.models import Video


anime_json = {
    "id": 1,
    "mal_id": 1,
    "slug": "cowboy-bebop",
    "status": "Finished Airing",
    "url": "https://hummingbird.me/anime/cowboy-bebop",
    "title": "Cowboy Bebop",
    "alternate_title": "",
    "episode_count": 26,
    "episode_length": 24,
    "cover_image": "https://static.hummingbird.me/anime/poster_images/000/000/001/large/Qe7VBIT.jpg?1425424889",
    "synopsis": "Enter a world in the distant future, where Bounty Hunters roam the solar system. Spike and Jet, bounty hunting partners, set out on journeys in an ever struggling effort to win bounty rewards to survive.\r\nWhile traveling, they meet up with other very interesting people. Could Faye, the beautiful and ridiculously poor gambler, Edward, the computer genius, and Ein, the engineered dog be a good addition to the group?",
    "show_type": "TV",
    "started_airing": "1998-04-03",
    "finished_airing": "1999-04-24",
    "community_rating": 4.50339744631209,
    "age_rating": "R17+",
    "genres": [
        {"name": "Action"},
        {"name": "Adventure"},
        {"name": "Comedy"},
        {"name": "Drama"},
        {"name": "Sci-Fi"},
        {"name": "Space"}
    ]
}



def timed(func):
    """
    use @timed to decorate a function that will print out the time it took
    for this function to run.
    """

    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        sys.stdout.write('\t{} '.format(func.__name__))
        sys.stdout.flush()
        result = func(*args, **kwargs)
        finish = datetime.datetime.now()
        sys.stdout.write('- {}\n'.format(finish - start))
        return result

    return inner


class Command(BaseCommand):

    @timed
    def create_users(self):
        def create_user_helper(email, name, is_active=True, **kwargs):
            user = User(email=email, name=name, is_active=is_active, **kwargs)
            user.set_password('password')
            user.save()
            return user

        self.user = create_user_helper('testuser@example.com', 'Test User')
        self.staff_user = create_user_helper('staffuser@example.com', 'Staff User', is_staff=True)

    @timed
    def create_tags(self):
        pinned_tag = Tag.objects.create(name='1998 Spring')

        genre_list = ['Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi', 'Space']
        tag_list = []
        for genre in genre_list:
            tag_list.append(Tag.objects.create(name=genre))

        anime = Tag.objects.create(
            name='Cowboy Bebop',
            slug='cowboy-bebop',
            type=TagType.ANIME,
            json=anime_json,
            cover='/cover/cowboy-bebop.jpg',
        )
        anime.children.add(pinned_tag, *tag_list)
        self.tag = anime

    @timed
    def create_videos(self):
        video_list = []
        for i in range(1, 25):
            video_list.append(Video(
                file='/video/cowboy-bebop/cowboy-bebop-{}'.format(i),
                name='Cowboy Bebop {}'.format(i),
                tag=self.tag,
            ))
        Video.objects.bulk_create(video_list)

    def handle(self, *args, **options):
        print('-'*70)
        print('datacreator.py started')
        start = datetime.datetime.now()

        self.create_users()
        self.create_tags()
        self.create_videos()

        finish = datetime.datetime.now()
        print('datacreator.py finished in {}'.format(finish-start))
        print('-'*70)
