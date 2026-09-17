# src/camera.py
import cv2
class Camera:
    def __init__(self,camera_index=0):    #_init_是构造函数，创建Camera()时自动运行
        self.cap = cv2.VideoCapture(camera_index)
        #self.cap是一个属性，代表这台相机对象的底层控制器
        if not self.cap.isOpened():
            print("X 无法打开摄像头，请检查是否被其他程序占用")

    def read(self):
        ret,frame = self.cap.read()
        if ret:
            return frame
        else:return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

# 这里的测试代码是为了让你能单独运行 camera.py 验证它自己
# 只有当你直接运行这个文件时（__name__ == "__main__"）才会执行，被 app.py 导入时不会执行
if __name__ == "__main__":
    cam = Camera()
    while True:
        frame = cam.read()
        if frame is None: break
        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cam.release()