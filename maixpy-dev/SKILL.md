---
name: maixpy-dev
description: |
  MaixPy v4 development assistant for Sipeed MaixCAM, MaixCAM-Pro, and MaixCAM2 edge AI devices.
  Use this skill when developing Python applications for MaixPy platform including:
  (1) AI vision applications (YOLO detection, classification, face recognition, pose estimation)
  (2) Image processing (find blobs, edges, QR codes, barcodes, lines)
  (3) Hardware peripherals (camera, display, UART, I2C, SPI, GPIO, PWM, ADC, USB HID)
  (4) Network applications (WiFi, HTTP streaming, MQTT, WebSocket, RTSP/RTMP)
  (5) Audio applications (playback, recording, TTS, ASR)
  (6) LLM/VLM integration (Qwen, DeepSeek, InternVL on MaixCAM2)
  (7) Object tracking and counting (ByteTracker)
  (8) Video encoding/decoding, OpenCV integration
  Trigger when user mentions MaixPy, MaixCAM, MaixCAM2, MaixCAM-Pro, Sipeed AI development, or embedded AI vision projects.
---

# MaixPy Development Skill

MaixPy v4 is a Python SDK for edge AI development on Sipeed hardware. This skill provides patterns, examples, and best practices.

## Hardware Comparison

| Feature | MaixCAM/MaixCAM-Pro | MaixCAM2 |
|---------|---------------------|----------|
| CPU | 1GHz RISC-V (Linux) | 1.2GHz A53 x2 (Ubuntu) |
| Memory | 256MB DDR3 | 1GB/4GB LPDDR4 |
| NPU | 1Tops@INT8 | 3.2Tops@INT8 |
| LLM Support | No | Yes (Qwen/DeepSeek) |

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
        img.draw_string(obj.x, obj.y, f'{detector.labels[obj.class_id]}: {obj.score:.2f}')
    disp.show(img)
```

## Reference Documentation

| Topic | File | Content |
|-------|------|---------|
| AI Models | [ai_models.md](references/ai_models.md) | YOLO, classifier, face, OCR, pose, segmentation |
| Image Processing | [image_processing.md](references/image_processing.md) | Draw, blobs, edges, QR/barcodes, transforms |
| Peripherals | [peripherals.md](references/peripherals.md) | UART, I2C, SPI, GPIO, PWM, ADC |
| Network | [network.md](references/network.md) | WiFi, HTTP, MQTT, WebSocket |
| Audio | [audio.md](references/audio.md) | Playback, recording, TTS, ASR |
| LLM/VLM | [llm_vlm.md](references/llm_vlm.md) | Qwen, DeepSeek, InternVL (MaixCAM2) |
| Tracking | [tracking.md](references/tracking.md) | ByteTracker, counting, trajectories |
| Patterns | [patterns.md](references/patterns.md) | Touch UI, threading, state machine, i18n |
| Advanced | [advanced.md](references/advanced.md) | OpenCV, video, USB HID, RTSP, protocols |

## Device Detection

```python
from maix import sys

device_id = sys.device_id()  # "maixcam", "maixcam2"

if device_id == "maixcam2":
    model = "/root/models/yolo11s.mud"  # Larger model
else:
    model = "/root/models/yolov8n.mud"  # Nano model
```

## Model Paths

Pre-installed models in `/root/models/`:
- Detection: `yolov8n.mud`, `yolo11n.mud`, `yolo11s.mud`
- Segmentation: `yolo11n_seg.mud`, `yolov8n_seg.mud`
- Pose: `yolo11n_pose.mud`, `yolov8n_pose.mud`
- Face: `yolov8n_face.mud`, `retinaface.mud`
- Classifier: `mobilenetv2.mud`
- OCR: `pp_ocr.mud`
- Hand: `hand_landmarks.mud`

## App Development

```
my_app/
├── app.yaml      # Config (see assets/app.yaml.template)
├── main.py       # Entry point
└── icon.png      # App icon (128x128)
```

## Resources

- Docs: https://wiki.sipeed.com/maixpy/
- API: https://wiki.sipeed.com/maixpy/api/index.html
- GitHub: https://github.com/sipeed/MaixPy
- Examples: https://github.com/sipeed/MaixPy/tree/main/examples
- Projects: https://github.com/sipeed/MaixPy/tree/main/projects
- MaixHub: https://maixhub.com
- Community: QQ群 862340358, t.me/maixpy
