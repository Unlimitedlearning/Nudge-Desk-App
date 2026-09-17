import cv2
import mediapipe as mp

# 1. 初始化 MediaPipe 姿态识别模块
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# 2. 打开电脑摄像头 (0 代表默认摄像头)
cap = cv2.VideoCapture(0)

print("🚀 摄像头已启动，按 'q' 键退出...")

while cap.isOpened():
    # 读取视频帧
    success, frame = cap.read()
    if not success:
        print("无法读取摄像头，请检查设备连接。")
        break

    # 3. 图像预处理：OpenCV读取的是BGR，MediaPipe需要RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 4. 核心推理：让MediaPipe识别图像中的姿态
    results = pose.process(image)

    # 5. 绘制骨架：把识别出来的火柴人画回画面中
    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2), # 关节（绿色）
            mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)                    # 连接线（红色）
        )

    # 6. 显示画面
    cv2.imshow('Sports Posture Correction - Demo', frame)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()