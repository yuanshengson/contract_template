from elasticsearch import Elasticsearch

es = Elasticsearch(["http://192.168.10.202:9200"])

index_name = "contract_templates"

# elasticsearch 6.5
index_mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "doc": {
            "properties": {
                "template": {"type": "keyword"},
                "template1": {"type": "keyword"},
                "template2": {"type": "keyword"},
                "parts": {
                    "properties": {
                        "text1": {"type": "text"},
                        "text2": {"type": "text"},
                        "text3": {"type": "text"},
                        "text4": {"type": "text"}
                    }
                },
                "vectors": {
                    "properties": {
                        "text1": {"type": "object"},
                        "text2": {"type": "object"},
                        "text3": {"type": "object"},
                        "text4": {"type": "object"}
                    }
                }
            }
        }
    }
}


# 创建索引
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_mapping)
    print(f"索引 {index_name} 创建成功 ✅")
else:
    print(f"索引 {index_name} 已存在")
