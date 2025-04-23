import json
from elasticsearch import Elasticsearch

# 连接到Elasticsearch
es_host = "http://192.168.10.202:9200/"
es = Elasticsearch([es_host])

# 定义索引名称
index_name = "contract_templates"

# 检查索引是否存在
if es.indices.exists(index=index_name):
    # 获取索引中的文档数量
    count = es.count(index=index_name)
    print(f"索引 {index_name} 中共有 {count['count']} 条文档")
else:
    print(f"索引 {index_name} 不存在")