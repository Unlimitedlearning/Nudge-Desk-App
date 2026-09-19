# Nudge-Desk-App (轻推)

## 📖 项目简介
Nudge-Desk-App (轻推)是一款面向学生群体的**桌面学习体态提醒工具**。基于普通摄像头与 MediaPipe 姿态识别技术，在用户日常学习（写作业、看网课）时，实时监测头前倾、圆肩、驼背等不良体态，并通过温和的视觉与声音反馈进行提醒，帮助用户养成健康的坐姿习惯。

**核心定位**：零硬件成本、离线可用、无感提醒、正向激励。

详细竞品分析见 docs/business/Competitive_Analysis.md

## 💻 开发环境
- **操作系统**：Windows 11
- **Python 版本**：3.11.9
- **开发工具**：VSCode + Git
- **虚拟环境**：`.venv`

## 📦 快速开始
在终端（已激活虚拟环境）执行以下命令，一键安装所有依赖：
```bash
pip install -r requirements.txt
```

## 📁 目录结构

```text
Nudge-Desk-App/
├── .venv/                  # 虚拟环境（不提交）
├── assets/                 # 静态资源（图片、视频、模型文件）
├── data/                   # 数据存储（原始/处理后的姿态数据）
├── docs/                   # 项目文档
│   ├── business/           # 商业计划、应用场景与市场调研
│   ├── devlog/             # 每日开发日志（工作留痕）
│   ├── planning/           # 项目规划、架构图、任务分配
│   └── references/         # 参考文献、竞品分析
├── src/                    # 源码核心库
│   ├── app.py              # 程序入口（负责串联所有模块）
│   ├── camera.py           # 输入层（摄像头读取）
│   ├── pose.py             # 视觉层（MediaPipe骨骼提取）
│   ├── analysis.py         # 分析层（体态夹角计算）
│   └── ui.py               # 表现层（界面渲染、画面反馈）
├── tests/                  # 测试代码
├── requirements.txt        # Python 依赖清单
└── README.md               # 项目说明（本文件）
```

## 📝 文档与日志
开发过程记录、每日工作留痕及架构设计，详见 docs/ 目录