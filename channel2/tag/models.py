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

    children    = models.ManyToManyField('self', symmetrical=False, null=True, blank=True, related_name='parents', editable=False)
    users       = models.ManyToManyField(User, null=True, blank=True, related_name='pinned_tags', editable=False)

    updated_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey(User, null=True, blank=True, editable=False)

    class Meta:
        db_table = 'tag'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:100] or '-'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


#-------------------------------------------------------------------------------
# Unmanaged join tables
#-------------------------------------------------------------------------------


class TagChildren(models.Model):

    parent  = models.ForeignKey(Tag, db_column='from_tag_id', related_name='+')
    child   = models.ForeignKey(Tag, db_column='to_tag_id', related_name='+')

    class Meta:
        db_table = 'tag_children'
        managed = False
        verbose_name_plural = 'Tag children'
