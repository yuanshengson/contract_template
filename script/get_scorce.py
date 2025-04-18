import json

def main(arg1):
    data = json.loads(arg1)
    templates = data["templates"]
    scores = data["scores"]
    similarities = data["similarities"]
    category_scores = data.get("category_scores", [])
    
    result = "\n\n推荐的合同模板（按匹配度排序）：\n"
    
    for i in range(len(templates)):
        template_name = templates[i]
        total_score = scores[i]
        result += f"\n{i+1}. 【{template_name}】 总匹配度: {total_score:.1f}分\n"
        
        if category_scores and i < len(category_scores):
            cat_score = category_scores[i]
            template1_score = cat_score.get("template1", 0)
            template2_score = cat_score.get("template2", 0)
            
            if template1_score > 0:
                result += f"   ✓ 一级分类匹配 (+5分)\n"
            else:
                result += f"   ✗ 一级分类不匹配 (0分)\n"
                
            if template2_score > 0:
                result += f"   ✓ 二级分类匹配 (+5分)\n"
            else:
                result += f"   ✗ 二级分类不匹配 (0分)\n"

        result += f"   • 合同标的相似度: {similarities['text1'][i]:.1f}% (权重: 27)\n"
        result += f"   • 合同主体相似度: {similarities['text2'][i]:.1f}% (权重: 27)\n"
        result += f"   • 合同价款与支付相似度: {similarities['text3'][i]:.1f}% (权重: 18)\n"
        result += f"   • 合同交易条款相似度: {similarities['text4'][i]:.1f}% (权重: 18)\n"
    
    result += "\n以上是根据您提供的信息，系统推荐的最匹配合同模板。"
    
    return {
        "result": result,
        "scores": str(scores)
    }