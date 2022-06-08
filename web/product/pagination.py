from rest_framework.pagination import PageNumberPagination


class BaseProductsPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    max_page_size = 100
    page_size_query_param = 'page_size'
