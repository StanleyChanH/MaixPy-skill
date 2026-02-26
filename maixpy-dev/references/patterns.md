# Common Patterns Reference

## Table of Contents
- [App Structure](#app-structure)
- [Touch Button Pattern](#touch-button-pattern)
- [Back Button Pattern](#back-button-pattern)
- [Error Handling](#error-handling)
- [Device Detection](#device-detection)
- [Multi-threading](#multi-threading)
- [State Machine Pattern](#state-machine-pattern)
- [FPS Calculation](#fps-calculation)
- [i18n Internationalization](#i18n-internationalization)

## App Structure

### Standard Application Template

```python
from maix import camera, display, image, app, time, touchscreen

def is_in_button(x, y, btn_pos):
    return x > btn_pos[0] and x < btn_pos[0] + btn_pos[2] and y > btn_pos[1] and y < btn_pos[1] + btn_pos[3]

def get_back_btn_img(width):
    ret_width = int(width * 0.1)
    img_back = image.load("/maixapp/share/icon/ret.png")
    w, h = (ret_width, img_back.height() * ret_width // img_back.width())
    if w % 2 != 0:
        w += 1
    if h % 2 != 0:
        h += 1
    img_back = img_back.resize(w, h)
    return img_back

def main(disp):
    # Initialize components
    cam = camera.Camera(640, 480)
    ts = touchscreen.TouchScreen()

    # Back button
    img_back = get_back_btn_img(cam.width())
    back_rect = [0, 0, img_back.width(), img_back.height()]
    back_rect_disp = image.resize_map_pos(
        cam.width(), cam.height(),
        disp.width(), disp.height(),
        image.Fit.FIT_CONTAIN,
        back_rect[0], back_rect[1], back_rect[2], back_rect[3]
    )

    while not app.need_exit():
        img = cam.read()

        # Your processing here

        img.draw_image(0, 0, img_back)
        disp.show(img)

        x, y, pressed = ts.read()
        if is_in_button(x, y, back_rect_disp):
            app.set_exit_flag(True)

disp = display.Display()
try:
    main(disp)
except Exception:
    import traceback
    msg = traceback.format_exc()
    img = image.Image(disp.width(), disp.height(), bg=image.COLOR_BLACK)
    img.draw_string(0, 0, msg, image.COLOR_WHITE)
    disp.show(img)
    while not app.need_exit():
        time.sleep_ms(100)
```

## Touch Button Pattern

### Simple Button
```python
def is_in_button(x, y, btn_pos):
    """Check if touch coordinates are within button bounds"""
    return (x > btn_pos[0] and x < btn_pos[0] + btn_pos[2] and
            y > btn_pos[1] and y < btn_pos[1] + btn_pos[3])

# Button definition: [x, y, width, height]
btn_pos = [100, 100, 80, 40]

# In main loop
x, y, pressed = ts.read()
if pressed and is_in_button(x, y, btn_pos):
    print("Button pressed!")
```

### Button with Visual Feedback
```python
# Create button images
btn_normal = image.Image(80, 40, bg=image.Color.from_rgb(0x08, 0x7b, 0xa7))
btn_normal.draw_string(10, 10, "START", image.COLOR_WHITE, 2)

btn_pressed = image.Image(80, 40, bg=image.Color.from_rgb(0x06, 0x5a, 0x80))
btn_pressed.draw_string(10, 10, "START", image.COLOR_WHITE, 2)

btn_pos = [100, 100, 80, 40]

# In main loop
x, y, pressed = ts.read()
if is_in_button(x, y, btn_pos):
    img.draw_image(btn_pos[0], btn_pos[1], btn_pressed)
    if pressed:
        # Action on press
        pass
else:
    img.draw_image(btn_pos[0], btn_pos[1], btn_normal)
```

### Multiple Buttons with State
```python
pressed_flag = [False, False, False]  # Track button states

def on_touch(x, y, pressed):
    global pressed_flag
    if pressed:
        if is_in_button(x, y, btn1_pos):
            pressed_flag[0] = True
        elif is_in_button(x, y, btn2_pos):
            pressed_flag[1] = True
        elif is_in_button(x, y, btn3_pos):
            pressed_flag[2] = True
    else:
        # Check which button was released
        if pressed_flag[0]:
            pressed_flag[0] = False
            return "btn1"
        if pressed_flag[1]:
            pressed_flag[1] = False
            return "btn2"
        if pressed_flag[2]:
            pressed_flag[2] = False
            return "btn3"
    return None
```

## Back Button Pattern

```python
def get_back_btn_img(width):
    """Create resized back button image"""
    ret_width = int(width * 0.1)
    img_back = image.load("/maixapp/share/icon/ret.png")
    w, h = (ret_width, img_back.height() * ret_width // img_back.width())
    if w % 2 != 0:
        w += 1
    if h % 2 != 0:
        h += 1
    img_back = img_back.resize(w, h)
    return img_back

# Usage
img_back = get_back_btn_img(cam.width())
back_rect = [0, 0, img_back.width(), img_back.height()]

# Map coordinates from display to camera image
back_rect_disp = image.resize_map_pos(
    cam.width(), cam.height(),
    disp.width(), disp.height(),
    image.Fit.FIT_CONTAIN,
    back_rect[0], back_rect[1], back_rect[2], back_rect[3]
)

# In main loop
x, y, pressed = ts.read()
if is_in_button(x, y, back_rect_disp):
    app.set_exit_flag(True)
```

## Error Handling

### Try-Except with Display
```python
disp = display.Display()
try:
    main(disp)
except Exception:
    import traceback
    msg = traceback.format_exc()
    img = image.Image(disp.width(), disp.height(), bg=image.COLOR_BLACK)
    img.draw_string(0, 0, msg, image.COLOR_WHITE)
    disp.show(img)
    while not app.need_exit():
        time.sleep_ms(100)
```

### Error with Timeout
```python
try:
    # Risky operation
    result = risky_function()
except RuntimeError as e:
    print(f"Error: {e}")
    wait_time_s = 10
    while wait_time_s:
        eimg = image.Image(cam.width(), cam.height())
        eimg.draw_string(10, 10, f"Error: {e}. Exit in {wait_time_s}s.")
        disp.show(eimg)
        time.sleep(1)
        wait_time_s -= 1
    exit(-1)
```

## Device Detection

### Device ID
```python
from maix import sys

device_id = sys.device_id()  # "maixcam", "maixcam-pro", "maixcam2"
device_name = sys.device_name()  # "MaixCAM", "MaixCAM2"

if device_id == "maixcam2":
    # MaixCAM2 specific code
    model = "/root/models/yolo11s.mud"
    cam_w, cam_h = 640, 480
else:
    # MaixCAM / MaixCAM-Pro code
    model = "/root/models/yolov8n.mud"
    cam_w, cam_h = 320, 240
```

### Device-Specific Pinmap
```python
from maix import sys, pinmap

device_id = sys.device_id()
if device_id == "maixcam2":
    uart_tx = "A21"
    uart_rx = "A22"
    i2c_id = 6
else:
    uart_tx = "A16"
    uart_rx = "A17"
    i2c_id = 5

pinmap.set_pin_function(uart_tx, "UART_TX")
pinmap.set_pin_function(uart_rx, "UART_RX")
```

## Multi-threading

### Thread with Lock
```python
import threading

class App:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.result = None
        self.thread_exit = False

    def worker_thread(self, data):
        self.thread_lock.acquire()
        # Process data
        self.result = process(data)
        self.thread_exit = True
        self.thread_lock.release()

    def run_async(self, data):
        t = threading.Thread(target=self.worker_thread, args=[data], daemon=True)
        t.start()

    def check_result(self):
        with self.thread_lock:
            if self.thread_exit:
                return self.result
        return None
```

### VLM Thread Example
```python
import threading

def vlm_thread(vlm, img, msg):
    vlm.set_image(img, image.Fit.FIT_CONTAIN)
    resp = vlm.send(msg)
    print(resp.msg)

def run_vlm(img, msg):
    t = threading.Thread(target=vlm_thread, args=[vlm, img, msg], daemon=True)
    t.start()
```

## State Machine Pattern

```python
class AppStatus:
    IDLE = 0
    RUNNING = 1
    PROCESSING = 2
    ERROR = 3

class App:
    def __init__(self):
        self.status = AppStatus.IDLE

    def run(self):
        while not app.need_exit():
            if self.status == AppStatus.IDLE:
                self.handle_idle()
            elif self.status == AppStatus.RUNNING:
                self.handle_running()
            elif self.status == AppStatus.PROCESSING:
                self.handle_processing()
            elif self.status == AppStatus.ERROR:
                self.handle_error()

            time.sleep_ms(10)

    def handle_idle(self):
        # Wait for user input
        if some_condition:
            self.status = AppStatus.RUNNING

    def handle_running(self):
        # Main operation
        if done:
            self.status = AppStatus.PROCESSING
```

## FPS Calculation

### Using time.fps()
```python
from maix import camera, display, time, app

cam = camera.Camera(640, 480)
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    fps = time.fps()  # Auto-calculates from last call
    img.draw_string(10, 10, f"FPS: {fps:.1f}", image.COLOR_GREEN)
    disp.show(img)
```

### Manual FPS Calculation
```python
total_time = 0
total_frames = 0

while not app.need_exit():
    t_start = time.ticks_ms()

    img = cam.read()
    # Processing...
    disp.show(img)

    t_end = time.ticks_ms()
    frame_time = t_end - t_start
    total_time += frame_time
    total_frames += 1

    fps = total_frames * 1000 / total_time
    print(f"Frame time: {frame_time}ms, FPS: {fps:.2f}")
```

## i18n Internationalization

### Simple Dictionary Approach
```python
from maix import i18n

trans_dict = {
    "zh": {
        "title": "人脸识别",
        "start": "开始",
        "stop": "停止"
    },
    "en": {
        "title": "Face Recognition",
        "start": "Start",
        "stop": "Stop"
    }
}

trans = i18n.Trans(trans_dict)
tr = trans.tr

# Usage
language = "zh"
title = tr("title")  # Returns "人脸识别"
```

### Language Switch Button
```python
language = 'zh'
language_box = [disp.width() - 50, 0, 50, 30]

# In main loop
x, y, pressed = ts.read()
if is_in_button(x, y, language_box):
    if language == 'zh':
        language = 'en'
    else:
        language = 'zh'
    trans.set_language(language)

# Display language indicator
if language == 'zh':
    img.draw_string(language_box[0], language_box[1], "ZH", image.COLOR_WHITE, scale=2)
else:
    img.draw_string(language_box[0], language_box[1], "EN", image.COLOR_WHITE, scale=2)
```

### Load Custom Font
```python
# Load Chinese font
image.load_font("sourcehansans", "/maixapp/share/font/SourceHanSansCN-Regular.otf", size=20)
image.set_default_font("sourcehansans")

# Now can draw Chinese characters
img.draw_string(10, 10, "你好世界", image.COLOR_WHITE)
```
