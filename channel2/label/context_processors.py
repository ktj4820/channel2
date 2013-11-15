from channel2.label.models import Label
from channel2.video.models import Video


def pinned_labels(request):
    context = {
        'PINNED_LABELS': Label.objects.filter(pinned=True).order_by('order')
    }

    if request.user.is_staff:
        context['UNLABELED_COUNT'] = Video.objects.filter(label=None).count()

    return context
