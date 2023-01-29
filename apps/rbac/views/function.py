from rest_framework import views

from apps.rbac.models import Function
from common.custom_exception import CustomException
from common.custom_response import CustomResponse


class FunctionListView(views.APIView):
    """
    For Function List Resource
    """

    def get(self, request):
        raise CustomException
