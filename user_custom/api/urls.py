from django.urls import re_path

from user_custom.api import views

app_name = "users_api"
urlpatterns = [

    # ------------------------------------------------------
    re_path(r'^$', views.UsersApiCreateRead.as_view({"get": "get_all_user"}), name='get_user'),
    re_path(r'^create_user/$', views.UsersApiCreateRead.as_view({"post": "create_user"}), name='create_user'),
    re_path(r'^user/(?P<pk>[0-9]+)/$', views.UsersApiCreateRead.as_view({"get": "specific_user"}), name='specific_user'),
    re_path(r'^user/delete/(?P<pk>[0-9]+)/$', views.UsersApiCreateRead.as_view({"delete": "delete_user"}),
        name='delete_user'),
    re_path(r'^user/edit/$', views.UsersApiCreateRead.as_view({"put": "edit_user"}), name='edit_user'),
    # ____________________________________________________________________
    re_path(r'^log_in/$', views.UsersApiCreateRead.as_view({"get": "get_current_user"}), name='get_current_user'),


]
