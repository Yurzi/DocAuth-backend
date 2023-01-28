from common.custom_response import CustomResponse
from common.custom_exception import CustomException
#---------------------
from ..models import Role_Function
from rest_framework import views
#Role_Function删除
class Role_FunctionView(views.APIView):
    def delete(self, request):
        re_data = request.data
        
        
        R_F_list = Role_Function.objects.all()
        R_F_list.filter(role_id = re_data['roleId'],function_id = re_data['functionId'])
        
        if(R_F_list.exists()):
            R_F_list.delete()
            return CustomResponse(data=None,message= '删除成功')
        else:
            return CustomResponse(message="该角色权限不存在", code=402)

        
        