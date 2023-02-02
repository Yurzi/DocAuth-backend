from rest_framework import serializers, status

from common.custom_exception import CustomException


def check_serializer_valid(serializer: serializers.BaseSerializer):
    if not serializer.is_valid():
        raise CustomException(
            message="格式错误",
            status_code=status.HTTP_502_BAD_GATEWAY,
            code=status.HTTP_502_BAD_GATEWAY,
            data=serializer.errors,
        )
