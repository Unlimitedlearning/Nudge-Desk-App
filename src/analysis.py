# src/analysis.py
import math
from collections import deque

POSTURE_THRESHOLD = 165  # 体态判定阈值
SMOOTH_WINDOW = 5        # 滑动窗口大小

class PostureAnalyzer:
    def __init__(self, threshold=165, smooth_window=5):
        # 判定阈值：低于此角度视为不良体态，后期应该可以增加校准机制，个性化适配
        self.threshold = threshold

        # 滑动窗口大小：用于平滑坐标，窗口越大越平滑但延迟越高
        self.smooth_window = smooth_window

        # 存储历史的平滑点队列 (耳, 肩, 髋)
        self.ear_history = deque(maxlen=smooth_window)
        self.shoulder_history = deque(maxlen=smooth_window)
        self.hip_history = deque(maxlen=smooth_window)

    def get_center_point(self, p1, p2):
        """计算两个点的中心点 (三维)"""
        return (
            (p1.x + p2.x) / 2.0,
            (p1.y + p2.y) / 2.0,
            (p1.z + p2.z) / 2.0
        )

    def calculate_3d_angle(self, p1, p2, p3):
        """
        计算三维空间中，三点 p1(耳), p2(肩), p3(髋) 的夹角
        p1, p2, p3 均为 (x, y, z) 元组
        """
        # 向量 p2->p1 和 p2->p3
        v1 = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
        v2 = (p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2])

        # 点积
        dot_product = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
        # 模长
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)

        if mag1 == 0 or mag2 == 0:
            return 180.0

        # 防止浮点数精度问题导致 acos 报错（边界保护，结果应该永远在 [-1.0, 1.0] 之间）
        cos_angle = max(-1.0, min(1.0, dot_product / (mag1 * mag2)))
        return math.degrees(math.acos(cos_angle))
        #反余弦函数+弧度制转角度制

    def analyze(self, landmarks):
        """
        输入：MediaPipe 的 landmarks
        输出：包含角度、状态、平滑后数据的字典
        """
        if not landmarks:
            return None

        try:
            # 提取左右两侧的关键点 (MediaPipe 索引)
            # 耳：7(左), 8(右)
            # 肩：11(左), 12(右)
            # 髋：23(左), 24(右)
            ear_l = landmarks.landmark[7]
            ear_r = landmarks.landmark[8]
            shoulder_l = landmarks.landmark[11]
            shoulder_r = landmarks.landmark[12]
            hip_l = landmarks.landmark[23]
            hip_r = landmarks.landmark[24]
        except IndexError:
            return None

        # 1. 计算中轴点
        center_ear = self.get_center_point(ear_l, ear_r)
        center_shoulder = self.get_center_point(shoulder_l, shoulder_r)
        center_hip = self.get_center_point(hip_l, hip_r)

        # 2. 放入历史队列进行平滑
        self.ear_history.append(center_ear)
        self.shoulder_history.append(center_shoulder)
        self.hip_history.append(center_hip)

        # 3. 计算平滑后的平均值
        avg_ear = (sum(p[0] for p in self.ear_history)/len(self.ear_history),
                   sum(p[1] for p in self.ear_history)/len(self.ear_history),
                   sum(p[2] for p in self.ear_history)/len(self.ear_history))
        avg_shoulder = (sum(p[0] for p in self.shoulder_history)/len(self.shoulder_history),
                        sum(p[1] for p in self.shoulder_history)/len(self.shoulder_history),
                        sum(p[2] for p in self.shoulder_history)/len(self.shoulder_history))
        avg_hip = (sum(p[0] for p in self.hip_history)/len(self.hip_history),
                   sum(p[1] for p in self.hip_history)/len(self.hip_history),
                   sum(p[2] for p in self.hip_history)/len(self.hip_history))

        # 4. 计算三维夹角
        angle = self.calculate_3d_angle(avg_ear, avg_shoulder, avg_hip)

        # 5. 判定状态
        status = "GOOD" if angle >= self.threshold else "BAD"

        return {
            "angle": round(angle, 2),
            "status": status
        }


# 测试代码
if __name__ == "__main__":
    from camera import Camera
    from pose import PoseEstimator
    import cv2

    cam = Camera()
    estimator = PoseEstimator()
    analyzer = PostureAnalyzer(POSTURE_THRESHOLD)

    print("🚀 开始体态检测（三维平滑版）...")
    print("💡 提示：请把摄像头放在你的侧前方约45度位置。")

    while True:
        frame = cam.read()
        if frame is None: break

        processed_frame, landmarks = estimator.process(frame)
        result = analyzer.analyze(landmarks)

        if result:
            color = (0, 255, 0) if result["status"] == "GOOD" else (0, 0, 255)
            cv2.putText(processed_frame, f"Angle: {result['angle']}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(processed_frame, f"Status: {result['status']}", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Posture Analysis Test", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cam.release()