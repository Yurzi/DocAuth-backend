from rest_framework.decorators import action
from rest_framework import views, status, viewsets,generics
from common.custom_exception import CustomException
from common.custom_response import CustomResponse
from rest_framework.parsers import JSONParser
from .models import User
from .serializers import UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''
    用户管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'user_all'}, {'get': 'user_list'}, {'post': 'user_create'}, {'put': 'user_edit'},
                 {'delete': 'user_delete'})
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_fields = ('is_active',)
    # search_fields = ('username', 'name', 'mobile', 'email')
    # ordering_fields = ('id',)
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserDetailSerializer
        elif self.action == 'list':
            return UserDetailSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        # 创建用户默认添加密码
        request.data['password'] = '123456'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # 删除用户时删除其他表关联的用户
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)

    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name',)
    ordering_fields = ('id',)
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

# class UserView(views.APIView):
#     queryset = User.objects.all()
#     serializer_class=UserDetailSerializer
#     lookup_field='url'

#     def get_object(self, pk):
#         """获取单个用户对象"""
#         try:
#             # pk 即主键，默认状态下就是 id
#             return User.objects.get(pk=pk)
#         except:
#             raise CustomException(message="用户不存在", code=404,status_code=status.HTTP_404_NOT_FOUND)

#     def post(self, request):
#         data = JSONParser().parse(request)
#         serializer = UserDetailSerializer( data=data)
#         # 验证提交的数据是否合法
#         # 不合法则返回400
#         if serializer.is_valid():
#             # 序列化器将持有的数据反序列化后，
#             # 保存到数据库中
#             serializer.save()
#             return CustomResponse(serializer.data)
#         return CustomException(message=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserDetailSerializer(user)
#         # 返回 Json 数据
#         return CustomResponse(data=serializer.data)

#     def put(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserDetailSerializer(user, data=request.data)
#         # 验证提交的数据是否合法
#         # 不合法则返回400
#         if serializer.is_valid():
#             # 序列化器将持有的数据反序列化后，
#             # 保存到数据库中
#             serializer.save()
#             return CustomResponse(serializer.data)
#         return CustomException(message=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         # 删除成功后返回204
#         return CustomResponse(status=status.HTTP_204_NO_CONTENT)


