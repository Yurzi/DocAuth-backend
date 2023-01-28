from django.urls import path, re_path
from .views.user import UserListView, UserDetailView, UserRegisterView, login
#from .views.test import test
from .views.Role import Role_FunctionView

urlpatterns = [
    path('/user/',
         UserRegisterView.as_view(), name='user_create'),
    path('/user/<int:pk>/',
         UserDetailView.as_view(), name='user_detail'),
    path('/user/list/', UserListView.as_view(), name='user_list'),
    path('/user/login/', login, name='user_login'),
    #path('/test/', test, name='test'),
    path('/permission/role/delfunction/',Role_FunctionView.as_view()),
    path('/permission/role/updfunction/',Role_FunctionView.as_view())
]
