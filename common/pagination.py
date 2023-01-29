from rest_framework.pagination import PageNumberPagination
from common.custom_response import CustomResponse


class StandardResultsSetPagination(PageNumberPagination):
    '''
    列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    # 页码参数 http://127.0.0.1:8000/goods/?page=2&page_size=30
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 30

    def get_paginated_response(self, data):
        return CustomResponse(data={
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class LargeResultsSetPagination(PageNumberPagination):
    # 默认每页显示的个数
    page_size = 30
    # 可以动态改变每页显示的个数
    # 页码参数 http://127.0.0.1:8000/goods/?page=2&page_size=30
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 50
