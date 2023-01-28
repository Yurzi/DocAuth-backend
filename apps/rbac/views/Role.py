from common.custom_response import CustomResponse
from common.custom_exception import CustomException
#---------------------
from ..models import Role_Function
from ..models import Role
from ..models import Function
from rest_framework import views
from rest_framework import serializers
import traceback
from django.core.paginator import Paginator, EmptyPage
#Role_Function序列化器
class R_FSer(serializers.ModelSerializer):
    class Meta:
        model = Role_Function
        fields = '__all__'
        read_only_fields = ('addTime',)
class ZqxRSer(serializers.Serializer):
    roleId = serializers.IntegerField(source = "id")
    rolename = serializers.CharField(max_length = 30,source = "name")
    desc = serializers.CharField(max_length = 100)
    addTime = serializers.DateTimeField()
    status = serializers.CharField()


#Role_Function删除
class Role_FunctionView(views.APIView):
    def delete(self, request):
        re_data = request.data
        
        
        R_F_list = Role_Function.objects.all()
        R_F_list = R_F_list.filter(role_id = re_data['roleId'],function_id = re_data['functionId'])
        
        if(R_F_list.exists()):
            R_F_list.delete()
            return CustomResponse(data=None,message= '删除成功')
        else:
            return CustomResponse(message="该角色权限不存在", code=402)
    #Role_Function更新
    def put(self,request):
        re_data = request.data
        rid = re_data['roleId']
        fList = re_data['functionIdList']
        print(rid)
        try:    
            rob = Role.objects.get(id= rid)
        except Role.DoesNotExist:
            return CustomResponse(message="角色id不存在",code = 402)
            
        
        R_F_list = Role_Function.objects.all()

        R_F_list = R_F_list.filter(role_id = rid)
        if R_F_list.exists():
            R_F_list.delete()


        for f in fList:
            try:
                fob = Function.objects.get(id= f)
            except Function.DoesNotExist:
                return CustomResponse(message="权限列表中有的权限id:"+str(f)+"不存在",code = 402)
        for f in fList:
            Role_Function.objects.create(role_id = rid,function_id = f)
        return CustomResponse(data= None,message="更新成功",code=200)
    def get(self,request):
        re_data = request.data
        rolename = re_data['roleName']
        ps = re_data['pageSize']
        pn = re_data['pageNum']
        if rolename is None:
            roles = Role.objects.all()
        else:
            roles = Role.objects.filter(name__contains = rolename).order_by('id')
        rsize = roles.count()
        if ps==0 or pn==0 or rsize==0:
            rt_data =   {"records":[],
                         "total":rsize
                        }
            return CustomResponse(code=200,data = rt_data,message = '查找成功')

        pageinator = Paginator(roles,ps)
        try:
            page=pageinator.page(pn)
        except EmptyPage:
            page = pageinator.page(1)
        rolesser = ZqxRSer(instance=page,many = True)
        rt_data =   {"records":rolesser.data,
                    "total":rsize
                    }
        return CustomResponse(code=200,data = rt_data,message = '查找成功')
