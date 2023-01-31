from rest_framework import views
from ..models import Role_User,User,Role
from common.custom_response import CustomResponse
from ..serializers.RoleSer import Rser
from ..views.Role import ZqxRSer
class wsRUView(views.APIView):
    def put(self,request):
        re_data = request.data
        uid = re_data['userId']
        rids = re_data['roleIds']
        try:    
            uob =  User.objects.get(id= uid)
        except User.DoesNotExist:
            return CustomResponse(message="User的id不存在",code = 402)
        for id in rids:
            try:
                rob = Role.objects.get(id=id)
            except Role.DoesNotExist:
                return CustomResponse(message="角色id为"+str(id)+"的角色不存在",code=402)

        r_u_obs = Role_User.objects.filter(user_id=uid)
        if r_u_obs.exists():
            r_u_obs.delete()

        for rid in rids:
            Role_User.objects.create(role_id = rid,user_id = uid)
        return CustomResponse(message= '更新完毕',code=200,data=None )
    #获取某个用户的角色列表
    def get(self,request):
        re_data = request.query_params
        uid = re_data['userid']
        print(uid)
        R_U_obs = Role_User.objects.filter(user_id = uid)
        rt_data = {
            "roles":[]
        }
        #print(1111111)
        if not R_U_obs.exists():
            return CustomResponse(code=200,data=rt_data,message='查询成功')
        #print(222222222222222)
        b = []
        for ru in R_U_obs.values():
            b.append(ru['role_id'])
        
        role_obs =  Role.objects.filter(id__in = b)

        rolesser = ZqxRSer(instance=role_obs,many=True)
        roles = rolesser.data
        for c in roles:
            if c['status'] == 'r':
                c['status'] = True
            else:
                c['status'] = False
        re_data = {
            "roles":roles
        }
        
        return CustomResponse(code = 200,data = re_data,message='查询成功')

