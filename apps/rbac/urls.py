from django.urls import path, include
from .views import UserListView, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename="users")

urlpatterns = [
    path(r'api/', include(router.urls)),
    path('/list', UserListView.as_view(), name='user_list'),
]
