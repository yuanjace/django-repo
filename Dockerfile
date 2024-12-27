# 使用轻量级 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装必要的系统工具
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装项目依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露 Gunicorn 的端口
EXPOSE 8000

# 使用 Gunicorn 启动 Django 应用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoRepo.wsgi:application"]
