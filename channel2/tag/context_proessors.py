from channel2.tag.models import Tag


def pinned_tags(request):
    """
    Enables {{ PINNED_TAGS }} to be used in templates.
    """

    return {
        'PINNED_TAGS': Tag.objects.filter(pinned=True).order_by('order'),
    }
