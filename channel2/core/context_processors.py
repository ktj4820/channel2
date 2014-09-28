import hashlib

from channel2.settings import RESOURCE_VERSION


def resource_version(request):
    context = {
        'RESOURCE_VERSION': RESOURCE_VERSION,
    }
    if request.user.is_authenticated():
        context['GRAVATAR_HASH'] = hashlib.md5(request.user.email.encode('utf-8')).hexdigest()
    return context
