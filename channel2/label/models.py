from django.db import models
from channel2.core.utils import slugify


class Label(models.Model):

    parent      = models.ForeignKey('self', null=True, blank=True, related_name='children')

    name        = models.CharField(max_length=100)
    slug        = models.SlugField(max_length=100, editable=False)

    markdown    = models.TextField(blank=True)
    html        = models.TextField(blank=True)
    pinned      = models.BooleanField(default=False)
    order       = models.PositiveSmallIntegerField(null=True, blank=True)

    created_on  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'label'
        ordering = ('slug',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:100] or '-'
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name
