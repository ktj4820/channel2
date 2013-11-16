from django.conf.urls import patterns, url
from channel2.flat.views import FlatHelpView

urlpatterns = patterns('',

    url(r'^help/$',         FlatHelpView.as_view(), name='flat.help'),

)
