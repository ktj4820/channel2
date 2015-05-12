from django.conf.urls import url

from channel2.search import views


urlpatterns = [

    url(r'^$',      views.SearchView.as_view(), name='search')

]
