# 1. 基础镜像
FROM python:3.10-slim

# 2. 工作目录
WORKDIR /app

# 3. 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libglib2.0-0 libsm6 libxrender1 libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# 4. 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install -r requirements.txt

# 5. 预下载 facenet-pytorch 模型权重到 pip 缓存
RUN python - <<'EOF'
from facenet_pytorch import InceptionResnetV1, MTCNN
# 这两行会把 vggface2 模型和 MTCNN 权重下载到 ~/.cache/torch
InceptionResnetV1(pretrained='vggface2')
MTCNN().eval()
EOF

# 6. 复制项目源码
COPY . .

# 7. 暴露端口（Railway 用 $PORT）
EXPOSE 3000

# 8. 启动命令：延长超时到 120 秒
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--timeout", "120"]
