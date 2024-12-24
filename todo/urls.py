from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

# 創建一個 DefaultRouter 並註冊 TodoViewSet
router = DefaultRouter()
router.register(r"todos", TodoViewSet)  # 確保這裡是 'todos'

urlpatterns = [
    path("", include(router.urls)),  # 把 router 的 urls 包含進來
]
