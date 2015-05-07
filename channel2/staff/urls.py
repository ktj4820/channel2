from django.conf.urls import url

from channel2.staff import views


urlpatterns = [

    url(r'^user/add/$',     views.StaffUserAddView.as_view(), name='staff.user.add'),
    url(r'^anime/add/$',    views.StaffAnimeAddView.as_view(), name='staff.anime.add'),

]
