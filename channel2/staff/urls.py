from django.conf.urls import patterns, url

from channel2.staff.views import StaffUserAddView


urlpatterns = patterns('',

    url(r'^users/add/$',            StaffUserAddView.as_view(), name='staff.user.add'),

)
