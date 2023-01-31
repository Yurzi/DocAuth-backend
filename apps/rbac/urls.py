from django.urls import path, re_path
from .views.user import UserListView, UserDetailView, UserRegisterView,WsUserView,WsUser_2_view, login
from .views.Role import Role_FunctionView,zqxR_F1View,zqx_RView,WRoleView
from .views.RoleUser import wsRUView
from .views.UserFunction import W_U_FView,W_U_FViewAll
from apps.rbac.views.function import FunctionListView, FunctionDetailView
from apps.rbac.views.api import ApiListView,ApiDetailView,ApiFunctionView
from apps.rbac.views.Role import Role_FunctionView, zqx_RView, zqxR_F1View
from apps.rbac.views.user import (UserDetailView, UserListView,
                                  UserRegisterView, WsUserView, login)
urlpatterns = [
    path('/user',
         UserRegisterView.as_view(), name='user_create'),
    path('/user/<int:pk>',
         UserDetailView.as_view(), name='user_detail'),
    path('/user/list', UserListView.as_view(), name='user_list'),
    path('/user/login', login, name='user_login'),
    path('/user/ids', WsUserView.as_view()),

    path('/user/page', WsUserView.as_view()),
    path('/user/upduser', WsUserView.as_view()),
    path('/permission/user/role', wsRUView.as_view()),
    path('/user/like', WsUser_2_view.as_view()),

    path('/permission/role/delfunction', Role_FunctionView.as_view()),
    path('/permission/role/updfunction', Role_FunctionView.as_view()),
    path('/permission/role/list', Role_FunctionView.as_view()),
    path('/permission/role/add', Role_FunctionView.as_view()),
    path('/permission/role/oneRoleList', zqxR_F1View.as_view()),
    path('/permission/role/ids', zqxR_F1View.as_view()),
    path('/permission/role/upInfo', zqxR_F1View.as_view()),
    path('/permission/role/delOne', zqx_RView.as_view()),
    path('/permission/role/upstatus', zqx_RView.as_view()),
    path('/permission/role/listall', WRoleView.as_view()),
    path('/permission/user/function', W_U_FView.as_view()),
    path('/permission/user/function/all', W_U_FViewAll.as_view()),
    path("/permission/role", Role_FunctionView.as_view()),

    # Function
    path("/permission", FunctionListView.as_view()),
    path("/permission/status", FunctionDetailView.as_view()),
    # Api
    path("/permission/api", ApiListView.as_view()),
    path("/permission/api/status", ApiDetailView.as_view()),
    path("/permission/api/function", ApiFunctionView.as_view())
]
