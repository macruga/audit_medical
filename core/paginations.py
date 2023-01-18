from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class CustomPaginationAfiliados(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            
            'results': data
        })

    # def paginate_queryset(self, queryset, request, init=False, view=None):
    #     print('queryset')
    #     if not init:
    #         self.page_size = self.get_custom_page_size(request, view)
    #         self.page = self.get_custom_page_size(request, view)
    #     else:
    #         self.page_size = DEFAULT_PAGE_SIZE
    #         self.page = DEFAULT_PAGE
    #     return super().paginate_queryset(queryset, request, view)

   