import re

from Levenshtein import distance


def extract_name(filename):
    """
    Attempts to guess the name that should be used for a given filename.
    See video/tests.py for examples.
    """

    REGEX_LIST = (
        r'\](.*?)[\(\[\.]',
        r'(.*?).mp4',
    )

    for regex in REGEX_LIST:
        match = re.search(regex, filename)
        if match: return match.group(1).strip()

    return ''


def guess_tag(name, tag_list):
    """
    Use the name to guess the tag that should be applied. Returns a blank
    tag if the guessing fails.
    """

    r = {}
    for tag in tag_list:
        r[tag] = distance(name, tag)
    return min(r, key=r.get)
