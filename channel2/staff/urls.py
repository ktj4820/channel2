from django.conf.urls import patterns, url
from channel2.staff.views import StaffUserAddView, StaffVideoImportView


urlpatterns = patterns('',

    url('^user/add/$',              StaffUserAddView.as_view(), name='staff.user.add'),
    url('^video/import/$',          StaffVideoImportView.as_view(), name='staff.video.import'),

)
