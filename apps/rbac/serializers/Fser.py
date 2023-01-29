from ..models import Function
from rest_framework import serializers
#Founction序列化器
class FSer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = '__all__'
        read_only_fields = ('addTime',)