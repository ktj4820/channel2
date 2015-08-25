import re


REGEX_LIST = (
    re.compile(r'.*-(?P<episode>\d{1,3})\.mp4'),
    re.compile(r'.*- (?P<episode>\d{1,3}) [\(\[].*'),
    re.compile(r'.*_(?P<episode>\d{1,3})_.*'),
    re.compile(r'.* (?P<episode>\d{1,3}) \[.*'),
)


def get_episode(filename):
    episode = ''

    for regex in REGEX_LIST:
        match = regex.match(filename)
        if match:
            return match.group('episode')

    return episode
