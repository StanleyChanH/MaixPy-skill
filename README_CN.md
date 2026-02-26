# MaixPy 开发技能

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MaixPy](https://img.shields.io/badge/MaixPy-v4-green.svg)](https://github.com/sipeed/MaixPy)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://claude.ai/code)

**[English](README.md)** | **[简体中文](README_CN.md)**

一个全面的 Claude Code 技能包，用于在 Sipeed MaixCAM、MaixCAM-Pro 和 MaixCAM2 边缘 AI 设备上使用 MaixPy v4 开发 Python 应用程序。

## 功能特性

- **AI 视觉**：YOLO 目标检测、图像分割、姿态估计、图像分类、人脸识别、OCR 文字识别
- **图像处理**：色块检测、边缘检测、二维码/条码扫描、线条追踪
- **硬件外设**：摄像头、显示屏、UART 串口、I2C、SPI、GPIO、PWM、ADC
- **网络功能**：WiFi、HTTP 视频流、MQTT、WebSocket、RTSP/RTMP 推流
- **音频功能**：音频播放、录制、TTS 语音合成、ASR 语音识别
- **大语言模型**：Qwen、DeepSeek、InternVL 视觉语言模型（仅限 MaixCAM2）

## 支持的硬件

| 设备 | CPU | 内存 | NPU | 大模型支持 |
|------|-----|------|-----|------------|
| MaixCAM | 1GHz RISC-V | 256MB | 1Tops | 否 |
| MaixCAM-Pro | 1GHz RISC-V | 256MB | 1Tops | 否 |
| MaixCAM2 | 1.2GHz A53 x2 | 1GB/4GB | 3.2Tops | 是 |

## 安装方法

### 方法一：直接下载

下载 `maixpy-dev.skill` 文件，放置到 Claude Code 的技能目录：

```bash
# Claude Code 技能目录
~/.claude/skills/
```

### 方法二：克隆仓库

```bash
git clone https://github.com/StanleyChanH/MaixPy-skill.git
cd MaixPy-skill
```

将 `maixpy-dev.skill` 复制到技能目录，或直接使用源码。

## 使用方法

安装完成后，当你提到以下内容时，技能会自动激活：

- MaixPy 开发
- MaixCAM / MaixCAM-Pro / MaixCAM2
- Sipeed AI 开发
- 嵌入式 AI 视觉项目

### 示例提示词

```
"帮我在 MaixCAM 上创建一个 YOLO 目标检测应用"
"如何在 MaixCAM2 上使用 UART 串口？"
"用 MaixPy 创建一个二维码扫描器"
"在 MaixCAM 上设置 HTTP 视频流"
```

## 快速入门示例

```python
from maix import camera, display, image, nn, app

# 初始化 YOLO 检测器
detector = nn.YOLOv8(model="/root/models/yolov8n.mud", dual_buff=True)

# 初始化摄像头和显示屏
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
    for obj in objs:
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
        img.draw_string(obj.x, obj.y, f'{detector.labels[obj.class_id]}: {obj.score:.2f}')
    disp.show(img)
```

## 技能目录结构

```
maixpy-dev/
├── SKILL.md                      # 主技能定义文件
├── references/
│   ├── ai_models.md              # AI/NN 模型参考
│   ├── image_processing.md       # 图像处理操作
│   ├── peripherals.md            # 硬件外设（UART、I2C 等）
│   ├── network.md                # 网络与流媒体
│   ├── audio.md                  # 音频播放/录制
│   └── llm_vlm.md                # LLM/VLM 集成（MaixCAM2）
└── assets/
    ├── templates.py              # 应用程序模板
    └── app.yaml.template         # 应用配置模板
```

## 资源链接

- [MaixPy 官方文档](https://wiki.sipeed.com/maixpy/)
- [MaixPy API 参考](https://wiki.sipeed.com/maixpy/api/index.html)
- [MaixPy GitHub](https://github.com/sipeed/MaixPy)
- [MaixHub 在线 AI 训练平台](https://maixhub.com)
- [MaixVision IDE](https://wiki.sipeed.com/zh/maixvision)

## 社区

- QQ 群：862340358
- Telegram：[t.me/maixpy](https://t.me/maixpy)
- GitHub Issues：[MaixPy Issues](https://github.com/sipeed/maixpy/issues)

## 参与贡献

欢迎参与贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 开源许可

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

## 致谢

- [Sipeed](https://www.sipeed.com/) - 创建了 MaixPy 和 MaixCAM 系列
- [MaixPy Project](https://github.com/sipeed/MaixPy) - 底层 SDK
- [Anthropic](https://www.anthropic.com/) - Claude 和 Claude Code

---

**注意**：本技能是非官方社区项目。如需官方 MaixPy 支持，请参考[官方文档](https://wiki.sipeed.com/maixpy/)。
