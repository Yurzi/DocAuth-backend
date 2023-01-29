from ..models import User,Role,Role_User
from ..serializers.user_serializer import UserListSerializer, UserDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, serializers
from common.custom_response import CustomResponse
from common.custom_exception import CustomException
from rest_framework import status, request
from ..utils import getTokensForUser
from django.core.paginator import Paginator,EmptyPage
from rest_framework import views
from django.db.models import Q

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


def getSearchObject(query, queries: list[str]):
    res = {}
    for key in queries:
        if key in query:
            res[key] = query[key]
    return res


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_fields = ('name',)
    ordering_fields = ('id',)

    def get_queryset(self):
        searchObj = getSearchObject(self.request.query_params, ['username', 'name', 'phone'])
        queryset = self.queryset.filter(**searchObj)
        return queryset


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




class WsUserView(views.APIView):
    def delete(self,request):
        ids = request.query_params['ids']
        ids = ids.replace('[','')
        ids = ids.replace(']','')
        ids = list(map(int,ids.split(',')))

        roles = Role.objects.filter(role_id__in = ids)
        if(roles.exists()):
            roles.delete()

        users = User.objects.filter(id__in = ids)
        if users.exists():
            users.delete()
            #print(1223)
        return CustomResponse(code=200,message='删除成功',data=None)
    def get(self,request):
        re_data = request.query_params
        pn = re_data['pageNum']
        ps = re_data['pageSize']
        us = User.objects.all()
        us.order_by('id')
        usize = us.count()
        if ps==0 or pn==0 or usize==0:
            rt_data =   {"records":[],
                         "total":usize
                        }
            return CustomResponse(code=200,data = rt_data,message = '查找成功')

        pageinator = Paginator(us,ps)
        try:
            page=pageinator.page(pn)
        except EmptyPage:
            page = pageinator.page(1)
        usser = UserListSerializer(instance=page,many = True)
        rt_data =   {"records":usser.data,
                    "total":usize
                    }
        return CustomResponse(code=200,data = rt_data,message = '查找成功')
    def put(self,request):
        re_data=request.data
        id = re_data['id']
        gd = re_data['gender']
        eml = re_data['email']
        phe = re_data['phone']
        uname = re_data['username']
        name = re_data['name']
        us = User.objects.filter(id = id)
        if not us.exists():
            return CustomResponse(code=402,message='该用户不存在')
        us.update(gender=gd,email=eml,phone=phe,username=uname,name=name)
        return CustomResponse(code=200,message='更新成功')

class WsUser_2_view(views.APIView):
    def get(self,request):
        re_data = request.query_params
        uname = str(re_data['userName'])
        uname = uname.strip('\'')
        uname = uname.strip('\"')
        phone = str(re_data['phone'])
        phone = phone.strip('\'')
        phone = phone.strip('\"')
        role = str(re_data['role'])
        role = role.strip('\'')
        role = role.strip('\"')

        pn = re_data['pageNum']
        ps = re_data['pageSize']
        us1 = User.objects.filter(Q(username__contains=uname)&Q(phone__contains=phone))
        
        if role == '':
            us = us1
        else:
            roles = Role.objects.filter(name__contains=role).values()        
            b = []
            for r in roles:
                b.append(r['id'])

            r_us = Role_User.objects.filter(role_id__in = b).values()
            c = []
            for r_u in r_us:
                c.append(r_u['user_id'])
            us2 = User.objects.filter(id__in = c)

            us = us1&us2
        
        usize = us.count()
        if ps==0 or pn==0 or usize==0:
            rt_data =   {"records":[],
                         "total":usize
                        }
            return CustomResponse(code=200,data = rt_data,message = '查找成功')

        pageinator = Paginator(us,ps)
        try:
            page=pageinator.page(pn)
        except EmptyPage:
            page = pageinator.page(1)
        usser = UserListSerializer(instance=page,many = True)
        rt_data =   {"records":usser.data,
                    "total":usize
                    }
        return CustomResponse(code=200,data = rt_data,message = '查找成功')

    