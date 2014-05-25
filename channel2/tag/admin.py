from django.contrib import admin

from channel2.tag.models import Tag


class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'children_list', 'pinned', 'order',)
    list_filter = ('pinned',)
    search_fields = ('name', 'markdown',)
    ordering = ('name',)

    def children_list(self, obj):
        return ', '.join(sorted([t.name for t in obj.children.all()]))
    children_list.short_description = 'children'

    def get_queryset(self, request):
        return Tag.objects.all().prefetch_related('children')


admin.site.register(Tag, TagAdmin)
