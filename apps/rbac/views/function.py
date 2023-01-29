from rest_framework import status, views

from apps.rbac.models import Function
from apps.rbac.serializers.function_serializer import FunctionSerializer
from common.custom_exception import CustomException
from common.custom_response import CustomResponse


class FunctionListView(views.APIView):
    """
    For Function List Resource
    """

    def get(self, request):
        # 获取权限列表
        function_list = Function.objects.all()

        serializer = FunctionSerializer(isinstance=function_list)

        return CustomResponse(
            code=status.HTTP_200_OK, data=serializer.data, message="获取成功"
        )

    def post(self, request):
        serializer = FunctionSerializer(data=request.data)
        # 校验数据
        if not serializer.is_valid():
            raise CustomException(
                message="格式错误",
                status_code=status.HTTP_502_BAD_GATEWAY,
                code=status.HTTP_502_BAD_GATEWAY,
                data=serializer.errors,
            )
        # 校验通过
        serializer.save()
        # 返回
        return CustomResponse(code=status.HTTP_200_OK, data=serializer.data)
