from rest_framework.pagination import PageNumberPagination

class CategoryPagination(PageNumberPagination):
    page_size = 8               
    page_size_query_param = 'page_size'
    max_page_size = 20


class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 24


class NewArrivalPagination(PageNumberPagination):
    page_size = 12