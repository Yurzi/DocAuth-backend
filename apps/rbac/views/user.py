from ..models import User
from ..serializers.user_serializer import UserListSerializer, UserDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, serializers
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from rest_framework import status, request
from ..utils import getTokensForUser


class UserDetailView(RetrieveUpdateDestroyAPIView):
    '''
    用户管理：删改查
    '''
    queryset = User.objects.all()
    search_fields = ('username', 'name', 'phone')
    ordering_fields = ('id',)
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request: request.Request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 先获取要修改的对象
        try:
            instance = self.queryset.get(pk=pk)
        except:
            # 当输入不存在的pk
            raise CustomException(message='用户不存在')
        self.perform_destroy(instance)
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: request.Request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 先获取要修改的对象
        try:
            instance = self.queryset.get(pk=pk)
        except:
            # 当输入不存在的pk
            raise CustomException(message='用户不存在')
        # 将要修改的对象，修改的数据传入序列化器
        serializer: serializers.Serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # 执行修改
        self.perform_update(serializer)
        return CustomResponse(data=None, status=status.HTTP_201_CREATED, message="修改用户信息成功")


class UserRegisterView(CreateAPIView):
    '''
    用户注册
    '''
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request: request.Request, *args, **kwargs):
        req_data = request.data.copy()  # type: ignore
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # refresh = RefreshToken.for_user(user)
        # res = {
        #     "refresh": str(refresh),
        #     "access": str(refresh.access_token),
        # }
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(data=None, status=status.HTTP_201_CREATED, headers=headers, message="注册成功")


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_fields = ('name',)
    ordering_fields = ('id',)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request: request.Request, pk=None, format=None):
    '''
    用户登录
    '''
    req_data = request.data
    try:
        user = User.objects.get(username=req_data['username'])  # type: ignore
    except User.DoesNotExist:
        return CustomResponse(message="用户不存在", code=402)
    if not user.check_password(req_data['password']):  # type: ignore
        return CustomResponse(message="密码错误", code=402)
    else:

        res_data = {**getTokensForUser(user), 'id': user.pk}
        return CustomResponse(data=res_data, message="登录成功")
