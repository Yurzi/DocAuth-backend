from rest_framework import status, views

from apps.rbac.models import Api
from apps.rbac.serializers.api_serializer import ApiSerializer, ApiWithFunctionSerializer
from apps.rbac.serializers.utils import check_serializer_valid
from common.custom_exception import CustomException
from common.custom_response import CustomResponse


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
        serializer.update(instance=self.get_object(pk=request.data["id"]), validated_data=serializer.validated_data)
        return CustomResponse(code=status.HTTP_200_OK, data=ApiSerializer(self.get_object(pk=request.data["id"])).data)

    def delete(self, request):
        request_dict = request.query_params
        api_id = request_dict["id"]

        api = self.get_object(pk=api_id)
        print(api)
        api.delete()
        return CustomResponse(code=status.HTTP_200_OK, message="删除成功")

