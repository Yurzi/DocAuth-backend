from ..models import Role
from rest_framework import serializers

class Rser(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('addTime',)