# src/ui.py
"""
表现层：桌面悬浮窗 UI 模块。
职责：创建无边框/置顶/半透明的窗口，接收体态状态并更新颜色与文字显示。
依赖：tkinter
"""

import tkinter as tk
import os
import sys
import pygame
# 把 utils 所在目录加入路径，防止打包后找不到
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import resource_path

class DesktopWidget:
    def __init__(self):
        # 1. 创建主窗口
        self.root = tk.Tk()
        self.root.title("Nudge-Desk-App (轻推)")
        
        # 2. 窗口大小和位置
        window_width = 140
        window_height = 120
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width - 20
        y = screen_height - window_height - 80
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 3. 无边框、置顶、半透明
        self.root.overrideredirect(True)            # 删掉系统自带的标题栏、关闭按钮
        self.root.attributes("-topmost", True)      # 永远悬浮在所有窗口（包括浏览器）之上
        self.root.attributes("-alpha", 0.85)        # 0.85表示85%的不透明度，露出背景

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
        self.status_label.bind("<Button-3>", self.show_menu)  # 绑定鼠标右键点击事件

        # 初始化音频
        try:
            # ⚡ 使用 resource_path 获取打包后的正确路径
            sound_path = resource_path("assets/audio/tone.wav")
            
            print(f"🔊 正在加载音频: {sound_path}")
            pygame.mixer.init()
            self.alert_sound = pygame.mixer.Sound(sound_path)
            self.alert_sound.set_volume(0.3)
            print("✅ 音频加载成功！")
        except Exception as e:
            print(f"❌ 音频初始化失败，具体报错: {e}")
            self.alert_sound = None
            
        self.last_status = None  # 用于记录上一次的状态，防止重复响铃

    def start_move(self, event):
        # 鼠标左键按下时：记录鼠标当前在窗口内的相对位置
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_move(self, event):
        # 鼠标左键按住并移动时：根据鼠标位移计算窗口的新位置
        deltax = event.x - self._drag_data["x"]
        deltay = event.y - self._drag_data["y"]
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def update_status(self, status="未检测到人", angle=0, neck_fatigue=0,is_tilted=False,is_too_close=False):
        """供外部调用：更新悬浮窗状态"""

        if is_too_close:
            status = "TOO_CLOSE"
        elif is_tilted:
            status = "TILTED"

        # 声音提醒：只有当从未达到 ALERT 突然变成 ALERT 时，才响一声，避免每30ms就响一次
        if status == "ALERT" and self.last_status != "ALERT":
            try:
                if self.alert_sound:
                    self.alert_sound.play()  # 播放自定义音效
            except Exception:
                pass  # 防止在非 Windows 系统上报错
        self.last_status = status  # 更新记录

        if status == "GOOD":
            self.status_label.config(
                text=f"体态端正\n{angle}°\n颈疲劳: {neck_fatigue}", 
                bg="#2ecc71", fg="black"
            )
        elif status == "WARNING":
            self.status_label.config(
                text=f"警告\n{angle}°\n颈疲劳: {neck_fatigue}", 
                bg="#f1c40f", fg="black"
            )
        elif status == "ALERT":
            self.status_label.config(
                text=f"严重疲劳\n{angle}°\n颈疲劳: {neck_fatigue}", 
                bg="#e74c3c", fg="white"
            )

        elif status == "TOO_CLOSE":
            self.status_label.config(text="脸太近了！\n请后退", bg="#e67e22", fg="white")
        elif status == "TILTED":
            self.status_label.config(text="高低肩！\n请坐正", bg="#9b59b6", fg="white")

        else:
            self.status_label.config(text=status, bg="#555555", fg="white")

    def start(self):
        self.root.mainloop()