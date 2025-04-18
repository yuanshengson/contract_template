import json
import os

template_to_delete = "港口作业合同_919325807132807168"

file_path = "/home/user/opt/ssy/contract_template/vector_new.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

original_count = len(data)

filtered_data = [item for item in data if item.get("template") != template_to_delete]

new_count = len(filtered_data)
deleted_count = original_count - new_count

print(f"原始数据总数：{original_count}")
print(f"删除后的数据总数：{new_count}")
print(f"删除了 {deleted_count} 条数据")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)