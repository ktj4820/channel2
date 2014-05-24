import re

from Levenshtein import distance


def extract_name(filename):
    """
    Attempts to guess the name that should be used for a given filename.
    Returns a blank name if it fails. See video/tests.py for examples.
    """

    match = re.search(r'\](.*?)[\(\[\.]', filename)
    if not match:
        return ''

    name = match.group(1)
    name = name.strip()
    return name


def guess_label(name, tag_list):
    """
    Use the name to guess the label that should be applied. Returns a blank
    label if the guessing fails.
    """

    r = {}
    for tag in tag_list:
        r[tag] = distance(name, tag)
    return min(r, key=r.get)
