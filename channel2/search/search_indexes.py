from haystack import indexes
from channel2.video.models import Video


class VideoIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Video

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related('label')
