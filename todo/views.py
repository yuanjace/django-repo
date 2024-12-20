from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Todo
from .serializers import TodoSerializer
from .throttles import secondThrottle

# 自定義分頁器
class TodoPagination(PageNumberPagination):
    page_size = 10  # 每一頁顯示 10 項
    page_size_query_param = 'page_size'  # 允許客戶端通過這個參數設置每頁的項目數
    max_page_size = 100  # 設置每頁的最大項目數


class TodoViewSet(viewsets.ModelViewSet):
    throttle_classes = [secondThrottle]

    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    pagination_class = TodoPagination  
