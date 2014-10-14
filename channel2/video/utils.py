import re


def extract_name(filename):
    """
    Attempts to guess the name that should be used for a given filename.
    See video/tests.py for examples.
    """

    REGEX_LIST = (
        r'\](.*?)[\(\[]',
        r'(.*?).mp4',
    )

    for regex in REGEX_LIST:
        match = re.search(regex, filename)
        if match:
            return match.group(1).replace('_', ' ').strip()

    return ''
