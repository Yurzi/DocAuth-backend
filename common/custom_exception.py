from rest_framework.views import Response, exception_handler, status


# 自定义错误
class CustomException(Exception):
    _default_code = 400

    def __init__(
        self,
        message: str = "",
        status_code=status.HTTP_200_OK,
        data=None,
        code: int = _default_code,
    ):

        self.code = code
        self.status = status_code
        self.message = message
        if data is None:
            self.data = {"detail": message}
        else:
            self.data = data

    def __str__(self):
        return self.message


# 自定义错误处理
def custom_exception_handler(exc, context):
    # 如果是自定义错误
    if isinstance(exc, CustomException):
        response = Response(
            data={
                "code": exc.code,
                "message": exc.message,
                "data": exc.data,
            },
            status=exc.status,
        )
    else:
        response = exception_handler(exc, context)
        if response:
            response = Response(status=response.status_code, data=response.data)
    return response
