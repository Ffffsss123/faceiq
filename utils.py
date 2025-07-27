# utils.py
import os
import torch
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import cosine
from tqdm import tqdm

# 初始化人脸检测与特征模型，keep_all=True 表示返回所有检测到的人脸
mtcnn = MTCNN(image_size=160, keep_all=True)
model = InceptionResnetV1(pretrained='vggface2').eval()

def extract_embedding(image_tensor):
    with torch.no_grad():
        emb = model(image_tensor.unsqueeze(0)).squeeze().numpy()
    return emb


def extract_embeddings_multi(image_path):
    img = Image.open(image_path)
    faces = mtcnn(img)            # keep_all=True，Detect 所有人脸
    if faces is None:
        return []
    # 如果 faces 是 list，就合并成 Tensor
    if isinstance(faces, list):
        faces = torch.stack(faces)
    embeddings = []
    for face in faces:
        embeddings.append(extract_embedding(face))
    return embeddings


def generate_reference_embedding(folder_path, output_path="embedding_IQ140.npy"):
    embeddings = []
    for fn in tqdm(os.listdir(folder_path), desc="处理中..."):
        if fn.lower().endswith(('.jpg', '.png', '.jpeg')):
            embs = extract_embeddings_multi(os.path.join(folder_path, fn))
            if embs:
                embeddings.append(embs[0])
    if not embeddings:
        raise ValueError("未检测到任何人脸特征，请检查样本文件夹。")
    mean_emb = np.mean(embeddings, axis=0)
    np.save(output_path, mean_emb)
    print(f"正在与数据库中的人类智慧学家对比")


def load_reference_embedding(path="embedding_IQ140.npy"):
    """加载保存的 reference embedding"""
    return np.load(path)


def get_user_iq_score(user_emb, reference_embedding, base_iq=140):
    """
    给定单个人脸的 embedding，计算相似度并映射 IQ 分数
    返回 (similarity, estimated_iq)
    """
    sim = 1 - cosine(user_emb, reference_embedding)
    return sim, base_iq * sim


def get_user_iq_scores_multi(image_path, reference_embedding, base_iq=140):
    """
    对一张可能含多张人脸的图，分别计算相似度和 IQ
    返回列表 [(sim, iq, label), ...]
    当相似度低于 0.7 时，label 为 '识别为正常人类'
    """
    embs = extract_embeddings_multi(image_path)
    results = []
    for emb in embs:
        sim, iq = get_user_iq_score(emb, reference_embedding, base_iq)
        label = '恭喜你！识别为正常人类' if sim < 0.7 else '不好意思! 经过大数据识别, 你是个3D，建议你立即联系潘宏培训！'
        results.append((sim, iq, label))
    return results
