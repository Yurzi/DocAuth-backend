from rest_framework import status, views

from apps.rbac.models import Function
from apps.rbac.serializers.function_serializer import FunctionSerializer
from apps.rbac.serializers.utils import check_serializer_valid
from common.custom_exception import CustomException
from common.custom_response import CustomResponse


class FunctionListView(views.APIView):
    """
    For Function List Resource
    """

    def get(self, request):
        # 获取权限列表
        function_list = Function.objects.all()
        if not function_list.exists():
            return CustomResponse(status=status.HTTP_200_OK, data={}, message="获取成功")

        serializer = FunctionSerializer(instance=function_list, many=True)

        return CustomResponse(
            code=status.HTTP_200_OK, data=serializer.data, message="获取成功"
        )

    def post(self, request):
        serializer = FunctionSerializer(data=request.data)
        # 校验数据
        check_serializer_valid(serializer)
        # 校验通过
        serializer.save()
        # 返回
        return CustomResponse(code=status.HTTP_200_OK, data=serializer.data)


class FunctionDetailView(views.APIView):
    """
    For Function Resource
    """

    def get_object(self, pk: int):
        try:
            function = Function.objects.get(id=pk)
        except Function.DoesNotExist:
            raise CustomException(
                code=status.HTTP_404_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
                message="对象未找到",
                data={"id": pk},
            )
        return function

    def get(self, request):
        # 获取请求数据
        request_dict = request.query_params
        function_id = request_dict["id"]

        serializer = FunctionSerializer(instance=self.get_object(pk=function_id))
        return CustomResponse(code=status.HTTP_200_OK, data=serializer.data)

    def put(self, request):
        serializer = FunctionSerializer(data=request.data)
        check_serializer_valid(serializer)
        serializer.update(instance=self.get_object(pk=request.data['id']), validated_data=serializer.validated_data)
        return CustomResponse(code=status.HTTP_200_OK, data=request.data)

    def delete(self, request):
        request_dict = request.query_params
        function_id = request_dict["id"]

        function = self.get_object(pk=function_id)
        function.delete()
        return CustomResponse(code=status.HTTP_200_OK, message="删除成功", data={})