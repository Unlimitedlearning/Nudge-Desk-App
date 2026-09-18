# src/app.py
import cv2
from camera import Camera
from pose import PoseEstimator

def main():
    print("🚀 体育体态纠正工具启动...")
    cam = Camera()
    estimator = PoseEstimator()

    while True:
        # 1. 输入层：读取一帧画面
        frame = cam.read()
        if frame is None:
            print("X 无法读取摄像头画面")
            break

        # 2. 视觉层：识别骨骼并画火柴人
        processed_frame, landmarks = estimator.process(frame)

        # 3. 表现层：显示画面（暂时用 OpenCV 显示）
        cv2.imshow("Posture Correction", processed_frame)

        # 4. 按 'q' 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cam.release()

if __name__ == "__main__":
    main()