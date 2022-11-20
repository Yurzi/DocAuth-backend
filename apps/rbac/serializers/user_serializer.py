from rest_framework import serializers
from ..models import User
import re

REGEX_MOBILE = r"^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

class UserListSerializer(serializers.ModelSerializer):
    '''
    用户列表的序列化
    '''
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone']
        depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    '''
    用户编辑的序列化
    '''
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone']

    def validate_mobile(self, mobile):
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile


class UserCreateSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_mobile(self, mobile):
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        if User.objects.filter(mobile=mobile):
            raise serializers.ValidationError("手机号已经被注册")
        return mobile

class UserInfoListSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone']