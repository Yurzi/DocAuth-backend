from rest_framework import views
from ..models import User_Function,Function,User,Role_User,Role_Function
from ..serializers.Fser import FSer
from common.custom_response import CustomResponse

class W_U_FView(views.APIView):
    def get(self,request):
        re_data = request.query_params

        uid = re_data['userId']
        ufs = User_Function.objects.filter(user_id = uid).values()
        b = []
        for c in ufs:
            b.append(c['function_id'])
        fs = Function.objects.filter(id__in=b)
        fsser = FSer(instance=fs,many=True)
        fsdata = fsser.data
        for a in fsdata:
            if a['status']=="s":
                a['status'] = "停止使用"
            if a['status'] == "r":
                a['status'] = "正在使用"
            if a['status'] == "d":
                a['status']="开发中"
        re_data = {"functions":fsdata

        }
        return  CustomResponse(code = 200,data = re_data,message='查找完成')

    def post(self,request):
        re_data = request.data
        uid = re_data['userId']
        fids = re_data['functions']
        try:
            User.objects.get(id=uid)
        except User.DoesNotExist:
            return CustomResponse(message="User的id:"+str(uid)+"不存在",code = 402)
        for f in fids:
            try:
                fob = Function.objects.get(id= f)
            except Function.DoesNotExist:
                return CustomResponse(message="权限列表中有的权限id:"+str(f)+"不存在",code = 402)
        for t in fids:
            User_Function.objects.create(user_id = uid,function_id = t)
        return CustomResponse(code = 200,message='插入成功')
    
    def delete(self,request):
        re_data = request.query_params
        userId = re_data['userId']
        fId = re_data['functionId']
        uf =User_Function.objects.filter(user_id = userId,function_id=fId)
        if uf.exists():
            uf.delete()
        return CustomResponse(code=200,message='删除成功')
    #更新角色小灶权限
    def put(self,request):
        re_data = request.data
        uid = re_data['userId']
        flist = re_data['extraFunctionList']
        ufobs = User_Function.objects.filter(user_id = uid)
        if ufobs.exists():
            ufobs.delete()
        try:
            uob = User.objects.get(id=uid)
        except User.DoesNotExist:
            return CustomResponse(code=402,message='用户id不存在')
        for fid in flist:
            try:
                fob = Function.objects.get(id=fid['id'])
            except Function.DoesNotExist:
                return CustomResponse(code = 402,message='id为'+str(fid['id'])+'的function不存在')
        print(11111111111)
        for fid in flist:
            User_Function.objects.create(user_id = uid,function_id=fid['id'])
        return CustomResponse(code=200,message='更新成功')

class W_U_FViewAll(views.APIView):
    def get(self,request):
        uId = request.query_params['userId']
        try:
            users = User.objects.get(id = uId)
        except User.DoesNotExist:
            CustomResponse(code=402,data=None,message='用户id不存在')
        R_Us = Role_User.objects.filter(user_id=uId)

        fs1ob = User_Function.objects.filter(user_id=uId)
        
        b = []
        for c in fs1ob.values():
            b.append(c['function_id'])
        if R_Us.exists():
            a = []
            for u in R_Us.values():
                a.append(u['role_id'])
            R_Fs=Role_Function.objects.filter(role_id__in = a)
            for m in R_Fs.values():
                b.append(m['function_id'])
        fs = Function.objects.filter(id__in=b)
        fsser = FSer(instance=fs,many=True)
        rt_data = {
            "functions":fsser.data
        }
        return CustomResponse(code = 200,data = rt_data,message='查找成功')
