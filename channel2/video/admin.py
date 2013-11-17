from django.contrib import admin
from channel2.video.models import Video, VideoLink


class VideoAdmin(admin.ModelAdmin):

    list_display = ('name', 'views', 'label', 'created_on',)
    search_fields = ('name', 'label',)
    ordering = ('-created_on',)


class VideoLinkAdmin(admin.ModelAdmin):

    list_display = ('created_by', 'video', 'ip_address', 'key', 'created_on',)
    search_fields = ('ip_address', 'video', 'key',)
    ordering = ('-created_on',)


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoLink, VideoLinkAdmin)
