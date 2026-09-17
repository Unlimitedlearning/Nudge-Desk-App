# 体育体态纠正工具（教育）
## 项目简介
基于摄像头与MediaPipe姿态识别，针对青少年常见体态问题（如深蹲姿势、高低肩）提供实时反馈的辅助教育工具。

## 💻 开发环境
- **操作系统**：Windows 11
- **Python 版本**：3.11.9
- **开发工具**：VSCode + Git
- **虚拟环境**：`.venv`

## 📦 依赖安装
在终端执行以下命令，一键安装所有依赖：
`pip install -r requirements.txt`

## 📂 目录结构
Sports_Posture_Correction/
├── .venv/                 # 虚拟环境（不提交）
├── assets/                # 静态资源（图片、视频、模型文件）
├── data/                  # 数据存储（原始/处理后的姿态数据）
├── docs/                  # 项目文档
│   ├── contest/           # 挑战杯申报书、PPT等材料
│   ├── devlog/            # 每日开发日志（工作留痕）
│   ├── planning/          # 项目规划、架构图、任务分配
│   └── references/        # 参考文献、竞品分析
├── src/                   # 源码核心库
│   ├── input/             # 输入层（摄像头读取）
│   ├── vision/            # 骨骼提取层（MediaPipe）
│   ├── analysis/          # 动作分析层（角度计算）
│   ├── logic/             # 判定逻辑层（计分/反馈）
│   ├── ui/                # 表现层（界面渲染）
│   └── main.py            # 程序入口
├── tests/                 # 测试代码
├── requirements.txt       # Python 依赖清单
└── README.md              # 项目说明

## 当前状态
- [x] 立项，架构设计
- [ ] 跑通MediaPipe摄像头Demo
- [ ] 实现单一动作（深蹲）的角度计算
- [ ] 输出交互界面（UI）

## 开发日志
- 2026年9月16日：项目立项，环境搭建完毕。