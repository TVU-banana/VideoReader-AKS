import os
import dashscope
from dashscope import MultiModalConversation

def call_qwen_vl_api(api_key, image_paths, query):
    dashscope.api_key = api_key
    
    # 构建符合 Qwen3-VL 规范的多模态消息
    content = [{"text": f"{query}。请在分析结果中包含目标的 [x1, y1, x2, y2] 归一化坐标。"}]
    
    for img_path in image_paths:
        content.append({"image": f"file://{os.path.abspath(img_path)}"})

    responses = MultiModalConversation.call(
        model='qwen-vl-max',
        messages=[{"role": "user", "content": content}],
        result_format='message'
    )

    if responses.status_code == 200:
        return responses.output.choices[0].message.content[0]['text']
    else:
        return f"API Error: {responses.message}"