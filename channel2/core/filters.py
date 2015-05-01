import hashlib


def gravatar_url(email):
    """
    returns the url to a gravatar profile image
    https://en.gravatar.com/site/implement/images/python/
    """

    email = email.encode()
    email_hash = hashlib.md5(email.lower()).hexdigest()
    url = '//www.gravatar.com/avatar/{}?d=mm'.format(email_hash)
    return url
