# MaixPy Development Skill

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![MaixPy](https://img.shields.io/badge/MaixPy-v4-green.svg)](https://github.com/sipeed/MaixPy)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-orange.svg)](https://claude.ai/code)

**[English](README.md)** | **[简体中文](README_CN.md)**

A comprehensive Claude Code skill for developing Python applications on Sipeed MaixCAM, MaixCAM-Pro, and MaixCAM2 edge AI devices using MaixPy v4.

## Features

- **AI Vision**: YOLO detection, segmentation, pose estimation, classification, face recognition, OCR
- **Image Processing**: Blob detection, edge detection, QR/barcode scanning, line tracking
- **Object Tracking**: ByteTracker, counting, trajectory visualization
- **Peripherals**: Camera, display, UART, I2C, SPI, GPIO, PWM, ADC, USB HID
- **Network**: WiFi, HTTP streaming, MQTT, WebSocket, RTSP/RTMP
- **Audio**: Playback, recording, TTS, ASR
- **LLM/VLM**: Qwen, DeepSeek, InternVL (MaixCAM2 only)
- **Advanced**: OpenCV integration, video encoding/decoding, self-learning classifier

## Installation

### Method 1: Direct Download

Download `maixpy-dev.skill` and place it in your Claude Code skills directory:

```bash
~/.claude/skills/
```

### Method 2: Clone Repository

```bash
git clone https://github.com/StanleyChanH/MaixPy-skill.git
```

## Quick Start

```python
from maix import camera, display, image, nn, app

detector = nn.YOLOv8(model="/root/models/yolov8n.mud", dual_buff=True)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
    for obj in objs:
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
    disp.show(img)
```

## Documentation Structure

| File | Content |
|------|---------|
| [ai_models.md](maixpy-dev/references/ai_models.md) | YOLO, classifier, face detection, OCR, pose, segmentation |
| [image_processing.md](maixpy-dev/references/image_processing.md) | Drawing, blobs, edges, QR/barcodes, transforms |
| [peripherals.md](maixpy-dev/references/peripherals.md) | UART, I2C, SPI, GPIO, PWM, ADC |
| [network.md](maixpy-dev/references/network.md) | WiFi, HTTP, MQTT, WebSocket |
| [audio.md](maixpy-dev/references/audio.md) | Playback, recording, TTS, ASR |
| [llm_vlm.md](maixpy-dev/references/llm_vlm.md) | Qwen, DeepSeek, InternVL (MaixCAM2) |
| [tracking.md](maixpy-dev/references/tracking.md) | ByteTracker, counting, trajectories |
| [patterns.md](maixpy-dev/references/patterns.md) | Touch UI, threading, state machine, i18n |
| [advanced.md](maixpy-dev/references/advanced.md) | OpenCV, video, USB HID, RTSP, protocols |

## Supported Hardware

| Device | CPU | Memory | NPU | LLM |
|--------|-----|--------|-----|-----|
| MaixCAM | 1GHz RISC-V | 256MB | 1Tops | No |
| MaixCAM-Pro | 1GHz RISC-V | 256MB | 1Tops | No |
| MaixCAM2 | 1.2GHz A53 x2 | 1GB/4GB | 3.2Tops | Yes |

## Resources

- [MaixPy Documentation](https://wiki.sipeed.com/maixpy/)
- [API Reference](https://wiki.sipeed.com/maixpy/api/index.html)
- [MaixPy GitHub](https://github.com/sipeed/MaixPy)
- [MaixHub (Online Training)](https://maixhub.com)
- [MaixVision IDE](https://wiki.sipeed.com/en/maixvision)

## Community

- QQ Group: 862340358
- Telegram: [t.me/maixpy](https://t.me/maixpy)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE).

## Acknowledgments

- [Sipeed](https://www.sipeed.com/) - For MaixPy and MaixCAM series
- [MaixPy Project](https://github.com/sipeed/MaixPy) - The underlying SDK

---

*Note: This is an unofficial community project. For official support, see [MaixPy docs](https://wiki.sipeed.com/maixpy/).*
