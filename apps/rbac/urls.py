from django.urls import path, re_path

from apps.rbac.views.function import FunctionListView
from apps.rbac.views.Role import Role_FunctionView, zqx_RView, zqxR_F1View
from apps.rbac.views.user import (UserDetailView, UserListView,
                                  UserRegisterView, WsUserView, login)

urlpatterns = [
    path("/user", UserRegisterView.as_view(), name="user_create"),
    path("/user/<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("/user/list", UserListView.as_view(), name="user_list"),
    path("/user/login", login, name="user_login"),
    path("/permission/role/delfunction/", Role_FunctionView.as_view()),
    path("/permission/role/updfunction/", Role_FunctionView.as_view()),
    path("/user/ids/", WsUserView.as_view()),
    path("/permission/role", Role_FunctionView.as_view()),
    path("/permisssion/role/list/", Role_FunctionView.as_view()),
    path("/permission/role/add/", Role_FunctionView.as_view()),
    path("/permission/role/oneRoleList/", zqxR_F1View.as_view()),
    path("/permission/role/ids/", zqxR_F1View.as_view()),
    path("/permission/role/upInfo/", zqxR_F1View.as_view()),
    path("/permission/role/delOne/", zqx_RView.as_view()),
    path("/permission/role/upstatus/", zqx_RView.as_view()),
    ## Function
    path("/permission/", FunctionListView.as_view()),
]
