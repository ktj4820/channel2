import hashlib

from channel2.settings import DEBUG


def date(value, format='%Y/%m/%d %H:%M'):
    if not value:
        return ''
    return value.strftime(format)


def gravatar_url(email):
    """
    returns the url to a gravatar profile image
    https://en.gravatar.com/site/implement/images/python/
    """

    email = email.encode()
    email_hash = hashlib.md5(email.lower()).hexdigest()
    url = '//www.gravatar.com/avatar/{}?d=mm'.format(email_hash)
    return url


def imagepress(url):
    """
    returns an imagepress version of the URL
    """

    if DEBUG:
        return url

    return 'http://channel2.imagepress.io' + url
