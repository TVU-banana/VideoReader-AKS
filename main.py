import os
import cv2
from core.aks_sampler import AKSSampler
from core.qwen_inference import call_qwen_vl_api
from utils.visualizer import apply_visual_grounding
from core.logger_config import logger

def main():
    # 1. 初始化设置
    API_KEY = "YOUR_DASHSCOPE_API_KEY" 
    VIDEO_PATH = "data/test_video.mp4"
    QUERY = "找到视频中正在写字的人"
    
    # 创建必要目录
    os.makedirs("data/temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    logger.info("系统启动：开始处理流程...")
    sampler = AKSSampler()
    
    # 2. 执行 AKS 抽帧
    logger.info("步骤 1: 正在进行 AKS 自适应采样...")
    keyframes = sampler.extract_keyframes(VIDEO_PATH)
    
    if not keyframes:
        logger.error("未提取到关键帧，程序终止。")
        return

    # 3. 保存临时帧供 API 调用
    img_paths = []
    for i, kf in enumerate(keyframes[:20]): # 限制帧数以控制 Token 消耗
        path = f"data/temp/f_{i}.jpg"
        cv2.imwrite(path, kf['frame'])
        img_paths.append(path)

    # 4. 调用 Qwen3-VL 分析 (此处保留模拟逻辑，实际运行请取消 API 注释)
    logger.info(f"步骤 2: 请求 Qwen3-VL 语义理解，发送帧数: {len(img_paths)}")
    # result_text = call_qwen_vl_api(API_KEY, img_paths, QUERY)
    
    # 模拟模型返回的 Grounding 结果
    mock_result = {"timestamp": 2.5, "bbox": [150, 200, 450, 600], "label": "Writing Person"}
    
    # 5. 可视化导出
    logger.info("步骤 3: 正在生成带标注的成品视频...")
    apply_visual_grounding(VIDEO_PATH, mock_result['timestamp'], mock_result['bbox'], 
                           mock_result['label'], "output/final_analysis.mp4")
    
    logger.info("项目运行成功！请检查 output/final_analysis.mp4")

if __name__ == "__main__":
    main()