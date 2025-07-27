# Dockerfile
FROM python:3.10-slim

# 1. 切换到工作目录
WORKDIR /app

# 2. 安装系统依赖（Facenet-PyTorch 需要一些底层库）
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      libglib2.0-0 libsm6 libxrender1 libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# 3. 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install -r requirements.txt

# 4. 复制项目所有源代码
COPY . .

# 5. 暴露端口（Railway 会提供 $PORT 环境变量）
EXPOSE 3000

# 6. 启动命令
CMD ["sh","-c","gunicorn app:app --bind 0.0.0.0:$PORT"]
