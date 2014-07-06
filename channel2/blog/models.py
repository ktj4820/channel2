from django.db import models
from channel2.account.models import User
from channel2.core.utils import slugify


class BlogPost(models.Model):

    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200)
    markdown    = models.TextField(blank=True)
    html        = models.TextField(blank=True)

    created_on  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(User, null=True, blank=True, editable=False)

    class Meta:
        db_table = 'blog_post'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:200] or '-'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
