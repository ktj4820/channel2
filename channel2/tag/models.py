from django.db import models
from channel2.account.models import User
from channel2.core.utils import slugify


class Tag(models.Model):

    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(max_length=100, db_index=True)
    markdown    = models.TextField(blank=True)
    html        = models.TextField(blank=True)
    pinned      = models.BooleanField(default=False)
    order       = models.PositiveSmallIntegerField(null=True, blank=True)

    tags        = models.ManyToManyField('self')

    updated_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        db_table = 'tag'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:100] or '-'
        super().save(*args, **kwargs)

    def __unicode__(self):
        return self.name
