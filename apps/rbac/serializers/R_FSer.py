from ..models import Role_Function
from rest_framework import serializers
#Role_Function序列化器
class R_FSer(serializers.ModelSerializer):
    class Meta:
        model = Role_Function
        fields = '__all__'
        read_only_fields = ('addTime',)