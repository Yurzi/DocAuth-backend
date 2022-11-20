from rest_framework import serializers


class UserListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_blank=True, max_length=100)
    username = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=False)
    addTime = serializers.DateTimeField()
