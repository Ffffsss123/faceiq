import numpy as np
from scipy.spatial.distance import cosine

# 全局加载 IQ140 参考向量
ref_emb = np.load("embedding_IQ140.npy")

def predict_from_descriptor(descriptor, base_iq=140):
    sim = 1 - cosine(descriptor, ref_emb)
    iq  = base_iq * sim
    if sim < 0:
        label = '毫无相似'
    elif sim < 0.7:
        label = '恭喜你！识别为正常人类'
    else:
        label = '不好意思!经过大数据识别,你是一个3D,建议联系潘宏进行训练'
    return sim, iq, label
