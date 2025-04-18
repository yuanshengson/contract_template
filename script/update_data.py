import json
import csv
import os

csv_path = "/home/user/opt/ssy/contract_template/data/contrac_csv/contract_4_15_500.csv"
json_path = "/home/user/opt/ssy/contract_template/data/vector_data/vector_new.json"

csv_key_column_index = 1    
csv_value_column_index = 13

json_target_field = ["template2"]

# 添加调试信息收集
duplicate_keys = set()
csv_updates = {}
try:
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) > max(csv_key_column_index, csv_value_column_index):
                key = row[csv_key_column_index]
                value = row[csv_value_column_index]
                if key:
                    # 检查是否有重复key
                    if key in csv_updates:
                        duplicate_keys.add(key)
                    csv_updates[key] = value
except Exception as e:
    print(f"读取CSV文件时出错: {str(e)}")
    exit(1)

print(f"从CSV中读取了 {len(csv_updates)} 条更新数据")
if duplicate_keys:
    print(f"发现 {len(duplicate_keys)} 个重复的key，这些key的最后一个值会覆盖前面的值")

# 收集未找到匹配的key
not_found_keys = set(csv_updates.keys())
try:
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
except Exception as e:
    print(f"读取JSON文件时出错: {str(e)}")
    exit(1)

update_count = 0

if isinstance(json_data, list):
    for item in json_data:
        key = item.get("template")
        if key in csv_updates:
            if "parts" not in item:
                item["parts"] = {}
            item["template2"] = csv_updates[key]
            update_count += 1
            # 从未找到匹配的集合中移除已更新的key
            if key in not_found_keys:
                not_found_keys.remove(key)
else:
    print("不支持的JSON数据格式")
    exit(1)

# 输出未找到匹配的key的数量
if not_found_keys:
    print(f"有 {len(not_found_keys)} 个key在JSON数据中未找到匹配项")
    # 如果数量不多，可以打印出来看看是哪些key
    if len(not_found_keys) <= 10:
        print(f"未匹配的key: {', '.join(not_found_keys)}")

try:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"成功更新了 {update_count} 条记录")
except Exception as e:
    print(f"保存JSON文件时出错: {str(e)}")
    exit(1)