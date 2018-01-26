from django.conf.urls import url
from .views import home, register, profile_view, EditUserProfileView, change_password, project_list, project_create, \
    project_update, project_delete, project_view, project_bid_list, project_bid_create, project_bid_update, \
    project_bid_delete, project_assign

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^register/', register),
    url(r'^profile/$', profile_view, name='profile'),
    url(r'^users/(?P<pk>\d+)/edit/$', EditUserProfileView.as_view(), name="edit-user-profile"),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^projects/$', project_list, name='project_list'),
    url(r'^project/new$', project_create, name='project_new'),
    url(r'^project/(?P<pk>\d+)$', project_view, name='project_view'),
    url(r'^project/edit/(?P<pk>\d+)$', project_update, name='project_edit'),
    url(r'^project/delete/(?P<pk>\d+)$', project_delete, name='project_delete'),
    url(r'^project/assign/(?P<pk>\d+)$', project_assign, name='project_assign'),
    url(r'^project_bids/$', project_bid_list, name='project_bid_list'),
    url(r'^project/(\d+)/project_bid/new$', project_bid_create, name='project_bid_new'),
    url(r'^project_bid/edit/(?P<pk>\d+)$', project_bid_update, name='project_bid_edit'),
    url(r'^project_bid/delete/(?P<pk>\d+)$', project_bid_delete, name='project_bid_delete'),
]