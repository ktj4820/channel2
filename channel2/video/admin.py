from django.contrib import admin
from channel2.video.models import Video, VideoLink


class VideoAdmin(admin.ModelAdmin):

    list_display = ('name', 'views', 'tag_name', 'created_on')
    search_fields = ('name', 'tag__name',)
    ordering = ('-created_on',)

    def tag_name(self, obj):
        return obj.tag.name
    tag_name.short_description = 'Tag'

    def get_queryset(self, request):
        return Video.objects.all().select_related('tag')


class VideoLinkAdmin(admin.ModelAdmin):

    list_display = ('video', 'created_by', 'created_on', 'ip_address')
    search_fields = ('video__name', 'created_by__email')
    ordering = ('-created_on',)


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoLink, VideoLinkAdmin)
