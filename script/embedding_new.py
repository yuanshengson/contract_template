import csv
import os
import json
import requests
import time
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

def process_csv(csv_file, output_file, template_column=0, template1_column=1, template2_column=2, 
                text1_column=3, text2_column=4, text3_column=5, text4_column=6, 
                batch_size=100, sleep_time=0.1, encoding='utf-8', first_save_append=False):
    """
        csv_file: 输入CSV文件路径
        output_file: 输出JSON文件路径
        template_column: 模板名称列索引（从0开始）
        template1_column: 一级分类列索引
        template2_column: 二级分类列索引
        text1_column: 文本1列索引
        text2_column: 文本2列索引
        text3_column: 文本3列索引
        text4_column: 文本4列索引
        batch_size: 批处理大小，每处理这么多条记录保存一次
        sleep_time: 每次请求后的休眠时间（秒）
    """
    results = []
    count = 0
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader, None)
        f.seek(0)
        total_rows = sum(1 for _ in reader) - 1
        f.seek(0)
        reader = csv.reader(f)
        next(reader, None)

        for row in tqdm(reader, total=total_rows, desc="处理数据"):
            max_col = max(template_column, template1_column, template2_column, 
                          text1_column, text2_column, text3_column, text4_column)
            if len(row) <= max_col:
                print(f"警告: 行 {count+1} 列数不足，跳过")
                continue
                
            template = row[template_column]
            template1 = row[template1_column]
            template2 = row[template2_column]
            text1 = row[text1_column]
            text2 = row[text2_column]
            text3 = row[text3_column]
            text4 = row[text4_column]
            
            vectors = {}
            all_vectors_valid = True
            
            text_parts = {
                "text1": text1,
                "text2": text2,
                "text3": text3,
                "text4": text4
            }
            
            parts = {}
            
            for part_name, part_text in text_parts.items():
                parts[part_name] = part_text
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
                    "template1": template1,
                    "template2": template2,
                    "parts": parts,
                    "vectors": vectors
                }
                results.append(result)
            
            count += 1
            
            if count % batch_size == 0:
            # 第一次保存时，如果指定了first_save_append，则使用追加模式
                save_results(results, output_file, append=(count > batch_size or first_save_append))
                print(f"已处理 {count} 条记录，保存中间结果")
                results = []

            time.sleep(sleep_time)
    
    if results:
        save_results(results, output_file, append=(count > batch_size or first_save_append))
    
    print(f"处理完成，共处理 {count} 条记录，结果保存至 {output_file}")

def save_results(results, output_file, append=False):
    if not append:
        print(f"使用覆盖模式保存 {len(results)} 条记录")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    else:
        try:
            existing_data = []
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                print(f"成功读取现有数据，共 {len(existing_data)} 条记录")
            except FileNotFoundError:
                print(f"文件 {output_file} 不存在，将创建新文件")
            
            original_count = len(existing_data)
            existing_data.extend(results)
            print(f"追加 {len(results)} 条记录后，共 {len(existing_data)} 条记录")
            
            # 备份原文件
            if original_count > 0:
                import shutil
                backup_file = "/home/user/opt/ssy/contract_template/data/backup/vector_new.json" + ".backup." + time.strftime("%Y%m%d%H%M%S")
                shutil.copy2(output_file, backup_file)
                print(f"已将原文件备份到 {backup_file}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}，将备份原文件并只保存新数据")
            # 备份原文件
            import shutil
            backup_file = output_file + ".backup." + time.strftime("%Y%m%d%H%M%S")
            try:
                shutil.copy2(output_file, backup_file)
                print(f"已将原文件备份到 {backup_file}")
            except Exception as be:
                print(f"备份文件失败: {be}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"警告：由于JSON解析错误，原有数据可能丢失，只保存了新的 {len(results)} 条记录")

def main():
    parser = argparse.ArgumentParser(description="批量处理CSV文件并获取向量")
    parser.add_argument("--csv", required=True, help="/home/user/opt/ssy/contract_template/data/contrac_csv/contract_new.csv.csv")
    parser.add_argument("--output", default="/home/user/opt/ssy/contract_template/data/vector_data/vector_new.json", help="输出JSON文件路径")
    parser.add_argument("--template-column", type=int, default=1, help="模板名称列索引（从0开始）")
    parser.add_argument("--template1-column", type=int, default=10, help="一级分类列索引（从0开始）")
    parser.add_argument("--template2-column", type=int, default=11, help="二级分类列索引（从0开始）")
    parser.add_argument("--text1-column", type=int, default=6, help="文本1列索引（从0开始）")
    parser.add_argument("--text2-column", type=int, default=7, help="文本2列索引（从0开始）")
    parser.add_argument("--text3-column", type=int, default=8, help="文本3列索引（从0开始）")
    parser.add_argument("--text4-column", type=int, default=9, help="文本4列索引（从0开始）")
    parser.add_argument("--batch-size", type=int, default=100, help="批处理大小")
    parser.add_argument("--sleep", type=float, default=0.1, help="每次请求后的休眠时间（秒）")
    parser.add_argument("--append", action="store_true", help="是否追加到现有文件，而不是覆盖")
    args = parser.parse_args()

    first_save_append = False
    if args.append and os.path.exists(args.output):
        first_save_append = True
    process_csv(
        args.csv, 
        args.output, 
        template_column=args.template_column,
        template1_column=args.template1_column,
        template2_column=args.template2_column,
        text1_column=args.text1_column,
        text2_column=args.text2_column,
        text3_column=args.text3_column,
        text4_column=args.text4_column,
        batch_size=args.batch_size,
        sleep_time=args.sleep,
        first_save_append=first_save_append  # 传递first_save_append参数
    )

if __name__ == "__main__":
    main()
    """
    python /home/user/opt/ssy/contract_template/embedding_new.py --csv /home/user/opt/ssy/contract_template/data/contract_new.csv --output /home/user/opt/ssy/contract_template/vector_new.json --batch-size 50 --append

    """