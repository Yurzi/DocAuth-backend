from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from ..models import User
from common.custom_exception import CustomException


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.get(Q(username=username) | Q(phone=username))
        print("find!",user)
        if not user:
            raise CustomException("未找到用户", status_code=status.HTTP_401_UNAUTHORIZED)
        if not password:
            raise CustomException("未输入密码",status_code=status.HTTP_402_PAYMENT_REQUIRED)
        if user.check_password(password):
            return user
        else:
            raise CustomException("密码错误", status_code=status.HTTP_401_UNAUTHORIZED)

