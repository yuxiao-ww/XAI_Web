# 使用Python官方镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 运行Django服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

