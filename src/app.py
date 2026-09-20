# src/app.py
"""
控制层：程序主入口与调度中心。
职责：串联输入层、视觉层、分析层与表现层，通过事件驱动循环（root.after）实现流畅调用。
依赖：camera, pose, analysis, ui
"""

import time
import os
import csv

from camera import Camera
from pose import PoseEstimator
from analysis import PostureAnalyzer, POSTURE_THRESHOLD
from ui import DesktopWidget

# 全局变量（方便在 UI 的循环里调用）
cam = None
estimator = None
analyzer = None
widget = None
last_log_time = 0

def process_frame():
    """每 30 毫秒调用一次，处理一帧摄像头画面"""
    global cam, estimator, analyzer, widget, last_log_time

    # 1. 读取摄像头
    frame = cam.read()
    
    # 如果读取到了画面，就进行处理
    if frame is not None:
        # 2. 视觉层：识别骨骼
        processed_frame, landmarks = estimator.process(frame)
        # 3. 分析层：计算姿态角度与疲劳值
        result = analyzer.analyze(landmarks)

        if result:
            posture_data = result["posture"]

            if time.time() - last_log_time > 5: # 每5秒记录一次
                    os.makedirs("data/raw", exist_ok=True)  # 存进你规划的data目录里
                    with open("data/raw/local_test_log.csv", "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            time.strftime("%Y-%m-%d %H:%M:%S"), 
                            posture_data["status"], 
                            posture_data["angle"], 
                            posture_data["neck_fatigue"],
                            posture_data["is_tilted"],
                            posture_data["is_too_close"]
                        ])
                    last_log_time = time.time()

            # 4. 把计算结果直接推送给 UI 悬浮窗
            widget.update_status(
                status=posture_data["status"],
                angle=posture_data["angle"],
                neck_fatigue=posture_data["neck_fatigue"],
                is_tilted=posture_data["is_tilted"],
                is_too_close=posture_data["is_too_close"]
            )

    # 🌟 核心：在 UI 主线程里循环调用自己，而不是用 while True
    widget.root.after(30, process_frame)

def main():
    global cam, estimator, analyzer, widget
    print("🚀 体育体态纠正工具启动...")

    # 1. 先创建悬浮窗 UI，让它立刻弹出来
    widget = DesktopWidget()
    widget.update_status("未检测到人")
    widget.root.update()  # 强制让 Tkinter 立刻渲染出 UI 窗口

    # 2. 然后再加载比较耗时的摄像头和 AI 模型
    cam = Camera()
    estimator = PoseEstimator()
    analyzer = PostureAnalyzer(threshold=POSTURE_THRESHOLD)
    
    print("✅ 模块初始化完成，开始进入检测循环...")

    # 3. 启动检测循环
    widget.root.after(0, process_frame)

    # 4. 启动 UI 主循环（这会接管整个程序的运行）
    widget.start()

if __name__ == "__main__":
    main()