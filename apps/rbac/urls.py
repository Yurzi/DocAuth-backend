from django.urls import path, re_path
from .views.user import UserListView, UserDetailView, UserRegisterView, login


urlpatterns = [
    path('/user',
         UserRegisterView.as_view(), name='user_create'),
    path('/user/<int:pk>',
         UserDetailView.as_view(), name='user_detail'),
    path('/user/list', UserListView.as_view(), name='user_list'),
    path('/user/login', login, name='user_login'),
]
