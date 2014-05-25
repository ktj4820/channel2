from django.contrib import admin
from channel2.video.models import Video


class VideoAdmin(admin.ModelAdmin):

    list_display = ('name', 'views', 'tag_name', 'created_on')
    search_fields = ('name', 'tag__name',)
    ordering = ('-created_on',)

    def tag_name(self, obj):
        return obj.tag.name
    tag_name.short_description = 'Tag'

    def get_queryset(self, request):
        return Video.objects.all().select_related('tag')


admin.site.register(Video, VideoAdmin)
