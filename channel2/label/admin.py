from django.contrib import admin
from channel2.label.models import Label


class LabelAdmin(admin.ModelAdmin):

    list_display = ('name', 'parent', 'pinned', 'order',)
    list_filter = ('pinned',)
    search_fields = ('name',)
    ordering = ('-pinned', 'order', 'slug')


admin.site.register(Label, LabelAdmin)
