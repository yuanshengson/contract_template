# from FlagEmbedding import FlagModel
# model = FlagModel(model_name_or_path='/data/pbx/bge-unified/BGE-10000', query_instruction_for_retrieval="", use_fp16=True)

# import random

# # 常用汉字列表，可以根据需要扩展
# common_chinese_chars = [
#     '的', '一', '是', '在', '不', '了', '有', '和', '人', '这', 
#     '中', '大', '为', '上', '个', '国', '我', '要', '他', '们', 
#     '来', '时', '地', '出', '生', '会', '能', '对', '就', '作', 
#     '里', '子', '和', '对', '说', '年', '过', '自', '然', '那', 
#     '也', '得', '于', '如', '以', '道', '于', '看', '它', '过', 
#     '多', '到', '好', '很', '起', '下', '心', '你', '给', '等'
# ]

# def generate_sentence(length):
#     return ''.join(random.choice(common_chinese_chars) for _ in range(length))

# # # 输入句子的长度
# sentence_length = 100  # 可以根据需要调整
# random_sentence = generate_sentence(sentence_length)
# for i in range(100):
#     embeddings_1 = model.encode(random_sentence)
#     print(embeddings_1.shape)




# ## uvicorn main:app --host 0.0.0.0 --port 8101 --workers 2
# ## curl -X POST "http://127.0.0.1:8101/text2vector/" -H "Content-Type: application/json" -d "{\"text\": \"2015年10月至12月，朱清良、朱清涛在承包土地内非法开采建筑用砂89370.8立方米，价值人民币4468540元。经鉴定，朱清良二人非法开采的土地覆被类型为果园，地块内原生土壤丧失，原生态系统被完全破坏，生态系统服务能力严重受损，确认存在生态环境损害。鉴定机构确定生态环境损害恢复方案为将损害地块恢复为园林地，将地块内缺失土壤进行客土回填，下层回填普通土，表层覆盖60厘米种植土，使地块重新具备果树种植条件。恢复工程费用评估核算为2254578.58元。北京市人民检察院第四分院以朱清良、朱清涛非法开采造成土壤受损，破坏生态环境，损害社会公共利益为由提起环境民事公益诉讼（本案刑事部分另案审理）。2020年6月24日，朱清良、朱清涛的代理人朱某某签署生态环境修复承诺书，承诺按照生态环境修复方案开展修复工作。修复工程自2020年6月25日开始，至2020年10月15日完成。2020年10月15日，北京市房山区有关单位对该修复工程施工质量进行现场勘验，均认为修复工程依法合规、施工安全有序开展、施工过程中未出现安全性问题、环境污染问题，施工程序、工程质量均符合修复方案要求。施工过程严格按照生态环境修复方案各项具体要求进行，回填土壤质量符合标准，地块修复平整，表层覆盖超过60厘米的种植土，已重新具备果树种植条件。上述涉案土地内存在无法查明的他人倾倒的21392.1立方米渣土，朱清良、朱清涛在履行修复过程中对该部分渣土进行环境清理支付工程费用75.4万元。【裁判结果】北京市第四中级人民法院于2020年12月21日作出（2020）京04民初277号民事判决：一、朱清良、朱清涛对其造成的北京市房山区长阳镇朱岗子村西的14650.95平方米土地生态环境损害承担恢复原状的民事责任，确认朱清良、朱清涛已根据《房山区朱清良等人盗采砂石矿案生态环境损害鉴定评估报告书》确定的修复方案将上述受损生态环境修复到损害发生之前的状态和功能（已履行完毕）。二、朱清良、朱清涛赔偿生态环境受到损害至恢复原状期间的服务功能损失652896.75元；朱清良、朱清涛在履行本判决第一项修复义务时处理涉案地块上建筑垃圾所支付费用754000元折抵其应赔偿的生态环境受到损害至恢复原状期间的服务功能损失652896.75元。三、朱清良、朱清涛于本判决生效之日起七日内给付北京市人民检察院第四分院鉴定费115000元。四、朱清良、朱清涛在一家全国公开发行的媒体上向社会公开赔礼道歉，赔礼道歉的内容及媒体、版面、字体需经本院审核，朱清良、朱清涛应于本判决生效之日起十五日内向本院提交，并于审核通过之日起三十日内刊登，如未履行上述义务，则由本院选择媒体刊登判决主要内容，所需费用由朱清良、朱清涛负担。判决后，双方当事人均未提出上诉。\"}"
# import json

# def main(laws,status):
#     law_data = json.loads(laws)['data']
#     status_data = json.loads(status)['data']
#     laws_string = '检索出法条结果如下：\n'
#     status_string = '检索出法条结果如下：\n'
#     if law_data:
#         for index in range(len(law_data)):
#             res_string =f'法条内容{index+1}:' + law_data[index]["title"] + ',' \
#             + law_data[index]["title"] + ','  \
#             + law_data[index]["articleDetails"]['part'] + ','  \
#             + law_data[index]["articleDetails"]['chapter'] + ',' \
#             + law_data[index]["articleDetails"]['section'] + ','  \
#             + law_data[index]["articleDetails"]['article'] + ',' \
#             + law_data[index]["text"] 
#             laws_string +=res_string
#     else:
#         laws_string = ""
#     if status_data:

#         for index in range(len(status_data)):
#             res_string =f'法条内容{index+1}:' + status_string[index]["title"] + ',' \
#             + status_string[index]["title"] + ','  \
#             + status_string[index]["articleDetails"]['part'] + ','  \
#             + status_string[index]["articleDetails"]['chapter'] + ',' \
#             + status_string[index]["articleDetails"]['section'] + ','  \
#             + status_string[index]["articleDetails"]['article'] + ',' \
#             + status_string[index]["text"] 
#             status_string +=res_string
#     else:
#         status_string = ""
#     return {'result':laws_string+"\n"+status_string}




from fastapi import FastAPI
from pydantic import BaseModel
from FlagEmbedding import FlagModel

import torch
import psutil, os, time

# --- 初始化模型 ---
model = FlagModel(
    model_name_or_path='/data/pbx/bge-m3/BGE-M3', 
    query_instruction_for_retrieval="", 
    use_fp16=True
)

app = FastAPI()

class TextInput(BaseModel):
    text: str

# 获取当前进程对象，用于读 RAM
_proc = psutil.Process(os.getpid())
_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
torch.cuda.reset_peak_memory_stats(_device)

@app.post("/text2vector", include_in_schema=False)
@app.post("/text2vector/")
async def text2vector(input_data: TextInput):
    # 记录调用前资源
    t0 = time.time()
    ram_before = _proc.memory_info().rss / 1024**2
    vram_before = torch.cuda.memory_allocated(_device) / 1024**2

    # 实际推理
    embeddings_1 = model.encode(input_data.text)

    # 确保所有 CUDA 调用都完成
    if _device.type == "cuda":
        torch.cuda.synchronize(_device)

    # 记录调用后资源
    t1 = time.time()
    ram_after = _proc.memory_info().rss / 1024**2
    vram_after = torch.cuda.memory_allocated(_device) / 1024**2
    peak_vram = torch.cuda.max_memory_allocated(_device) / 1024**2

    # 打印或记录
    print(f"[text2vector] time={(t1-t0)*1000:.1f} ms | "
          f"RAM Δ={(ram_after-ram_before):.1f} MiB | "
          f"VRAM Δ={(vram_after-vram_before):.1f} MiB | "
          f"VRAM peak={peak_vram:.1f} MiB")

    return {"result": embeddings_1.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8035, 
        log_level="info"
    )
