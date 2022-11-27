from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer


class CustomResponse(Response):
    """ An HttpResponse that allows its data to be rendered into arbitrary media types. """
    
    # 注意这里的初始化参数，我新增了一个paginator参数，就是分页器的实例     
    def __init__(self, data=None, code=200, message=None,status=status.HTTP_200_OK,template_name="", headers=None,exception=False, content_type=None, paginator=None):
        """ Alters the init arguments slightly. For example, drop 'template_name', and instead use 'data'. Setting 'renderer' and 'media_type' will typically be deferred, For example being set automatically by the `APIView`. """

        super().__init__(data=data, status=status,)

        if isinstance(data, Serializer):
            message = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(message)
            # 之所以加上判断是为了兼容第一种格式，在没有分页器传入的时候，可以正常返回         
        if not paginator:
            self.data = {"code": code, "message": message, "data": data}
        else:
            # 这里的分页器实例调用的方法都是drf已经为我们封装好的方法             
            self.data = {"count": paginator.count,
                         "next": paginator.get_next_link(),
                         "previous": paginator.get_previous_link(),
                         "data": data,
                         "message": message,
                         "code": code
                         }
            self.template_name = template_name
            self.exception = exception
            self.content_type = content_type
        if headers:
            for name, value in headers.items():
                self[name] = value

def decorateRes(res:Response,code=200, message=None):
    res.data = {"code": code, "message": message, "data": res.data}
    return res