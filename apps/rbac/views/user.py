from ..models import User
from ..serializers.user_serializer import UserListSerializer,  UserDetailSerializer
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework.decorators import api_view
from rest_framework import decorators,permissions
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from rest_framework import status,request
from ..utils import createMD5

class UserDetailView(RetrieveUpdateDestroyAPIView):
    '''
    用户管理：删改查
    '''
    queryset = User.objects.all()
    search_fields = ('username', 'name', 'phone')
    ordering_fields = ('id',)
    serializer_class = UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        #先获取要修改的对象
        try:
            instance = self.queryset.get(pk=pk)
        except:
            #当输入不存在的pk
            raise CustomException(message='用户不存在')
        self.perform_destroy(instance)
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        #先获取要修改的对象
        try:
            instance = self.queryset.get(pk=pk)
        except:
            #当输入不存在的pk
            raise CustomException(message='用户不存在')
        # 将要修改的对象，修改的数据传入序列化器
        serializer = self.get_serializer(instance=instance,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        # 执行修改
        self.perform_update(serializer)
        return CustomResponse(data=None, status=status.HTTP_201_CREATED, msg="修改用户信息成功")


class UserRegisterView(CreateAPIView):
    '''
    用户注册
    '''
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        # 给密码加盐
        request.data['password'] = createMD5(request.data['password'])
        request.POST._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # user = serializer.data
        # refresh = RefreshToken.for_user(user)
        # res = {
        #     "refresh": str(refresh),
        #     "access": str(refresh.access_token),
        # }
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(data=None, status=status.HTTP_201_CREATED, headers=headers,msg="注册成功")


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_fields = ('name',)
    ordering_fields = ('id',)


@api_view(['GET'])
def login(request:request.Request, pk=None, format=None):
    '''
    用户登录
    '''
    req_data = request.query_params
    try:
        user = User.objects.get(username=req_data['username'])
    except User.DoesNotExist:
        return CustomException(message="用户不存在")
    if createMD5(req_data["password"]) != user.password:
        return CustomException(message="密码错误")
    else:
        return CustomResponse(data=None, status=status.HTTP_200_OK, msg="登录成功")