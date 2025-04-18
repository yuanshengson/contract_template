from fastapi import FastAPI, HTTPException
import requests
import json
import numpy as np
from typing import List, Dict, Any
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="合同模板相似度查询API", description="查询与输入文本最相似的合同模板")

vector_data = None

class TextRequest(BaseModel):
    text: str

class TemplateResponse(BaseModel):
    templates: List[str]
    similarities: List[float]

def load_vector_data(file_path: str = "/home/user/opt/ssy/contract_template/vector.json") -> List[Dict[str, Any]]:
    global vector_data
    
    if vector_data is None:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                vector_data = json.load(f)
            print(f"成功加载向量数据，共 {len(vector_data)} 条记录")
        except Exception as e:
            print(f"加载向量数据失败: {e}")
            raise HTTPException(status_code=500, detail=f"加载向量数据失败: {e}")
    
    return vector_data

def get_vector(text: str, api_url: str = "http://192.168.10.58:8101/text2vector/") -> List[float]:
    headers = {"Content-Type": "application/json"}
    data = {"text": text}
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, dict) and "result" in response_data:
                return response_data["result"]
            return response_data
        else:
            raise HTTPException(status_code=response.status_code, detail=f"向量服务请求失败: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"向量服务请求异常: {str(e)}")

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    
    return dot_product / (norm_vec1 * norm_vec2)

@app.post("/find_similar_templates/", response_model=TemplateResponse)
async def find_similar_templates(request: TextRequest):
    """
    查找与输入文本最相似的合同模板
    
    Args:
        request: 包含输入文本的请求
        
    Returns:
        最相似的三个模板及其相似度
    """
    data = load_vector_data()
    
    input_vector = get_vector(request.text)
    
    similarities = []
    for item in data:
        template = item.get("template", "")
        vector = item.get("vector", [])
        
        if not vector:
            continue
        
        similarity = cosine_similarity(input_vector, vector)
        similarities.append((template, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # 获取前三个最相似的模板
    top_templates = similarities[:3]
    
    return {
        "templates": [item[0] for item in top_templates],
        "similarities": [item[1] for item in top_templates]
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}

if __name__ == "__main__":
    load_vector_data()
    
    uvicorn.run(app, host="0.0.0.0", port=8031)