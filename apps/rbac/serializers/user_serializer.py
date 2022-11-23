from rest_framework import serializers
from ..models import User
from common.custom_exception import CustomException

class UserListSerializer(serializers.ModelSerializer):
    '''
    用户列表的序列化
    '''
    # roles = serializers.SerializerMethodField()

    # def get_roles(self, obj):
    #     return obj.roles.values()

    class Meta:
        model = User
        exclude = ['password']
        depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    '''
    创建、修改用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise CustomException(username + ' 账号已存在')
        return username

    def validate_phone(self, phone):
        if User.objects.filter(phone=phone):
            raise CustomException("手机号已经被注册")
        return phone
