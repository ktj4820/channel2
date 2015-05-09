from django.conf.urls import url

from channel2.staff import views


urlpatterns = [

    url(r'^anime/add/$',    views.StaffAnimeAddView.as_view(), name='staff.anime.add'),
    url(r'^user/add/$',     views.StaffUserAddView.as_view(), name='staff.user.add'),

    url(r'^tag/(?P<id>\d+)/edit/$',     views.StaffTagEditView.as_view(), name='staff.tag.edit'),
    url(r'^tag/(?P<id>\d+)/video/$',    views.StaffTagVideoView.as_view(), name='staff.tag.video'),

]
