from django.conf.urls import url

from channel2.tag import views


urlpatterns = [

    url(r'^$',          views.TagListView.as_view(), name='tag.list'),
    url(r'^anime/$',    views.TagListAnimeView.as_view(), name='tag.list.anime'),
    url(r'^current/$',  views.TagCurrentView.as_view(), name='tag.current'),
    url(r'^random/$',   views.TagRandomView.as_view(), name='tag.random'),

    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',                         views.TagView.as_view(), name='tag'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<video_id>\d+)/$',       views.TagView.as_view(), name='tag.video'),

]
