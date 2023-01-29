from rest_framework.exceptions import APIException
from rest_framework.views import Response, exception_handler, status


# 自定义错误
class CustomException(APIException):
    _default_code = "custom_internal_server_error"

    def __init__(
        self,
        message: str = "A CustomException raised",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=None,
        code: str = _default_code,
    ):

        self.default_code = code
        self.status_code = status_code
        self.default_detail = message
        if data is None:
            self.data = {"detail": message}
        else:
            self.data = data

    def __str__(self):
        return self.default_detail


# 自定义错误处理
def custom_exception_handler(exc, context):
    # 如果是自定义错误
    if isinstance(exc, CustomException):
        response = Response(
            data={
                "code": exc.default_code,
                "message": exc.default_detail,
                "data": exc.data,
            },
            status=exc.status_code,
        )
    else:
        response = Response(
            data={
                "code": 400,
                'data':str(exc),
            },
            status=400,
        )
    return response
