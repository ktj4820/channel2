from django.conf.urls import url

from channel2.staff import views


urlpatterns = [

    url(r'^anime/add/$',                    views.StaffAnimeAddView.as_view(), name='staff.anime.add'),

    url(r'^tag/add/$',                      views.StaffTagAddView.as_view(), name='staff.tag.add'),
    url(r'^tag/(?P<id>\d+)/edit/$',         views.StaffTagEditView.as_view(), name='staff.tag.edit'),
    url(r'^tag/(?P<id>\d+)/delete/$',       views.StaffTagDeleteView.as_view(), name='staff.tag.delete'),
    url(r'^tag/(?P<id>\d+)/video/$',        views.StaffTagVideoView.as_view(), name='staff.tag.video'),
    url(r'^tag/(?P<id>\d+)/video/add/$',    views.StaffTagAddVideoView.as_view(), name='staff.tag.video.add'),
    url(r'^tag/autocomplete.json',          views.StaffTagAutocompleteView.as_view(), name='staff.tag.autocomplete'),

    url(r'^user/add/$',                     views.StaffUserAddView.as_view(), name='staff.user.add'),

]
