from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from ..models import User
from common.custom_exception import CustomException


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.get(Q(username=username) | Q(phone=username))
        if not user:
            raise CustomException("未找到用户", code=401)
        if not password:
            raise CustomException("未输入密码", code=401)
        if user.check_password(password):
            return user
        else:
            raise CustomException("密码错误", code=401)

