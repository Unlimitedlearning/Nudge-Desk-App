# src/pose.py
import cv2
import mediapipe as mp

class PoseEstimator:
    def __init__(self):
        """初始化 MediaPipe 姿态识别模型"""
        self.mp_pose = mp.solutions.pose
        #在__init__里进行一次模型实例化，避免process里面反复创建消耗内存

        self.pose = self.mp_pose.Pose(
            min_detection_confidence = 0.5,   # 最小检测置信度50%
            min_tracking_confidence = 0.5    #最小追踪置信度50%
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process(self,frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 图像预处理：OpenCV读取的是BGR，MediaPipe需要RGB

        results = self.pose.process(image_rgb)
        # 调用MediaPipe识别图像中的姿态

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,    #画布 把骨骼图画在原始的摄像头画面上
                results.pose_landmarks,    #数据 AI识别出的关节坐标点
                self.mp_pose.POSE_CONNECTIONS,    #连接规则 

                #关节（绿色）
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), #绿色
                                            thickness=2,#线条粗细
                                            circle_radius=2#圆点半径
                                            ),

                #连接线（红色）
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), #红色
                                            thickness=2
                                            )
            )

        #把画好的画面和原始骨骼数据都返回出去
        #results.pose_landmarks是骨骼数据，以后传给analysis.py算角度
        return frame, results.pose_landmarks


#测试代码
if __name__ == "__main__":
    from camera import Camera # 从同级目录导入 camera.py
    
    cam = Camera()
    estimator = PoseEstimator()

    while True:
        frame = cam.read()
        if frame is None:
            break

        # 调用我们刚刚写好的封装方法
        processed_frame, landmarks = estimator.process(frame)

        cv2.imshow("Pose Test", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()