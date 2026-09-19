# src/ui.py
import tkinter as tk

class DesktopWidget:
    def __init__(self):
        # 1. 创建主窗口
        self.root = tk.Tk()
        self.root.title("体态守望者")
        
        # 2. 窗口大小和位置
        window_width = 140
        window_height = 120
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width - 20
        y = screen_height - window_height - 80
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 3. 无边框、置顶、半透明
        self.root.overrideredirect(True)# 删掉系统自带的标题栏、关闭按钮
        self.root.attributes("-topmost", True)# 永远悬浮在所有窗口（包括浏览器）之上
        self.root.attributes("-alpha", 0.85)# 0.85表示85%的不透明度，露出背景

        # 4. 状态标签
        self.status_label = tk.Label(
            self.root, 
            text="初始化...", 
            font=("Microsoft YaHei", 12, "bold"),
            bg="#333333", 
            fg="white",
            justify="center"
        )
        self.status_label.pack(expand=True, fill="both")

        # 5. 鼠标拖动
        self.status_label.bind("<Button-1>", self.start_move)
        self.status_label.bind("<B1-Motion>", self.do_move)
        self._drag_data = {"x": 0, "y": 0}

        # 6. 鼠标右键菜单（用来关闭）
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="退出", command=self.root.destroy)
        self.status_label.bind("<Button-3>", self.show_menu)# 绑定鼠标右键点击事件

    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
    # 鼠标左键按下时：记录鼠标当前在窗口内的相对位置

    def do_move(self, event):
        deltax = event.x - self._drag_data["x"]
        deltay = event.y - self._drag_data["y"]
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    # 鼠标左键按住并移动时：根据鼠标位移计算窗口的新位置

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def update_status(self, status, angle=0, fatigue=0):
        """供外部调用：更新悬浮窗状态"""
        if status == "GOOD":
            self.status_label.config(
                text=f"体态端正\n{angle}°\n疲劳值: {fatigue}", 
                bg="#2ecc71", fg="black"
            )
        elif status == "WARNING":
            self.status_label.config(
                text=f"警告\n{angle}°\n疲劳值: {fatigue}", 
                bg="#f1c40f", fg="black"
            )
        elif status == "ALERT":
            self.status_label.config(
                text=f"严重疲劳\n{angle}°\n疲劳值: {fatigue}", 
                bg="#e74c3c", fg="white"
            )
        else:
            self.status_label.config(text="未检测到人", bg="#555555", fg="white")

    def start(self):
        self.root.mainloop()




# 测试代码（独立运行 ui.py 时，模拟变色）
if __name__ == "__main__":
    import time
    import threading
    
    widget = DesktopWidget()
    
    def fake_loop():
        import random
        while True:
            # 模拟三种状态随机切换
            status = random.choice(["GOOD", "WARNING", "ALERT"])
            angle = random.randint(150, 180)
            fatigue = random.randint(0, 15)
            # 调用 UI 更新
            widget.update_status(status, angle, fatigue)
            time.sleep(2)

    # 用多线程启动模拟循环，不卡住主界面
    threading.Thread(target=fake_loop, daemon=True).start()
    
    # 启动 UI 主循环
    widget.start()