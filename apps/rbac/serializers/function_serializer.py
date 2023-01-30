from rest_framework import serializers

from apps.rbac.models import Function


class FunctionSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Function
        fields = "__all__"

    def get_status_display(self, obj):
        if obj.status == "r":
            return "正在使用"
        if obj.status == "d":
            return "开发中"
        if obj.status == "s":
            return "停止使用"
