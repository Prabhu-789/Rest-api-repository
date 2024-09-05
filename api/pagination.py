# pagination.py
from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3  # Default number of items per page
    max_limit = 10  # Maximum number of items per page
