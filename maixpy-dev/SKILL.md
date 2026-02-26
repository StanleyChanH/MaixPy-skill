---
name: maixpy-dev
description: |
  MaixPy v4 development assistant for Sipeed MaixCAM, MaixCAM-Pro, and MaixCAM2 edge AI devices.
  Use this skill when developing Python applications for MaixPy platform including:
  (1) AI vision applications (YOLO detection, classification, face recognition, pose estimation)
  (2) Image processing (find blobs, edges, QR codes, barcodes, lines)
  (3) Hardware peripherals (camera, display, UART, I2C, SPI, GPIO, PWM, ADC)
  (4) Network applications (WiFi, HTTP streaming, MQTT, WebSocket)
  (5) Audio applications (playback, recording, TTS, ASR)
  (6) LLM/VLM integration (Qwen, DeepSeek on MaixCAM2)
  (7) Object tracking and counting applications
  (8) Touch screen UI and multi-threaded applications
  Trigger when user mentions MaixPy, MaixCAM, MaixCAM2, MaixCAM-Pro, Sipeed AI development, or embedded AI vision projects.
---

# MaixPy Development Skill

MaixPy v4 is a Python SDK for edge AI development on Sipeed hardware (MaixCAM/MaixCAM-Pro/MaixCAM2). This skill provides patterns, examples, and best practices for developing applications.

## Hardware Comparison

| Feature | MaixCAM/MaixCAM-Pro | MaixCAM2 |
|---------|---------------------|----------|
| CPU | 1GHz RISC-V (Linux) | 1.2GHz A53 x2 (Ubuntu) |
| Memory | 256MB DDR3 | 1GB/4GB LPDDR4 |
| NPU | 1Tops@INT8 | 3.2Tops@INT8 |
| Camera | 5MP | 8MP with AI ISP |
| LLM Support | No | Yes (Qwen/DeepSeek 0.5B-1.5B) |

## Quick Start Pattern

```python
from maix import camera, display, image, nn, app

# Initialize model
detector = nn.YOLOv8(model="/root/models/yolov8n.mud", dual_buff=True)

# Initialize camera with model input size
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

## Core Modules

### Camera & Display

```python
from maix import camera, display, app

cam = camera.Camera(640, 480)  # width, height
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    disp.show(img)
```

### Image Processing

See [references/image_processing.md](references/image_processing.md) for complete image operations.

### AI/NN Models

See [references/ai_models.md](references/ai_models.md) for YOLO, classifier, face detection patterns.

### Object Tracking

See [references/tracking.md](references/tracking.md) for ByteTracker, counting, trajectory patterns.

### Peripherals (UART/I2C/SPI/GPIO)

See [references/peripherals.md](references/peripherals.md) for hardware interface patterns.

### Network & Streaming

See [references/network.md](references/network.md) for WiFi, HTTP, MQTT patterns.

### Audio

See [references/audio.md](references/audio.md) for playback and recording.

### LLM/VLM (MaixCAM2 Only)

See [references/llm_vlm.md](references/llm_vlm.md) for Qwen and VLM usage.

### Object Tracking

See [references/tracking.md](references/tracking.md) for ByteTracker, counting, trajectory patterns.

### Advanced Features

See [references/advanced.md](references/advanced.md) for:
- OpenCV integration
- Video encoding/decoding
- USB HID (keyboard/mouse)
- Communication protocol
- Self-learning classifier
- AI ISP configuration
- RTSP streaming
- Low-level NN forward

### Common Patterns

See [references/patterns.md](references/patterns.md) for:
- App structure template
- Touch button handling
- Back button pattern
- Error handling
- Multi-threading
- State machine pattern
- FPS calculation
- i18n internationalization

## Device ID Detection

```python
from maix import sys

device_id = sys.device_id()  # "maixcam", "maixcam2", etc.
device_name = sys.device_name()  # "MaixCAM", "MaixCAM2"

if device_id == "maixcam2":
    # MaixCAM2 specific code
    model = "/root/models/yolo11s.mud"
else:
    # MaixCAM/MaixCAM-Pro code
    model = "/root/models/yolov8n.mud"
```

## Model Paths

Pre-installed models are in `/root/models/`:
- YOLOv8: `yolov8n.mud`
- YOLO11: `yolo11n.mud`, `yolo11n_seg.mud`, `yolo11n_pose.mud`
- Classifier: `mobilenetv2.mud`
- Face: `yolov8n_face.mud`, `yolo11s_face.mud`, `retinaface.mud`
- OCR: `pp_ocr.mud`
- Hand: `hand_landmarks.mud`
- Whisper: `whisper-base/whisper-base.mud`

## App Development

### App Structure
```
my_app/
├── app.yaml          # App configuration
├── main.py           # Entry point
├── icon.png          # App icon (128x128)
└── assets/           # Additional resources
```

### app.yaml Template
```yaml
id: my_app
name: My Application
name[zh]: 我的应用
version: 1.0.0
author: Your Name
icon: icon.png
desc: App description
files:
  - app.yaml
  - main.py
  - icon.png
```

See [assets/app.yaml.template](assets/app.yaml.template) for complete configuration options.

## Development Workflow

1. Write code in MaixVision IDE or any editor
2. Connect device via USB (appears as network device)
3. Upload and run via MaixVision or `scp` + `ssh`
4. For production, create app package with `app.yaml`

## Key Resources

- Official Docs: https://wiki.sipeed.com/maixpy/
- API Reference: https://wiki.sipeed.com/maixpy/api/index.html
- GitHub: https://github.com/sipeed/MaixPy
- Example Projects: https://github.com/sipeed/MaixPy/tree/main/projects
- MaixHub (online training): https://maixhub.com
- Community: QQ群 862340358, t.me/maixpy
