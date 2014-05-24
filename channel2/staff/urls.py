from django.conf.urls import patterns, url

from channel2.staff.views import *


urlpatterns = patterns('',

    url('^user/add/$',          StaffUserAddView.as_view(), name='staff.user.add'),
    url('^video/add/$',         StaffVideoAddView.as_view(), name='staff.video.add'),

)
