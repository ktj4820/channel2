from django.conf.urls import url

from channel2.staff import views


urlpatterns = [

    url(r'^user/add/$',     views.StaffUserAddView.as_view(), name='staff.user.add'),

]
