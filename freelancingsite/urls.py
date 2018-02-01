from django.conf.urls import url
from .views import EditUserProfileView, project_delete, project_bid_delete, project_assign, Home, Register, ViewProfile, ChangePassword, ProjectList, ViewProject, \
    UpdateProject, ListOfProjectBids, UpdateBidForProject, CreateProject, CreateBidForProject

urlpatterns = [
    url(r'^$', Home.as_view(), name="home"),
    url(r'^register/', Register.as_view()),
    url(r'^profile/$', ViewProfile.as_view(), name='profile'),
    url(r'^users/(?P<pk>\d+)/edit/$', EditUserProfileView.as_view(), name="edit-user-profile"),
    url(r'^password/$', ChangePassword.as_view(), name='change_password'),
    url(r'^projects/$', ProjectList.as_view(), name='project_list'),
    url(r'^project/new$', CreateProject.as_view(), name='project_new'),
    url(r'^project/(?P<pk>\d+)$', ViewProject.as_view(), name='project_view'),
    url(r'^project/edit/(?P<pk>\d+)$', UpdateProject.as_view(), name='project_edit'),
    url(r'^project/delete$', project_delete, name='project_delete'),
    url(r'^project/assign/(?P<pk>\d+)$', project_assign, name='project_assign'),
    url(r'^project_bids/$', ListOfProjectBids.as_view(), name='project_bid_list'),
    url(r'^project/(?P<project_id>\d+)/project_bid/new$', CreateBidForProject.as_view(), name='project_bid_new'),
    url(r'^project_bid/edit/(?P<pk>\d+)$', UpdateBidForProject.as_view(), name='project_bid_edit'),
    url(r'^project_bid/delete$', project_bid_delete, name='project_bid_delete'),
]

