from rest_framework.views import exception_handler,Response,status
# 自定义错误
class CustomException(Exception):
    _default_code = 400

    def __init__(
        self,
        message: str = "",
        status_code=status.HTTP_400_BAD_REQUEST,
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
    response = exception_handler(exc, context)
    
    if response is not None:
        detail = response.data
        response.data = {"detail":detail}
        response.data['code'] = response.status_code

        if response.status_code == 404:
            response.data['message'] = "未找到"

        if response.status_code == 400:

            response.data['message'] = '输入错误'

        elif response.status_code == 401:
            response.data['message'] = '未认证'

        elif response.status_code >= 500:
            response.data['message'] = "服务器错误"

        elif response.status_code == 403:
            response.data['message'] = "权限不允许"

        elif response.status_code == 405:
            response.data['message'] = '请求不允许'
        else:
            response.data['message'] = '未知错误'
    return response

