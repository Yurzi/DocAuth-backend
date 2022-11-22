from rest_framework import serializers
from ..models import User

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
    phone = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone']




class UserCreateSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.CharField(max_length=11)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_phone(self, phone):
        if User.objects.filter(phone=phone):
            raise serializers.ValidationError("手机号已经被注册")
        return phone

class UserInfoListSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone']