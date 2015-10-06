import re

from Levenshtein import distance


EPISODE_REGEX_LIST = (
    re.compile(r'.*-(?P<episode>\d{1,3})\.mp4'),
    re.compile(r'.*- (?P<episode>\d{1,3}) [\(\[].*'),
    re.compile(r'.*_(?P<episode>\d{1,3})_.*'),
    re.compile(r'.* (?P<episode>\d{1,3}) \[.*'),
)


NAME_REGEX_LIST = (
    r'\](.*?)[\(\[\.]',
    r'(.*?).mp4',
)


def get_episode(filename):
    episode = ''
    for regex in EPISODE_REGEX_LIST:
        match = regex.match(filename)
        if match:
            return match.group('episode')
    return episode


def extract_name(filename):
    """
    Attempts to guess the name that should be used for a given filename.
    See video/tests.py for examples.
    """

    for regex in NAME_REGEX_LIST:
        match = re.search(regex, filename)
        if match: return match.group(1).strip()
    return ''


def guess_tag(filename, tag_list):
    """
    Use the name to guess the tag that should be applied. Returns a blank
    tag if the guessing fails.
    """

    r = {}
    for tag in tag_list:
        name = extract_name(filename) or filename
        r[tag] = distance(name, tag)
    return min(r, key=r.get)
