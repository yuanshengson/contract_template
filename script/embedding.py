import csv
import json
import requests
import time
import re
import argparse
from tqdm import tqdm

def get_vector(text, api_url="http://192.168.10.58:8101/text2vector/"):
    headers = {"Content-Type": "application/json"}
    data = {"text": text}
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常: {e}")
        return None

def split_contract_text(text):
    parts = {
        "text1": "",
        "text2": "",
        "text3": "",
        "text4": ""
    }

    patterns = {
        "text1": r'合同标的："([^"]*)"',
        "text2": r'合同主体："([^"]*)"',
        "text3": r'合同价款与支付："([^"]*)"',
        "text4": r'合同交易条款："([^"]*)"'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            parts[key] = match.group(1)
    
    return parts

def process_csv(csv_file, output_file, text_column=1, template_column=0, batch_size=100, sleep_time=0.1, encoding='utf-8'):
    """
        csv_file: 输入CSV文件路径
        output_file: 输出JSON文件路径
        text_column: 文本列索引（从0开始）
        template_column: 模板列索引（从0开始）
        batch_size: 批处理大小，每处理这么多条记录保存一次
        sleep_time: 每次请求后的休眠时间（秒）
    """
    results = []
    count = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        total_rows = sum(1 for _ in reader)
        f.seek(0)
        reader = csv.reader(f)

        for row in tqdm(reader, total=total_rows, desc="处理数据"):
            if len(row) <= max(text_column, template_column):
                print(f"警告: 行 {count+1} 列数不足，跳过")
                continue
                
            template = row[template_column]
            text = row[text_column]
            
            parts = split_contract_text(text)
            
            vectors = {}
            all_vectors_valid = True
            
            for part_name, part_text in parts.items():
                if part_text:
                    vector_result = get_vector(part_text)
                    if vector_result and "result" in vector_result:
                        vectors[part_name] = vector_result["result"]
                    else:
                        all_vectors_valid = False
                        print(f"警告: 无法获取部分 {part_name} 的向量")
                    time.sleep(sleep_time)
                else:
                    all_vectors_valid = False
                    print(f"警告: 部分 {part_name} 为空")
            
            if all_vectors_valid and vectors:
                result = {
                    "template": template,
                    "text1": parts["text1"],
                    "text2": parts["text2"],
                    "text3": parts["text3"],
                    "text4": parts["text4"],
                    "vector1": vectors["text1"],
                    "vector2": vectors["text2"],
                    "vector3": vectors["text3"],
                    "vector4": vectors["text4"]
                }
                results.append(result)
            
            count += 1
            
            if count % batch_size == 0:
                save_results(results, output_file, append=(count > batch_size))
                print(f"已处理 {count} 条记录，保存中间结果")
                results = []

            time.sleep(sleep_time)
    
    if results:
        save_results(results, output_file, append=(count > batch_size))
    
    print(f"处理完成，共处理 {count} 条记录，结果保存至 {output_file}")

def save_results(results, output_file, append=False):
    mode = 'a' if append else 'w'
    with open(output_file, mode, encoding='utf-8') as f:
        if not append:
            json.dump(results, f, ensure_ascii=False, indent=2)
        else:
            f.seek(0)
            try:
                existing_data = json.load(f)
                existing_data.extend(results)

                f.seek(0)
                f.truncate()
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="批量处理CSV文件并获取向量")
    parser.add_argument("--csv", required=True, help="输入CSV文件路径")
    parser.add_argument("--output", default="vectors.json", help="输出JSON文件路径")
    parser.add_argument("--text-column", type=int, default=1, help="文本列索引（从0开始）")
    parser.add_argument("--template-column", type=int, default=0, help="模板列索引（从0开始）")
    parser.add_argument("--batch-size", type=int, default=100, help="批处理大小")
    parser.add_argument("--sleep", type=float, default=0.1, help="每次请求后的休眠时间（秒）")
    
    args = parser.parse_args()
    
    process_csv(
        args.csv, 
        args.output, 
        text_column=args.text_column, 
        template_column=args.template_column,
        batch_size=args.batch_size,
        sleep_time=args.sleep
    )

if __name__ == "__main__":
    main()