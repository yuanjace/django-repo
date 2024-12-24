from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer
from .throttles import secondThrottle

# import ollama


# 自定義分頁器
class TodoPagination(PageNumberPagination):
    page_size = 10  # 每一頁顯示 10 項
    page_size_query_param = "page_size"  # 允許客戶端通過這個參數設置每頁的項目數
    max_page_size = 100  # 設置每頁的最大項目數


class TodoViewSet(viewsets.ModelViewSet):
    throttle_classes = [secondThrottle]

    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer
    pagination_class = TodoPagination

    # def create(self, request, *args, **kwargs):
    #     """
    #     Override create method to add custom text to request data.
    #     """
    #     # 複製原始的 request.data
    #     data = request.data.copy()

    #     response = ollama.chat(
    #         model="llama3.1",
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": "你是中英雙語翻譯機，負責翻譯使用者傳來的內容。如果使用者傳中文，就翻譯成英文，如果使用者傳英文，就翻譯成中文。其他什麼事情都不要做",
    #             },
    #             {
    #                 "role": "user",
    #                 "content": f"幫我翻譯'{data["description"]}'",
    #             },
    #         ],
    #     )
    #     print(response["message"]["content"])

    #     # 假設您要在 `title` 字段中添加一些文字
    #     if "description" in data:
    #         data["description"] = (
    #             data["description"] + f"({response["message"]["content"]})"
    #         )

    #     # 使用序列化器來進行驗證
    #     serializer = self.get_serializer(data=data)

    #     if serializer.is_valid():
    #         # 如果驗證成功，保存並返回創建的物件
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         # 如果驗證失敗，返回錯誤訊息
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     """
    #     保存新創建的物件。
    #     """
    #     serializer.save()
