# Advanced Features Reference

## Table of Contents
- [OpenCV Integration](#opencv-integration)
- [Video Encoding/Decoding](#video-encodingdecoding)
- [USB HID Devices](#usb-hid-devices)
- [Communication Protocol](#communication-protocol)
- [Self-Learning Classifier](#self-learning-classifier)
- [AI ISP Configuration](#ai-isp-configuration)
- [RTSP Streaming](#rtsp-streaming)

## OpenCV Integration

### Convert Between Maix Image and OpenCV

```python
from maix import image, display, app, time, camera
import cv2

# Initialize camera with BGR format for OpenCV
cam = camera.Camera(320, 240, image.Format.FMT_BGR888)
disp = display.Display()

while not app.need_exit():
    img = cam.read()

    # Convert maix.image.Image to numpy.ndarray
    img_np = image.image2cv(img, ensure_bgr=False, copy=False)

    # Use OpenCV functions
    edged = cv2.Canny(img_np, 180, 60)
    blurred = cv2.GaussianBlur(img_np, (5, 5), 0)

    # Convert back to maix.image.Image
    img_show = image.cv2image(edged, bgr=True, copy=False)

    disp.show(img_show)
```

### Common OpenCV Operations

```python
import cv2
from maix import image, camera, display, app

cam = camera.Camera(320, 240, image.Format.FMT_BGR888)
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    np_img = image.image2cv(img, ensure_bgr=True, copy=False)

    # Edge detection
    edges = cv2.Canny(np_img, 100, 200)

    # Color conversion
    gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(np_img, cv2.COLOR_BGR2HSV)

    # Thresholding
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(np_img, contours, -1, (0, 255, 0), 2)

    # Show result
    result = image.cv2image(np_img, bgr=True, copy=False)
    disp.show(result)
```

## Video Encoding/Decoding

### Video Encoding (Recording)

```python
from maix import video, time, image, camera, display, app

width = 640
height = 480

cam = camera.Camera(width, height, image.Format.FMT_YVU420SP)
disp = display.Display()

# Create encoder
encoder = video.Encoder('/root/output.mp4', width, height)

record_ms = 5000  # Record for 5 seconds
start_ms = time.ticks_ms()

while not app.need_exit():
    img = cam.read()

    # Encode frame
    encoder.encode(img)

    # Show preview
    disp.show(img)

    if time.ticks_ms() - start_ms > record_ms:
        break

# Encoder is automatically closed when deleted
print("Recording complete!")
```

### Video Decoding (Playback)

```python
from maix import video, display, app, time

disp = display.Display()

# Open video file
decoder = video.Decoder('/root/output.mp4')

print(f'Resolution: {decoder.width()}x{decoder.height()}')
print(f'Bitrate: {decoder.bitrate()}')
print(f'FPS: {decoder.fps()}')

# Seek to beginning
decoder.seek(0)

last_us = time.ticks_us()

while not app.need_exit():
    # Decode frame
    ctx = decoder.decode_video()
    if not ctx:
        # End of video, restart
        decoder.seek(0)
        continue

    img = ctx.image()

    # Wait for frame duration
    while time.ticks_us() - last_us < ctx.duration_us():
        time.sleep_ms(1)
    last_us = time.ticks_us()

    disp.show(img)
```

## USB HID Devices

### USB Keyboard

```python
from maix import hid, time

# Initialize HID keyboard
keyboard = None
try:
    keyboard = hid.Hid(hid.DeviceType.DEVICE_KEYBOARD)
except Exception as e:
    print('HID device not enabled')
    print('Enable in Settings -> USB Settings -> HID Keyboard')
    exit(0)

def press_key(kb, key):
    """Press and release a single key"""
    kb.write([0, 0, key, 0, 0, 0, 0, 0])
    time.sleep_ms(50)
    kb.write([0, 0, 0, 0, 0, 0, 0, 0])  # Release

def press_combo(kb, modifier, key):
    """Press key with modifier (Shift, Ctrl, Alt)"""
    kb.write([modifier, 0, key, 0, 0, 0, 0, 0])
    time.sleep_ms(50)
    kb.write([0, 0, 0, 0, 0, 0, 0, 0])

# Modifier values:
# 0x1: left-ctrl, 0x2: left-shift, 0x4: left-alt, 0x8: left-windows
# 0x10: right-ctrl, 0x20: right-shift, 0x40: right-alt, 0x80: right-windows

# Key codes (HID Usage Tables): https://www.usb.org
# a=4, b=5, c=6... z=29
# 1=30, 2=31... 0=39
# Enter=40, Space=44

press_key(keyboard, 21)              # Press 'r'
press_combo(keyboard, 0x2, 25)       # Press Shift+V (paste)
```

### USB Mouse

```python
from maix import hid, time

mouse = hid.Hid(hid.DeviceType.DEVICE_MOUSE)

def move_mouse(m, dx, dy):
    """Move mouse relative"""
    m.write([0, dx, dy, 0])

def click_mouse(m, button=1):
    """Click mouse button (1=left, 2=right, 4=middle)"""
    m.write([button, 0, 0, 0])
    time.sleep_ms(50)
    m.write([0, 0, 0, 0])

# Move and click
move_mouse(mouse, 100, 50)
click_mouse(mouse, 1)  # Left click
```

## Communication Protocol

### Built-in Protocol Handler

```python
from maix import comm, protocol, app, err

# Custom command IDs
APP_CMD_ECHO = 0x01
APP_CMD_GET_DATA = 0x02

# Initialize communication (UART or TCP based on system config)
p = comm.CommProtocol(buff_size=1024)

while not app.need_exit():
    msg = p.get_msg()
    if msg and msg.is_req:
        if msg.cmd == APP_CMD_ECHO:
            # Echo back
            resp_msg = f"echo from app"
            p.resp_ok(msg.cmd, resp_msg.encode())

        elif msg.cmd == APP_CMD_GET_DATA:
            # Return some data
            data = b'\x01\x02\x03\x04'
            p.resp_ok(msg.cmd, data)

        elif msg.cmd == protocol.CMD.CMD_SET_REPORT:
            # Auto-upload not supported
            p.resp_err(msg.cmd, err.Err.ERR_NOT_IMPL,
                      b"auto upload not supported")
```

### YOLO Detection Protocol

```python
from maix import comm, protocol, nn, camera, app

# See: examples/protocol/comm_protocol_yolov5.py
p = comm.CommProtocol(buff_size=2048)
detector = nn.YOLOv8(model="/root/models/yolov8n.mud")
cam = camera.Camera(detector.input_width(), detector.input_height())

while not app.need_exit():
    msg = p.get_msg()
    if msg and msg.is_req:
        if msg.cmd == protocol.CMD.CMD_DETECT:
            img = cam.read()
            objs = detector.detect(img)
            # Send detection results
            p.resp_ok(msg.cmd, encode_objects(objs))
```

## Self-Learning Classifier

### Train Custom Classes Without Retraining

```python
from maix import nn, image, display, app, camera

# Initialize self-learning classifier
classifier = nn.SelfLearnClassifier(
    model="/root/models/mobilenet_v2_no_top.mud",
    dual_buff=True
)

cam = camera.Camera(classifier.input_width(),
                    classifier.input_height(),
                    classifier.input_format())
disp = display.Display()

# Add reference images for each class
class_images = []
class_names = ["object_a", "object_b", "object_c"]

# Capture or load reference images
for i, name in enumerate(class_names):
    img = cam.read()
    disp.show(img)
    classifier.add_class(img)
    class_images.append(img)

# Optionally add more samples
sample_images = []
for i in range(5):
    img = cam.read()
    classifier.add_sample(img)
    sample_images.append(img)

# Learn from samples
print("Learning...")
classifier.learn()
print("Learning complete!")

# Now classify new images
while not app.need_exit():
    img = cam.read()
    result = classifier.classify(img)

    # result is list of (class_id, distance) sorted by distance
    best_match = result[0]
    class_id = best_match[0]
    distance = best_match[1]

    # Lower distance = better match
    if distance < 0.5:  # Threshold
        label = class_names[class_id]
    else:
        label = "unknown"

    img.draw_string(10, 10, f"{label}: {distance:.2f}")
    disp.show(img)
```

## AI ISP Configuration

### Enable/Disable AI ISP (MaixCAM2)

```python
from maix import app, err

def get_ai_isp_on():
    """Check if AI ISP is enabled"""
    ai_isp_on = app.get_sys_config_kv("npu", "ai_isp", "0")
    return ai_isp_on != "0"

def set_ai_isp(on: bool):
    """Enable or disable AI ISP"""
    print("Setting AI ISP:", "ON" if on else "OFF")
    value = "1" if on else "0"
    e = app.set_sys_config_kv("npu", "ai_isp", value)
    err.check_raise(e, f"Set AI ISP failed")
    print("Reboot required for changes to take effect")

# Usage
print("AI ISP:", "ON" if get_ai_isp_on() else "OFF")
set_ai_isp(False)  # Disable for VLM usage
```

**Note**: AI ISP must be disabled when using VLM on MaixCAM2.

## RTSP Streaming

### RTSP Server with Audio

```python
from maix import rtsp, camera, image, audio, app, time

AUDIO_ENABLE = True

# Initialize camera with YVU420SP format for hardware encoding
cam = camera.Camera(640, 480, image.Format.FMT_YVU420SP)

# Create RTSP server
server = rtsp.Rtsp()
server.bind_camera(cam)

# Optionally bind audio
if AUDIO_ENABLE:
    audio_recorder = audio.Recorder()
    server.bind_audio_recorder(audio_recorder)

# Start server
server.start()

print(f"RTSP URL: {server.get_url()}")
print("Open in VLC or ffplay")

while not app.need_exit():
    time.sleep(1)
```

### RTSP Client (Receive Stream)

```python
from maix import rtsp, display, app, time

# Connect to RTSP server
client = rtsp.RtspClient("rtsp://192.168.1.100:8554/stream")
disp = display.Display()

while not app.need_exit():
    img = client.read()
    if img:
        disp.show(img)
```

## Low-Level NN Forward

### Direct Model Forward Pass

```python
from maix import nn, tensor, time, sys
import numpy as np

model_path = "/root/models/yolov8n.mud"
model = nn.NN(model_path, dual_buff=False)

# Print input/output info
print("Inputs:")
for layer in model.inputs_info():
    print(f"  {layer.name}: {layer.shape}, dtype: {layer.dtype}")

print("Outputs:")
for layer in model.outputs_info():
    print(f"  {layer.name}: {layer.shape}, dtype: {layer.dtype}")

# Create input tensors
input_tensors = tensor.Tensors()
for layer in model.inputs_info():
    dtype = np.float32 if sys.device_id() in ["maixcam", "maixcam_pro"] else np.uint8
    data = np.zeros(layer.shape, dtype=dtype)
    t = tensor.tensor_from_numpy_float32(data, copy=False)
    input_tensors.add_tensor(layer.name, t, False, False)

# Forward pass
outputs = model.forward(input_tensors, copy_result=False)

# Get output as numpy
for k in outputs.keys():
    out = tensor.tensor_to_numpy_float32(outputs[k], copy=False)
    print(f"Output [{k}], shape: {out.shape}")
```
