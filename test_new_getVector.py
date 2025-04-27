from typing import List, Dict
import numpy as np

def get_vector(input):
    import requests
    import json
    
    url = "https://ailab.pkulaw.com/api/openai/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "5df2069a02034877bda56ed136d7ccd4"
    }
    data = {
        "model": "bge-m3-dense",
        "input": input
    }
    
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    if "data" in response_data and len(response_data["data"]) > 0:
        embedding_vector = response_data["data"][0]["embedding"]
        return embedding_vector
    else:
        return None

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    
    return (dot_product / (norm_vec1 * norm_vec2))*0.184
if __name__ == "__main__":
    vector1 = get_vector("合同价款与支付约定了租金计价方式（固定租金或按面积计费，待确认）、支付批次（按月/按季度/按年，待确认）、支付方式（银行转账/现金/支票，待确认）等内容。")
    vector2 = get_vector("合同价款与支付条款涵盖了租金标准、月租金金额，支付方式包括银行托收、非税缴款、现金支付或银行转账，同时规定了租赁保证金、违约金及缴费清单等相关事项。")
    similarity = cosine_similarity(vector1, vector2)
    print(similarity)

