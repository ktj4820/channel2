from django.conf.urls import url

from channel2.tag import views


urlpatterns = [

    url(r'^$',      views.TagListView.as_view(), name='tag.list'),

]
