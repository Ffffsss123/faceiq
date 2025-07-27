# 1. 基于官方 PyTorch CPU-only 镜像
FROM pytorch/pytorch:2.7.1-cpu

# 2. 设置工作目录
WORKDIR /app

# 3. 复制项目所有文件到容器
COPY . .

# 4. 安装除 torch 之外的 Python 依赖
#    （torch 和 torchvision 已在基础镜像中）
RUN pip install --upgrade pip \
 && pip install flask gunicorn facenet-pytorch torchvision scipy pillow tqdm

# 5. 暴露端口（Railway 会自动设置 $PORT 环境变量）
EXPOSE 3000

# 6. 启动命令
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT"]
