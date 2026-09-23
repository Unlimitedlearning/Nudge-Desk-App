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
from config_manager import load_calibration, save_calibration

# 全局变量（方便在 UI 的循环里调用）
cam = None
estimator = None
analyzer = None
widget = None
last_log_time = 0

# 校准相关状态
app_state = "NORMAL"      # NORMAL / CALIBRATING
calib_frames = 0          # 校准计时器
calib_angles = []         # 收集的角度

def process_frame():
    """每 30 毫秒调用一次，处理一帧摄像头画面"""
    global cam, estimator, analyzer, widget, last_log_time
    global app_state, calib_frames, calib_angles

    # 1. 读取摄像头
    frame = cam.read()
    if frame is None:
        widget.root.after(30, process_frame)
        return  #读取到内容才进行后续处理

    # 2. 视觉层与分析层
    processed_frame, landmarks = estimator.process(frame)
    result = analyzer.analyze(landmarks)

    # 3. 状态机分流
    if app_state == "CALIBRATING":
        # 校准状态下，不进行报警，只收集角度
        if result:
            angle = result["posture"]["angle"]
            calib_angles.append(angle)
        calib_frames += 1
        
        # 显示倒计时（5秒，假设30ms一帧，约233帧，我们简化用帧计数算秒数）
        remaining = max(0, 5 - int(calib_frames * 0.03))
        widget.update_status(status="CALIBRATING", angle=remaining)
        
        if calib_frames >= 166:  # 约5秒
            # 计算基准阈值
            if calib_angles:
                avg_angle = sum(calib_angles) / len(calib_angles)
                # 基准角度减去 6 度作为报警阈值（可根据实际情况微调）
                new_threshold = avg_angle - 4 
                save_calibration(new_threshold)
                analyzer.threshold = new_threshold
                print(f"✅ 校准完成：基准角度 {avg_angle:.1f}°，阈值设为 {new_threshold:.1f}°")
            else:
                print("⚠️ 校准失败，未收集到数据")
            
            # 重置状态，回到常规检测
            app_state = "NORMAL"
            calib_frames = 0
            calib_angles = []
            widget.update_status(status="GOOD", angle=0)
    else:
        # 常规检测逻辑（原封不动）
        if result:
            posture_data = result["posture"]
            # 写入 CSV 日志的逻辑（略，保持原样）
            
            # 推送给 UI
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
    global cam, estimator, analyzer, widget, app_state
    print("🚀 Nudge-Desk-App 启动...")

    # 1. 先创建悬浮窗 UI，让它立刻弹出来
    widget = DesktopWidget()
    widget.update_status("初始化...")
    widget.root.update()  # 强制让 Tkinter 立刻渲染出 UI 窗口

    # 注入“重新校准”的回调
    def start_recalibration():
        global app_state, calib_frames, calib_angles
        app_state = "CALIBRATING"
        calib_frames = 0
        calib_angles = []
        print("📐 手动触发重新校准...")
    
    widget.on_recalibrate = start_recalibration

    # 2. 然后再加载比较耗时的摄像头和 AI 模型
    cam = Camera()
    estimator = PoseEstimator()
    analyzer = PostureAnalyzer(threshold=POSTURE_THRESHOLD)
    
    # 加载本地配置
    saved_threshold = load_calibration()
    if saved_threshold:
        analyzer.threshold = saved_threshold
        print(f"✅ 已加载本地校准配置，阈值为：{saved_threshold:.1f}°")
        app_state = "NORMAL"
        widget.root.after(0, process_frame)
    else:
        print("📐 首次运行，启动 7 秒个性化校准...")
        app_state = "CALIBRATING"
        widget.update_status(status="CALIBRATING", angle=7)
        widget.root.after(0, process_frame)     # 启动检测循环

    # 4. 启动 UI 主循环（这会接管整个程序的运行）
    widget.start()

if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception as e:
        # 把真实报错写到本地文件，方便排查
        with open("crash_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        print("❌ 程序崩溃，已将错误写入 crash_log.txt")
        import time
        time.sleep(10)  # 留10秒让你看控制台