import cv2
import numpy as np
import os
# 修改为绝对导入或确保在项目根目录运行
try:
    from .logger_config import logger
except ImportError:
    from core.logger_config import logger

class AKSSampler:
    def __init__(self, threshold=30.0, min_interval=15):
        self.threshold = threshold
        self.min_interval = min_interval
        self.total_frames_count = 0

    def extract_keyframes(self, video_path):
        if not os.path.exists(video_path):
            logger.error(f"视频路径不存在: {video_path}")
            return []

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"无法打开视频文件: {video_path}")
            return []

        self.total_frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        logger.info(f"成功加载视频 | 总帧数: {self.total_frames_count} | FPS: {fps:.2f}")

        keyframes = []
        prev_frame_processed = None
        frame_idx = 0
        last_kept_idx = -self.min_interval # 确保第一帧被选中

        try:
            while True:
                ret, frame = cap.read()
                if not ret: break

                # 预处理：缩小+灰度+高斯模糊以减少噪点
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                small_frame = cv2.resize(gray, (64, 64))
                curr_frame_processed = cv2.GaussianBlur(small_frame, (5, 5), 0)

                if prev_frame_processed is not None:
                    # 使用 L1 范数计算帧间差异
                    diff_score = cv2.norm(curr_frame_processed, prev_frame_processed, cv2.NORM_L1)
                    avg_diff = diff_score / float(small_frame.size)

                    is_significant = avg_diff > self.threshold
                    is_time_up = (frame_idx - last_kept_idx) >= self.min_interval

                    if is_significant or is_time_up:
                        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                        keyframes.append({
                            'frame': frame.copy(),
                            'timestamp': round(timestamp, 2),
                            'frame_idx': frame_idx,
                            'cause': "motion" if is_significant else "interval"
                        })
                        last_kept_idx = frame_idx
                        prev_frame_processed = curr_frame_processed
                else:
                    # 记录初始帧
                    keyframes.append({'frame': frame.copy(), 'timestamp': 0.0, 'frame_idx': 0, 'cause': "initial"})
                    prev_frame_processed = curr_frame_processed
                    last_kept_idx = 0

                frame_idx += 1
                if self.total_frames_count > 0 and frame_idx % max(1, self.total_frames_count // 10) == 0:
                    progress = (frame_idx / self.total_frames_count) * 100
                    logger.info(f"采样进度: {progress:.1f}% ...")
        finally:
            cap.release()

        compression_rate = (1 - len(keyframes) / max(1, self.total_frames_count)) * 100
        logger.info(f"AKS 任务结束 | 关键帧: {len(keyframes)} | 压缩率: {compression_rate:.2f}%")
        return keyframes