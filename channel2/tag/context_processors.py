from channel2.tag.models import Tag


def pinned_tags(request):
    return {
        'PINNED_TAG_LIST': Tag.objects.filter(pinned=True),
    }
