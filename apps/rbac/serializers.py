from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

# ModelSerializers默认帮我们实现了创建和更新方法，简化了我们的操作
class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','phone','name','addTime'],



class UserDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        },
