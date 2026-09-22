@echo off
echo ========================================
echo  Nudge-Desk-App 一键打包脚本
echo ========================================

REM 1. 激活虚拟环境
call .venv\Scripts\activate

REM 2. 执行 Nuitka 打包（含 assets 和 mediapipe 数据）
python -m nuitka --standalone --enable-plugin=tk-inter ^
  --include-package=mediapipe --include-package=cv2 ^
  --include-package-data=mediapipe ^
  --include-data-dir=assets=assets ^
  --windows-console-mode=disable src/app.py

REM 3. 补全 MediaPipe 模型文件（Nuitka 偶尔漏拷）
xcopy /E /Y /I ".venv\Lib\site-packages\mediapipe\modules" "app.dist\mediapipe\modules\"

echo.
echo ========================================
echo  打包完成！
echo  请将整个 app.dist 文件夹压缩后发送。
echo ========================================
pause