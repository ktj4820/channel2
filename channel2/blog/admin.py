from django.contrib import admin
from channel2.blog.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):

    list_display = ('title', 'created_on', 'created_by')
    search_fields = ('title',)
    ordering = ('-created_by',)


admin.site.register(BlogPost, BlogPostAdmin)
