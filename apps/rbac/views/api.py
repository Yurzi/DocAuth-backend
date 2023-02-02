from rest_framework import status, views

from apps.rbac.models import Api, Api_Function, Function
from apps.rbac.serializers.api_serializer import (ApiSerializer,
                                                  ApiWithFunctionSerializer)
from apps.rbac.serializers.utils import check_serializer_valid
from common.custom_exception import CustomException
from common.custom_response import CustomResponse
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage

class ApiListView(views.APIView):
    """
    For Api List
    """

    def get(self, request):
        # 获取权限列表
        api_list = Api.objects.all()
        if not api_list.exists():
            return CustomResponse(status=status.HTTP_200_OK, data={}, message="获取成功")

        serializer = ApiSerializer(instance=api_list, many=True)

        return CustomResponse(
            code=status.HTTP_200_OK, data=serializer.data, message="获取成功"
        )

    def post(self, request):
        serializer = ApiSerializer(data=request.data)
        # 校验数据
        check_serializer_valid(serializer)
        # 校验通过
        serializer.save()
        # 返回
        return CustomResponse(code=status.HTTP_200_OK, data=serializer.data)


class ApiDetailView(views.APIView):
    """
    For Api Resource Detail
    """

    def get_object(self, pk: int):
        try:
            api = Api.objects.get(id=pk)
        except Api.DoesNotExist:
            raise CustomException(
                code=status.HTTP_404_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
                message="对象未找到",
                data={"id": pk},
            )
        return api

    def get(self, request):
        # 获取请求参数
        api_dict = request.query_params
        api_id = api_dict["id"]

        serializer = ApiWithFunctionSerializer(instance=self.get_object(pk=api_id))
        return CustomResponse(code=status.HTTP_200_OK, data=serializer.data)

    def put(self, request):
        serializer = ApiSerializer(data=request.data)
        check_serializer_valid(serializer)
        serializer.update(
            instance=self.get_object(pk=request.data["id"]),
            validated_data=serializer.validated_data,
        )
        return CustomResponse(
            code=status.HTTP_200_OK,
            data=ApiSerializer(self.get_object(pk=request.data["id"])).data,
        )

    def delete(self, request):
        request_dict = request.query_params
        api_id = request_dict["id"]

        api = self.get_object(pk=api_id)
        print(api)
        api.delete()
        return CustomResponse(code=status.HTTP_200_OK, message="删除成功")


class ApiFunctionView(views.APIView):
    """
    For Api Function Operation
    """

    def get_api_object(self, pk: int):
        try:
            api = Api.objects.get(id=pk)
        except Api.DoesNotExist:
            raise CustomException(
                code=status.HTTP_404_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
                message="对象未找到",
                data={"id": pk},
            )
        return api

    def check_and_get_function(self, pk: int):
        try:
            function = Function.objects.get(id=pk)
        except Function.DoesNotExist:
            return None
        return function

    def check_rw_type(self, rw_type:str):
        if rw_type not in ['r','w','a']:
            raise CustomException(
                code=status.HTTP_502_BAD_GATEWAY,
                status_code=status.HTTP_502_BAD_GATEWAY,
                message="不支持的rw_type",
                data={"rw_type": rw_type})
        return rw_type


    def post(self, request):
        api_id = request.data["id"]
        functions = request.data["functions"]

        api = self.get_api_object(pk=api_id)

        failure_flag = False

        for item in functions:
            function = self.check_and_get_function(item["functionid"])
            self.check_rw_type(item["rw_type"])
            if function is None:
                failure_flag = True

            qwq = Api_Function.objects.get_or_create(
                api=api, function=function, rw_type=item["rw_type"]
            )

        if failure_flag:
            return CustomResponse(
                code=status.HTTP_202_ACCEPTED,
                message="接受更新但部分权限不存在",
                data=ApiWithFunctionSerializer(instance=self.get_api_object(pk=api_id)).data,
            )
        return CustomResponse(
            code=status.HTTP_200_OK,
            message="添加成功",
            data=ApiWithFunctionSerializer(instance=self.get_api_object(pk=api_id)).data,
        )

    def delete(self, request):
        request_dict = request.query_params
        print(request_dict)

        api = self.get_api_object(pk=request_dict["id"])
        function = self.check_and_get_function(pk=request_dict["functionid"])
        rw_type = self.check_rw_type(request_dict["rw_type"])

        record = Api_Function.objects.filter(api=api, function=function, rw_type=rw_type).all()
        if not record.exists():
            raise CustomException(
                code=status.HTTP_404_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
                message="记录未找到",
            )
        record.delete()
        return CustomResponse(code=status.HTTP_200_OK, message="删除成功", data=ApiWithFunctionSerializer(instance=api).data)



class zqxApiView(views.APIView):
    #模糊分页获取API
    def get(self,request):
        re_data = request.query_params
        print(re_data)
        pn = re_data['pageNum']
        ps = re_data['pageSize']
        print(pn)
        pat = re_data['path']
        print(type(pat))
        pat = pat.strip('\'')
        pat = pat.strip('\"')
        pat = pat.lstrip()
        print(pat)
        name = re_data['name']
        name = name.strip('\'')
        name = name.strip('\"')
        name = name.lstrip()
        print(name)
        apis = Api.objects.filter(Q(path__contains=pat)|Q(name__contains=name))
        asize = apis.count()
        if pn==0 or ps==0 or asize==0:
            rt_data = {
            "records":[],
            "total":asize
        }
            return CustomResponse(code=0,data=rt_data,message='查找成功')
        pageinator = Paginator(apis,ps)
        try:
            page=pageinator.page(pn)
        except EmptyPage:
            page = pageinator.page(1)
        apsser = ApiSerializer(instance=page,many = True)
        api_datas = apsser.data
        # for d in role_datas:
        #     if d['status'] == 'r':
        #         d['status'] = True
        #     else:
        #         d['status'] = False
        for d in api_datas:
            d['status'] = d['status_display']
        rt_data =   {"records":api_datas,
                    "total":asize
                    }
        return CustomResponse(code=200,data = rt_data,message = '查找成功')

    #批量删除Api
    def delete(self,request):
        re_data = request.query_params
        ids = re_data.getlist('ids[]')
        Api.objects.filter(id__in =ids)
        return CustomResponse(code=200,message='删除成功')
    