from channel2.settings import RESOURCE_VERSION


def resource_version(request):
    return {
        'RESOURCE_VERSION': RESOURCE_VERSION,
    }
