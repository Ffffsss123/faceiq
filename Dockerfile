# 1. 基于轻量 Python 镜像
FROM python:3.10-slim

# 2. 指定工作目录
WORKDIR /app

# 3. 先复制 requirements.txt，以便利用 Docker 缓存加速
COPY requirements.txt .

# 4. 安装 CPU-only PyTorch + 其它依赖
RUN pip install --upgrade pip setuptools wheel \
 && pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install -r requirements.txt

# 5. 复制项目代码
COPY . .

# 6. 暴露端口（Railway 会自动设置 $PORT 环境变量）
EXPOSE 3000

# 7. 启动命令，绑定到 $PORT
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT"]
