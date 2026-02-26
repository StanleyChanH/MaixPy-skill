# Object Tracking Reference

## Table of Contents
- [ByteTracker](#bytetracker)
- [Tracking with YOLO](#tracking-with-yolo)
- [Counting Objects](#counting-objects)
- [Trajectory Visualization](#trajectory-visualization)

## ByteTracker

### Basic Setup
```python
from maix import nn, camera, display, image, tracker, app, time

# Initialize tracker
max_lost_buff_time = 120   # Frames to keep lost tracks
track_thresh = 0.4         # Tracking confidence threshold
high_thresh = 0.6          # Threshold to add new track
match_thresh = 0.8         # Matching threshold (IoU)
max_history_num = 10       # Max position history length

tracker0 = tracker.ByteTracker(
    max_lost_buff_time,
    track_thresh,
    high_thresh,
    match_thresh,
    max_history_num
)
```

### Convert YOLO Results to Tracker Objects
```python
def yolo_objs_to_tracker_objs(objs, valid_class_id=[]):
    """Convert YOLO detection results to tracker objects"""
    new = []
    for obj in objs:
        if len(valid_class_id) > 0 and obj.class_id not in valid_class_id:
            continue
        new.append(tracker.Object(
            obj.x, obj.y, obj.w, obj.h,
            obj.class_id, obj.score
        ))
    return new
```

## Tracking with YOLO

### Complete Example
```python
from maix import nn, camera, display, image, tracker, app, time, sys

# Model selection by device
if sys.device_name().lower() == "maixcam2":
    detector = nn.YOLO11(model="/root/models/yolo11s.mud", dual_buff=True)
else:
    detector = nn.YOLOv5(model="/root/models/yolov5s.mud", dual_buff=True)

cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
disp = display.Display()

# Tracker configuration
tracker0 = tracker.ByteTracker(120, 0.4, 0.6, 0.8, 10)
valid_class_id = [0]  # Only track person (class 0)

# Color palette for tracks
colors = [
    [255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0],
    [0, 255, 255], [255, 0, 255], [255, 128, 0], [128, 255, 0]
]

while not app.need_exit():
    img = cam.read()

    # Detect objects
    objs = detector.detect(img, conf_th=0.3, iou_th=0.45)

    # Convert to tracker format
    tracker_objs = yolo_objs_to_tracker_objs(objs, valid_class_id)

    # Update tracker
    tracks = tracker0.update(tracker_objs)

    # Draw tracks
    for track in tracks:
        if track.lost:
            continue

        color = colors[track.id % len(colors)]
        color = image.Color.from_rgb(color[0], color[1], color[2])

        obj = track.history[-1]
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color, thickness=2)
        img.draw_string(obj.x, obj.y, f"{track.id}", color, scale=1.5)

    disp.show(img)
```

## Counting Objects

### ROI-based Counting
```python
def obj_in_roi(obj, roi):
    """Check object position relative to ROI
    Returns: -1 (above), 0 (in), 1 (below), None (outside horizontally)
    """
    x = obj.x + obj.w // 2
    y = obj.y + obj.h // 2
    if x >= roi[0] and x <= roi[0] + roi[2]:
        if y < roi[1]:
            return -1
        if y > roi[1] + roi[3]:
            return 1
        return 0
    return None

def count_tracks(img, count_roi, tracks, count, counted_ids):
    """Count objects crossing ROI from top to bottom"""
    img.draw_rect(count_roi[0], count_roi[1], count_roi[2], count_roi[3],
                  image.COLOR_YELLOW, thickness=2)

    for track in tracks:
        if track.lost:
            continue

        obj = track.history[-1]
        ret = obj_in_roi(obj, count_roi)

        if ret is None:
            continue

        # Object below ROI and not yet counted
        if ret > 0 and track.id not in counted_ids:
            # Check if object was previously in ROI
            for o in track.history[::-1][1:]:
                if obj_in_roi(o, count_roi) == 0:
                    count += 1
                    counted_ids.append(track.id)
                    break

    img.draw_string(0, img.height() - 30, f"Count: {count}",
                    color=image.COLOR_RED, scale=2)

    # Prevent memory growth
    if len(counted_ids) > 500:
        counted_ids = counted_ids[300:]

    return count, counted_ids

# Usage
count_roi = [0, cam.height() - cam.height() // 2, cam.width(), cam.height() // 9]
up_down_count = 0
counted_ids = []

while not app.need_exit():
    # ... detection and tracking ...

    up_down_count, counted_ids = count_tracks(
        img, count_roi, tracks, up_down_count, counted_ids
    )
```

## Trajectory Visualization

### Draw Track History
```python
def draw_trajectory(img, track, color, thickness=2):
    """Draw trajectory line from track history"""
    for i in range(1, len(track.history)):
        o = track.history[i]
        last_o = track.history[i - 1]
        img.draw_line(
            last_o.x + last_o.w // 2, last_o.y + last_o.h // 2,
            o.x + o.w // 2, o.y + o.h // 2,
            color=color, thickness=thickness
        )

# Usage
for track in tracks:
    if track.lost:
        continue
    color = colors[track.id % len(colors)]
    color = image.Color.from_rgb(color[0], color[1], color[2])
    draw_trajectory(img, track, color)
```

### Show Track Statistics
```python
def show_track_stats(img, tracks, start_y):
    """Display tracking statistics"""
    valid = sum(1 for t in tracks if not t.lost)
    total = len(tracks)

    img.draw_string(2, start_y, f'Valid: {valid}, Total: {total}',
                    image.COLOR_RED, scale=1.5)
```

## Complete Tracking & Counting Example

```python
from maix import nn, camera, display, image, tracker, app, time, sys

# Initialize
if sys.device_name().lower() == "maixcam2":
    detector = nn.YOLO11(model="/root/models/yolo11s.mud", dual_buff=True)
else:
    detector = nn.YOLOv5(model="/root/models/yolov5s.mud", dual_buff=True)

cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
disp = display.Display()
tracker0 = tracker.ByteTracker(120, 0.4, 0.6, 0.8, 10)

# Colors
colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0]]

# Counter setup
count_roi = [0, cam.height() // 2, cam.width(), cam.height() // 8]
count = 0
counted_ids = []

while not app.need_exit():
    img = cam.read()

    # Detect and track
    objs = detector.detect(img, conf_th=0.3, iou_th=0.45)
    tracker_objs = [tracker.Object(o.x, o.y, o.w, o.h, o.class_id, o.score)
                    for o in objs if o.class_id == 0]  # Person only
    tracks = tracker0.update(tracker_objs)

    # Draw and count
    img.draw_rect(count_roi[0], count_roi[1], count_roi[2], count_roi[3],
                  image.COLOR_YELLOW, thickness=2)

    for track in tracks:
        if track.lost:
            continue

        color = image.Color.from_rgb(*colors[track.id % len(colors)])
        obj = track.history[-1]

        # Draw box and ID
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color, thickness=2)
        img.draw_string(obj.x, obj.y, f"{track.id}", color, scale=1.5)

        # Draw trajectory
        for i in range(1, len(track.history)):
            o = track.history[i]
            last = track.history[i - 1]
            img.draw_line(last.x + last.w//2, last.y + last.h//2,
                         o.x + o.w//2, o.y + o.h//2, color, thickness=1)

        # Count crossing
        y = obj.y + obj.h // 2
        if y > count_roi[1] + count_roi[3] and track.id not in counted_ids:
            for o in track.history[::-1][1:]:
                oy = o.y + o.h // 2
                if count_roi[1] <= oy <= count_roi[1] + count_roi[3]:
                    count += 1
                    counted_ids.append(track.id)
                    break

    img.draw_string(10, 10, f"Count: {count}", image.COLOR_RED, scale=2)
    disp.show(img)
```
