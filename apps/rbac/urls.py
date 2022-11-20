from django.urls import path, include
from .views.user import UserListView, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename="user")

urlpatterns = [
    path('/', include(router.urls)),
    path('/user/list', UserListView.as_view(), name='user_list'),
]
