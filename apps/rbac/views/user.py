from ..models import User
from django.contrib.auth.hashers import check_password
from ..serializers.user_serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer, UserInfoListSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from rest_framework import status
from ..utils import *

class UserViewSet(ModelViewSet):
    '''
    用户管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'user_all'}, {'get': 'user_list'}, {'post': 'user_create'}, {'put': 'user_edit'},
                 {'delete': 'user_delete'})
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'phone')
    ordering_fields = ('id',)
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        # 给密码加盐
        salt = createSalt()
        request.data['password'] = createMD5(request.data['password'], salt)
        request.POST._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(data=None, status=status.HTTP_201_CREATED, headers=headers,msg="注册成功")

    def destroy(self, request, *args, **kwargs):
        # 删除用户时删除其他表关联的用户
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoListSerializer
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name',)
    ordering_fields = ('id',)
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)