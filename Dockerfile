FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential libglib2.0-0 libsm6 libxrender1 libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install -r requirements.txt

# 预下载模型权重到缓存
RUN python - <<'EOF'
from facenet_pytorch import InceptionResnetV1, MTCNN
InceptionResnetV1(pretrained='vggface2')
MTCNN().eval()
EOF

COPY . .
EXPOSE 3000

CMD ["gunicorn", "app:app", \
     "--bind", "0.0.0.0:$PORT", \
     "--preload", \
     "--timeout", "120", \
     "--workers", "1"]
