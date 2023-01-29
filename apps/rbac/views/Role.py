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
#Founction序列化器
class FSer(serializers.ModelSerializer):
    class Meta:
        model = Function
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
    #分页获取角色列表
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
        role_datas = rolesser.data
        for d in role_datas:
            if d['status'] == 'r':
                d['status'] = True
            else:
                d['status'] = False
        rt_data =   {"records":rolesser.data,
                    "total":rsize
                    }
        return CustomResponse(code=200,data = rt_data,message = '查找成功')
    def post(self,request):
        re_data = request.data
        #print(re_data)
        n_r = re_data['newRoleAllInfo']['newRole']
        fu_list = re_data['newRoleAllInfo']['newRoleFunctions']
        
        if n_r['status']:
            n_r['status'] = 'r'
        else:
            n_r['status'] = 's'
        rId = Role.objects.create(name = n_r['rolename'],desc=n_r['desc'],status=n_r['status'])
        for f in fu_list:
            try:
                fob = Function.objects.get(id= f)
            except Function.DoesNotExist:
                return CustomResponse(message="权限列表中有的权限id:"+str(f)+"不存在",code = 402)

        for f in fu_list:
            Role_Function.objects.create(function_id=f,role_id=rId.id)

        return CustomResponse(code=200,message='成功',data=None)

class zqxR_F1View(views.APIView):
    #根据id获取角色的权限列表
    def get(self,request):
        re_data = request.data
        roleid = re_data['roleid']
        fid_list = Role_Function.objects.filter(role_id = roleid).values()
        b = []
        for f in fid_list:
            b.append(f['function_id'])
        f_list = Function.objects.filter(id__in = b)
        FS = FSer(instance=f_list,many = True)
        rt_data = FS.data
        #print(flist.function_id)
        return CustomResponse(code=200,message='成功',data=rt_data)
    #批量删除角色
    def delete(self,request):
        re_data = request.data
        rids = re_data['ids']
        #print(1111111111111)
        #print(rids)
        flist = Role_Function.objects.filter(role_id__in= rids)
        if flist.exists():
            flist.delete()
        rs = Role.objects.filter(id__in = rids)
        if rs.exists():
            rs.delete()
        return CustomResponse(code=200,message='成功',data=None)
    #更新角色信息
    def put(self,request):
        re_data = request.data['role']
        roleid = re_data['roleid']
        rname = re_data['rolename']
        n_desc = re_data['desc']
        r =Role.objects.filter(id=roleid)
        if r.exists():
            r.update(name=rname,desc = n_desc)
        else:
            return CustomResponse(message="该角色不存在",code = 402)
        return CustomResponse(data=None,code=200,message='修改成功')
class zqx_RView(views.APIView):
    #根据id删除一个角色
    def delete(self,request):
        re_data = request.data
        roleid = re_data['roleid']
        flist = Role_Function.objects.filter(role_id= roleid)
        if flist.exists():
            flist.delete()
        rs = Role.objects.filter(id = roleid)
        if rs.exists():
            rs.delete()
        return CustomResponse(code=200,message='成功',data=None)
    #更新角色状态
    def put(self,request):
        re_data = request.data
        rid = re_data['roleid']
        status = re_data['status']
        if status:
            status='r'
        else:
            status = 's'
        #try:
        #    rob = Role.objects.get(id= rid)
        #except Function.DoesNotExist:
        #    return CustomResponse(message="该角色不存在",code = 402)
        rob = Role.objects.filter(id = rid)
        if not rob.exists():
           return CustomResponse(message="该角色不存在",code = 402)
        rob.update(status=status)
        return CustomResponse(message='更新状态成功',code=200,data=None) 
        

