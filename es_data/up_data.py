import json
import re
from elasticsearch import Elasticsearch

es_host = "http://192.168.10.202:9200/"
es = Elasticsearch([es_host])

index_name = "contract_templates"

index_mapping = {
    "mappings": {
      "doc": {
        "properties": {
          "parts": {
            "properties": {
              "text1": {
                "type": "text"
              },
              "text2": {
                "type": "text"
              },
              "text3": {
                "type": "text"
              },
              "text4": {
                "type": "text"
              }
            }
          },
          "template": {
            "type": "keyword"
          },
          "template1": {
            "type": "keyword"
          },
          "template2": {
            "type": "keyword"
          },
          "vectors": {
            "properties": {
              "text1": {
                "type": "float"
              },
              "text2": {
                "type": "float"
              },
              "text3": {
                "type": "float"
              },
              "text4": {
                "type": "float"
              }
            }
          }
        }
      }
    }
}

if es.indices.exists(index=index_name):
    print(f"索引 {index_name} 已存在，正在删除...")
    es.indices.delete(index=index_name)
    print(f"索引 {index_name} 已删除")

print(f"正在创建索引 {index_name}...")
es.indices.create(index=index_name, body=index_mapping)
print(f"索引 {index_name} 创建成功")

try:
    with open(r"/home/user/opt/ssy/contract_template/data/vector_data/vector_new.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if data and len(data) > 0:
        print("\nvector_new.json 数据格式示例:")
        print(json.dumps(data[0], ensure_ascii=False, indent=2))
        print(f"\n共有 {len(data)} 条数据待导入")
    
    def extract_chinese(text):
        if not text:
            return ""
        return re.sub(r'\b\d+_|\_\d+\b', '', text)
    
    bulk_data = []
    for i, item in enumerate(data):
        if "template" in item:
            original_template = item["template"]
            item["template"] = extract_chinese(original_template)
            if original_template != item["template"]:
                print(f"模板名称已更新: '{original_template}' -> '{item['template']}'")
        
        index_action = {
            "index": {
                "_index": index_name,
                "_type": "doc",
                "_id": str(i)
            }
        }
        bulk_data.append(index_action)
        bulk_data.append(item)
    
    if bulk_data:
        response = es.bulk(body=bulk_data, refresh=True)
        
        if response.get("errors", False):
            print("导入数据时出现错误:")
            for item in response["items"]:
                if "error" in item["index"]:
                    print(item["index"]["error"])
        else:
            print(f"成功导入 {len(data)} 条数据到索引 {index_name}")
    else:
        print("没有数据需要导入")
        
except FileNotFoundError:
    print("找不到 vector_new.json 文件，请确保文件路径正确")
except json.JSONDecodeError:
    print("vector_new.json 文件格式不正确，无法解析 JSON")
except Exception as e:
    print(f"导入数据时发生错误: {str(e)}")

# 验证索引是否创建成功
if es.indices.exists(index=index_name):
    print(f"索引 {index_name} 创建并导入数据成功")
    
    # 获取索引映射
    mapping = es.indices.get_mapping(index=index_name)
    print("\n索引映射结构:")
    print(json.dumps(mapping, ensure_ascii=False, indent=2))
    
    # 获取索引中的文档数量
    count = es.count(index=index_name)
    print(f"\n索引中共有 {count['count']} 条文档")
    
    # 获取一条示例文档
    if count['count'] > 0:
        print("\n示例文档:")
        sample = es.search(
            index=index_name,
            body={
                "size": 1,
                "query": {"match_all": {}}
            }
        )
        if sample['hits']['hits']:
            print(json.dumps(sample['hits']['hits'][0]['_source'], ensure_ascii=False, indent=2))
else:
    print(f"索引 {index_name} 创建失败")