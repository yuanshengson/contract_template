from fastapi import FastAPI, HTTPException
import requests
import json
import re
import numpy as np
from typing import List, Dict, Any, Optional
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="合同模板相似度查询API", description="查询与输入文本最相似的合同模板")

vector_data = None

class TextRequest(BaseModel):
    template1: Optional[str] = None
    template2: Optional[str] = None
    text1: str  
    text2: str  
    text3: str 
    text4: str  

class TemplateResponse(BaseModel):
    templates: List[str]
    scores: List[float]
    category_scores: List[Dict[str, float]]
    similarities: Dict[str, List[float]]

def load_vector_data():
    global vector_data
    vector_file_path = "/home/user/opt/ssy/contract_template/data/vector_data/vector_new.json"
    try:
        with open(vector_file_path, 'r', encoding='utf-8') as f:
            content = ""
            for line in f:
                if not line.strip().startswith(('#', '//')):
                    content += line

            if content.strip():
                vector_data = json.loads(content)
                print(f"成功加载向量数据，共 {len(vector_data)} 条记录")
            else:
                print("警告：向量数据文件为空")
                vector_data = []
    except FileNotFoundError:
        print(f"警告：向量数据文件 {vector_file_path} 不存在")
        vector_data = []
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        try:
            with open(vector_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            error_line = e.lineno
            start_line = max(0, error_line - 10)
            end_line = min(len(lines), error_line + 10)
            
            print(f"错误位置附近的内容 (行 {start_line} 到 {end_line}):")
            for i in range(start_line, end_line):
                if i == error_line - 1:
                    print(f">>> {i+1}: {lines[i].strip()}")
                else:
                    print(f"    {i+1}: {lines[i].strip()}")

            fixed_content = "[\n"
            in_object = False
            valid_objects = []
            current_object = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("{"):
                    in_object = True
                    current_object = line + "\n"
                elif line.endswith("}") or line.endswith("},"):
                    if in_object:
                        current_object += line + "\n"
                        try:
                            test_obj = json.loads(current_object.rstrip(",\n") + "}")
                            valid_objects.append(current_object)
                        except:
                            print(f"跳过无效对象: {current_object[:50]}...")
                        in_object = False
                        current_object = ""
                elif in_object:
                    current_object += line + "\n"

            fixed_json = "[\n" + "".join(valid_objects).rstrip(",\n") + "\n]"

            vector_data = json.loads(fixed_json)
            print(f"成功修复并加载向量数据，共 {len(vector_data)} 条记录")

            backup_path = vector_file_path + ".backup"
            print(f"备份原文件到 {backup_path}")
            import shutil
            shutil.copy2(vector_file_path, backup_path)
            
            with open(vector_file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_json)
            print(f"已将修复后的数据保存到 {vector_file_path}")
            
        except Exception as repair_error:
            print(f"尝试修复JSON失败: {repair_error}")
            vector_data = []
            raise HTTPException(status_code=500, detail=f"加载向量数据失败: {e}")
    except Exception as e:
        print(f"加载向量数据时发生错误: {e}")
        vector_data = []
        raise HTTPException(status_code=500, detail=f"加载向量数据失败: {e}")

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

def clean_text(text: str) -> str:
    text = text.strip()
    brackets_pairs = [('(', ')'), ('[', ']'), ('{', '}'), ('（', '）'), ('【', '】'), ('「', '」'), ('『', '』')]
    
    changed = True
    while changed:
        changed = False
        for start_bracket, end_bracket in brackets_pairs:
            if text.startswith(start_bracket) and text.endswith(end_bracket):
                text = text[len(start_bracket):-len(end_bracket)].strip()
                changed = True
    
    return text

def extract_chinese(text):
    return ''.join(re.findall(r'[\u4e00-\u9fff]+', text))

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

    load_vector_data()

    global vector_data
    
    input_vectors = {
        "text1": get_vector(request.text2),
        "text2": get_vector(request.text1),
        "text3": get_vector(request.text3),
        "text4": get_vector(request.text4)
    }
    
    scores = []
    for item in vector_data:
        template = item.get("template", "")
        template1 = item.get("template1", "")
        template2 = item.get("template2", "")

        total_score = 0
        similarities = {
            "text1": 0.0,
            "text2": 0.0,
            "text3": 0.0,
            "text4": 0.0
        }
        
        category_score = {
            "template1": 0.0,
            "template2": 0.0
        }

        request_template1 = extract_chinese(request.template1)
        request_template2 = extract_chinese(request.template2)
        
        if request_template1 and request_template1 == template1:
            total_score += 4
            category_score["template1"] = 4
        
        if request_template2 and request_template2 == template2:
            total_score += 4
            category_score["template2"] = 4
        
        vectors = item.get("vectors", {})
        
        for text_key in ["text1", "text2", "text3", "text4"]:
            if text_key in vectors and vectors[text_key]:
                sim = cosine_similarity(input_vectors[text_key], vectors[text_key])
                similarities[text_key] = sim * 100
                
                if text_key in ["text1", "text2"]:
                    total_score += sim * 27.6
                elif text_key in ["text3", "text4"]:
                    total_score += sim * 18.4
        
        scores.append((template, total_score, similarities, category_score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    
    top_templates = scores[:3]
    
    return {
        "templates": [item[0] for item in top_templates],
        "scores": [item[1] for item in top_templates],
        "category_scores": [item[3] for item in top_templates],
        "similarities": {
            "text1": [item[2]["text1"] for item in top_templates],
            "text2": [item[2]["text2"] for item in top_templates],
            "text3": [item[2]["text3"] for item in top_templates],
            "text4": [item[2]["text4"] for item in top_templates]
        }
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}

if __name__ == "__main__":
    load_vector_data()
    
    uvicorn.run(app, host="0.0.0.0", port=8031)