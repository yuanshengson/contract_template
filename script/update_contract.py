import os
import json
import docx
from pathlib import Path

def extract_text_from_docx(file_path):
    """从docx文件中提取文本内容"""
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return ""

def update_json_with_fulltext():
    """更新vector_new.json文件，为每条数据添加fulltext字段"""
    template_dir = "/home/user/opt/ssy/contract_template/data/合同模板(市场监管局）"
    json_file_path = "/home/user/opt/ssy/contract_template/data/vector_data/vector_new.json"
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取JSON文件时出错: {e}")
        return
    
    for item in data:
        # 默认设置fulltext为空字符串
        item['fulltext'] = ""
        
        template_name = item.get('template', '')
        if not template_name:
            print(f"数据项缺少template字段，已设置fulltext为空字符串")
            continue
        
        docx_path = os.path.join(template_dir, f"{template_name}.docx")
        
        if not os.path.exists(docx_path):
            print(f"找不到文件: {docx_path}，已设置fulltext为空字符串")
            continue
        
        fulltext = extract_text_from_docx(docx_path)
        item['fulltext'] = fulltext
        print(f"已更新模板 '{template_name}' 的fulltext字段")
    
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已成功更新 {json_file_path}")
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

if __name__ == "__main__":
    update_json_with_fulltext()