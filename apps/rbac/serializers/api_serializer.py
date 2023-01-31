from rest_framework import serializers

from apps.rbac.models import Api, Function
from apps.rbac.serializers.function_serializer import FunctionSerializer


class ApiSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Api
        fields = "__all__"
        read_only_fields = ("path",)

    def get_status_display(self, obj):
        if obj.status == "r":
            return "正在使用"
        if obj.status == "d":
            return "开发中"
        if obj.status == "s":
            return "停止使用"

class ApiWriteSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Api
        fields = "__all__"
        #read_only_fields = ("path",)

    def get_status_display(self, obj):
        if obj.status == "r":
            return "正在使用"
        if obj.status == "d":
            return "开发中"
        if obj.status == "s":
            return "停止使用"


class ApiWithFunctionSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField(required=False)
    required_functions = FunctionSerializer(required=False, many=True,write_only=True)
    class Meta:
        model = Api
        fields = "__all__"
        read_only_fields = ("path",)

    def get_status_display(self, obj):
        if obj.status == "r":
            return "正在使用"
        if obj.status == "d":
            return "开发中"
        if obj.status == "s":
            return "停止使用"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["required_functions"] = list()
        print(instance.required_functions.all())
        for function in instance.required_functions.all():
            item = FunctionSerializer(instance=function.function).data
            item["rw_type"] = function.rw_type
            data["required_functions"].append(item)
        return data
