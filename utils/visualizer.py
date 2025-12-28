import cv2

def apply_visual_grounding(video_path, timestamp, bbox, label, output_path):
    cap = cv2.VideoCapture(video_path)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        curr_ts = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        
        # 匹配时间戳，并在目标位置绘制红框
        if abs(curr_ts - timestamp) < 0.5 and len(bbox) == 4:
            # 还原归一化坐标
            x1 = int(bbox[0] * w / 1000)
            y1 = int(bbox[1] * h / 1000)
            x2 = int(bbox[2] * w / 1000)
            y2 = int(bbox[3] * h / 1000)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        out.write(frame)
    
    cap.release()
    out.release()