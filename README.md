# MaixPy Development Skill

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MaixPy](https://img.shields.io/badge/MaixPy-v4-green.svg)](https://github.com/sipeed/MaixPy)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://claude.ai/code)

**[English](README.md)** | **[简体中文](README_CN.md)**

A comprehensive Claude Code skill for developing Python applications on Sipeed MaixCAM, MaixCAM-Pro, and MaixCAM2 edge AI devices using MaixPy v4.

## Features

- **AI Vision**: YOLO detection, segmentation, pose estimation, classification, face recognition, OCR
- **Image Processing**: Blob detection, edge detection, QR/barcode scanning, line tracking
- **Hardware Peripherals**: Camera, display, UART, I2C, SPI, GPIO, PWM, ADC
- **Network**: WiFi, HTTP streaming, MQTT, WebSocket, RTSP/RTMP
- **Audio**: Playback, recording, TTS, ASR
- **LLM/VLM**: Qwen, DeepSeek, InternVL (MaixCAM2 only)

## Supported Hardware

| Device | CPU | Memory | NPU | LLM Support |
|--------|-----|--------|-----|-------------|
| MaixCAM | 1GHz RISC-V | 256MB | 1Tops | No |
| MaixCAM-Pro | 1GHz RISC-V | 256MB | 1Tops | No |
| MaixCAM2 | 1.2GHz A53 x2 | 1GB/4GB | 3.2Tops | Yes |

## Installation

### Method 1: Direct Download

Download `maixpy-dev.skill` and place it in your Claude Code skills directory:

```bash
# Claude Code skills directory
~/.claude/skills/
```

### Method 2: Clone Repository

```bash
git clone https://github.com/StanleyChanH/MaixPy-skill.git
cd MaixPy-skill
```

Copy `maixpy-dev.skill` to your skills directory or use the source directly.

## Usage

Once installed, the skill automatically activates when you mention:

- MaixPy development
- MaixCAM / MaixCAM-Pro / MaixCAM2
- Sipeed AI development
- Embedded AI vision projects

### Example Prompts

```
"Help me create a YOLO object detection app for MaixCAM"
"How do I use UART on MaixCAM2?"
"Create a QR code scanner with MaixPy"
"Set up HTTP video streaming on MaixCAM"
```

## Quick Start Example

```python
from maix import camera, display, image, nn, app

# Initialize YOLO detector
detector = nn.YOLOv8(model="/root/models/yolov8n.mud", dual_buff=True)

# Initialize camera and display
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

## Skill Structure

```
maixpy-dev/
├── SKILL.md                      # Main skill definition
├── references/
│   ├── ai_models.md              # AI/NN models reference
│   ├── image_processing.md       # Image processing operations
│   ├── peripherals.md            # Hardware peripherals (UART, I2C, etc.)
│   ├── network.md                # Network & streaming
│   ├── audio.md                  # Audio playback/recording
│   ├── llm_vlm.md                # LLM/VLM integration (MaixCAM2)
│   ├── tracking.md               # Object tracking & counting
│   └── patterns.md               # Common patterns (UI, threading, i18n)
└── assets/
    ├── templates.py              # Application template
    └── app.yaml.template         # App configuration template
```

## Resources

- [MaixPy Official Documentation](https://wiki.sipeed.com/maixpy/)
- [MaixPy API Reference](https://wiki.sipeed.com/maixpy/api/index.html)
- [MaixPy GitHub](https://github.com/sipeed/MaixPy)
- [MaixHub (Online AI Training)](https://maixhub.com)
- [MaixVision IDE](https://wiki.sipeed.com/en/maixvision)

## Community

- QQ Group: 862340358
- Telegram: [t.me/maixpy](https://t.me/maixpy)
- GitHub Issues: [MaixPy Issues](https://github.com/sipeed/maixpy/issues)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Sipeed](https://www.sipeed.com/) - For creating MaixPy and the MaixCAM series
- [MaixPy Project](https://github.com/sipeed/MaixPy) - The underlying SDK
- [Anthropic](https://www.anthropic.com/) - For Claude and Claude Code

---

**Note**: This skill is an unofficial community project. For official MaixPy support, please refer to the [official documentation](https://wiki.sipeed.com/maixpy/).
