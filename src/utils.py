# src/utils.py
import sys
import os

def resource_path(relative_path):
    """获取打包后或本地运行时的资源绝对路径"""
    # 1. PyInstaller 打包：使用 _MEIPASS 临时目录
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    # 2. Nuitka 或直接运行：基于当前可执行文件/脚本定位
    else:
        if getattr(sys, 'frozen', False): # Nuitka 打包后
            base_path = os.path.dirname(sys.executable)
        else:                             # 本地源码运行
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # 如果本地运行在 src/ 下，向上回退一级指向项目根目录
            if os.path.basename(base_path) == "src":
                base_path = os.path.dirname(base_path)
    
    return os.path.join(base_path, relative_path)