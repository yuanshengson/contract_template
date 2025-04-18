input = {
  "arg1":  [
    "user:我需要一份北京市限额以下小型工程施工合同模板，用于和施工单位签订工程协议。",
    "assistant:标的信息：本合同涉及的标的为北京市限额以下小型工程，具体工程范围和施工内容需在合同中详细列明，包括但不限于土建、安装、装饰等分项工程。工程范围应明确地理位置、面积、结构类型等要素，施工内容需细化至材料规格、工艺标准及特殊技术要求（如防水、抗震等级）。附件可附工程量清单、施工图纸作为补充说明。\n\n主体信息：合同双方为发包方与施工单位，其中发包方在合同中处于中立地位，不偏向任何一方，主要行使监督、验收等权利；施工单位作为承包方，需具备相应资质，并在合同中明确企业名称、统一社会信用代码、项目负责人信息。双方联系人及通讯方式需单独列明条款。\n\n价款与支付信息：计价方式可选择固定总价或单价计费，需注明是否含税及税率；付款批次约定按进度付款（需划分形象进度节点及对应支付比例）或首尾款（如预付款30%、竣工款60%、质保金10%）。支付方式限定银行转账，需写明收款账户信息、发票开具要求及逾期付款的违约金计算标准。\n\n履行条款信息：工期需标注日历天及起止日期，并约定雨雪天气、不可抗力的处理方式；工程验收分阶段明确（如隐蔽工程验收、竣工验收），标准需引用国标或行业规范；施工进度管理要求施工单位提交甘特图、周报，延误需按日计罚金；质量保证期不少于2年，需明确保修范围、响应时间及质保金返还条件。可附验收单模板作为附件。",
    "user:确认"
  ]
}
import json
import re

def get_last_assistant_reply(history: list) -> str:
    for item in reversed(history):
        if item.startswith("assistant:"):
            return item[len("assistant:"):].strip()
    return ""

def clean_for_json(text: str) -> str:
    return json.dumps(text.strip().replace('\n', '').replace('\\n', ''),ensure_ascii=False)[1:-1]

def main1(arg1):
    output = get_last_assistant_reply(arg1)

    pattern = (
        r"标的.+?：(.+?)"
        r"主体信息：(.+?)"
        r"价款与支付信息：(.+?)"
        r"履行信息：(.+)"
    )

    match = re.search(pattern, output, re.DOTALL)
    
    if match:
        text1 = clean_for_json(match.group(1))
        text2 = clean_for_json(match.group(2))
        text3 = clean_for_json(match.group(3))
        text4 = clean_for_json(match.group(4))
    else:
        text1 = text2 = text3 = text4 = ""

    return {
        "text1": text1,
        "text2": text2,
        "text3": text3,
        "text4": text4
    }

def main(arg1):
    output = get_last_assistant_reply(arg1)

    pattern = (
    r"标的[物的]*信息：(.+?)"
    r"\s*主体信息：(.+?)"
    r"\s*价款与支付信息：(.+?)"
    r"\s*履行[条款的]*信息：(.+)"
)




    match = re.search(pattern, output, re.DOTALL)
    
    if match:
        text1 = match.group(1).strip().replace('\n', '').replace('\\n', '')
        text2 = match.group(2).strip().replace('\n', '').replace('\\n', '')
        text3 = match.group(3).strip().replace('\n', '').replace('\\n', '')
        text4 = match.group(4).strip().replace('\n', '').replace('\\n', '')
    else:
        text1 = text2 = text3 = text4 = ""

    return {
        "text1": text1,
        "text2": text2,
        "text3": text3,
        "text4": text4
    }

historylist =  ['user:我要在浙江省内的实体店购买成品家具，请提供一份家具买卖合同模板。', 'assistant:标的物信息：本合同涉及的标的为成品家具，包括家具的规格、型号、数量等具体信息，需在合同中明确列出。  \\n主体信息：本合同主体为买方（中立地位）与卖方，双方需在合同中明确身份信息（如名称、地址、联系方式等）。  \\n价款与支付信息：合同采用固定总价计价方式，付款批次为定金+尾款（交货前付清），付款方式为银行转账或现金。  \\n\\n履行条款信息：合同需明确交货时间、地点及方式，并约定验收标准（如外观、质量等）。买方应在验收合格后支付尾款。若交货延迟或货物不符约定，需规定违约责任（如违约金或解除合同）。此外，可附加争议解决条款（如协商或诉讼）。附件可包括家具详细清单、技术参数及验收标准等。', 'user:确认']

# print(get_last_assistant_reply(historylist))
print(main(historylist))