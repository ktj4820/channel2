from channel2 import settings


def resource_version(request):
    return {
        'RESOURCE_VERSION': settings.RESOURCE_VERSION
    }
