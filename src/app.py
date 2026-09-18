# src/app.py
import cv2
from camera import Camera
from pose import PoseEstimator
from analysis import PostureAnalyzer, POSTURE_THRESHOLD

def main():
    print("🚀 体育体态纠正工具启动...")
    cam = Camera()
    estimator = PoseEstimator()
    analyzer = PostureAnalyzer(threshold=POSTURE_THRESHOLD)

    while True:
        #输入层：读取一帧画面
        frame = cam.read()
        if frame is None:
            print("X 无法读取摄像头画面")
            break

        # 视觉层：识别骨骼并画火柴人
        processed_frame, landmarks = estimator.process(frame)

        # 分析层：计算姿态角度，判断是否低头/驼背
        result = analyzer.analyze(landmarks)

        if result:
            # 表现层：根据判定结果，在画面上叠加文字（红绿提示）
            color = (0, 255, 0) if result["status"] == "GOOD" else (0, 0, 255)
            cv2.putText(processed_frame, f"Angle: {result['angle']}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(processed_frame, f"Status: {result['status']}", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # 显示画面（暂时用 OpenCV 显示）
        cv2.imshow("Posture Correction", processed_frame)

        # 按 'q' 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cam.release()

if __name__ == "__main__":
    main()