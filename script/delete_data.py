import json
import os

# 要删除的模板列表
templates_to_delete = [
    "浙江省医院陪护服务合同_919324133915889664",
    "天津市二手机动车买卖合同_919325790565306368",
    "工业品买卖合同_919326035453939712",
    "农副产品买卖合同_919324024847208448",
    "化肥买卖合同_919325795678162944",
    "粮食买卖合同_919324155696910336",
    "棉花买卖合同_919325811981422592",
    "水路货物运输合同_919324141348196352",
    "海南省建设工程检测合同_919323891598364672",
    "商品代销合同_919324982532640768",
    "修缮修理合同_919323902495166464",
    "煤炭买卖合同_919325777105784832",
    "加工合同_919324129578979328",
    "赠与合同_919325947839123456",
    "居间合同_919323888461025280",
    "国内快递服务协议_919324831269261312",
    "广告发布业务合同_919325813684310016",
    "烟花爆竹安全买卖合同_919324816601780224",
    "委托合同_919324852551159808",
    "家具买卖合同_919323652149743616",
    "民用爆破器材买卖合同_919323656419545088",
    "行纪合同_919324042215821312",
    "地质机械仪器产品买卖合同　_919323666137747456",
    "煤矿机电产品买卖合同_919323663415644160",
    "木材买卖（订货）合同_919325806516244480",
    "航次租船合同_919325813315211264",
    "铁路货物运输合同_919325815571746816",
    "水陆联运货物运输合同_919325983150968832",
    "钢材买卖（订货）合同_919324134893162496",
    "木材买卖合同_919325958257774592",
    "水泥买卖合同_919325004074586112"
]

file_path = "/home/user/opt/ssy/contract_template/data/vector_data/vector_new.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

original_count = len(data)

filtered_data = [item for item in data if item.get("template") not in templates_to_delete]

new_count = len(filtered_data)
deleted_count = original_count - new_count

print(f"原始数据总数：{original_count}")
print(f"删除后的数据总数：{new_count}")
print(f"删除了 {deleted_count} 条数据")

for template in templates_to_delete:
    template_deleted_count = len([item for item in data if item.get("template") == template])
    if template_deleted_count > 0:
        print(f"删除 '{template}' 的数据：{template_deleted_count} 条")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)