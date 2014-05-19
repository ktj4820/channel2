from django.conf.urls import patterns, url

from channel2.staff.views import *


urlpatterns = patterns('',

    url('^users/$',         StaffUserListView.as_view(), name='staff.user.list'),

)
