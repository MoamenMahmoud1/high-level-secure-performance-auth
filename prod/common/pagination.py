from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView


class UserPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'  # يسمح للمستخدم يحدد page_size
    max_page_size = 50