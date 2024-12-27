import os

from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer
from .throttles import secondThrottle

from ollama import Client


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

    def create(self, request, *args, **kwargs):
        # 在这里修改 request.data
        modified_data = request.data.copy()  # 复制原始请求数据
        try:
            ollama_host = os.getenv("OLLAMA_HOST")
            ollama_port = os.getenv("OLLAMA_PORT")
            client = Client(host=f"http://{ollama_host}:{ollama_port}")

            # 尝试连接到聊天模型
            response = client.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "system",
                        "content": f"你是一個待辦事項助手，主題是({modified_data['title']})，協助使用者進行1.整理2.規劃3.建議。",
                    },
                    {
                        "role": "user",
                        "content": f"以下是使用者的待辦事項'{modified_data['description']}'",
                    },
                ],
            )

            # 如果连接成功，修改描述字段
            modified_data["description"] = (
                f"{modified_data['description']}\n以下括號內是建議 : \n\n({response['message']['content']})"
            )

        except Exception as e:
            print(f"Error while connecting to the client: {e}")

        # 将修改后的数据传递给序列化器
        serializer = self.get_serializer(data=modified_data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # 在这里执行保存操作（可以使用默认的保存方法）
        serializer.save()
