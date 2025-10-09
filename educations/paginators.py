from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 5  # Количество элементов на странице
    page_size_query_param = "page_size"  # Кастомный параметр указания количества элементов на странице page_size = 30
    max_page_size = 15  # Максимальное количество элементов на странице
