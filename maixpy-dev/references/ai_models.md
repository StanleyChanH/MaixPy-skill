# AI/NN Models Reference

## Table of Contents
- [YOLO Object Detection](#yolo-object-detection)
- [YOLO Segmentation](#yolo-segmentation)
- [YOLO Pose Estimation](#yolo-pose-estimation)
- [YOLO OBB (Oriented Bounding Box)](#yolo-obb)
- [Image Classification](#image-classification)
- [Face Detection & Recognition](#face-detection--recognition)
- [Self-Learning Classifier](#self-learning-classifier)
- [OCR (Optical Character Recognition)](#ocr)
- [Depth Estimation](#depth-estimation)

## YOLO Object Detection

### YOLOv8
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
        msg = f'{detector.labels[obj.class_id]}: {obj.score:.2f}'
        img.draw_string(obj.x, obj.y, msg, color=image.COLOR_RED)
    disp.show(img)
```

### YOLO11
```python
detector = nn.YOLO11(model="/root/models/yolo11n.mud", dual_buff=True)
# Same usage as YOLOv8
```

### YOLO-World (Open Vocabulary)
```python
detector = nn.YOLO11(model="/root/models/yolo11n_world.mud")
detector.set_labels(["person", "car", "dog"])  # Custom labels at runtime

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5)
    # Process results...
```

## YOLO Segmentation

```python
detector = nn.YOLO11(model="/root/models/yolo11n_seg.mud")
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45, keypoint_th=0.5)
    for obj in objs:
        # Draw segmentation mask
        detector.draw_seg_mask(img, obj.x, obj.y, obj.seg_mask, threshold=127)
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
    disp.show(img)
```

## YOLO Pose Estimation

```python
detector = nn.YOLO11(model="/root/models/yolo11n_pose.mud")

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
    for obj in objs:
        # Draw keypoints and skeleton
        detector.draw_pose(img, obj.points, threshold=0.5)
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color=image.COLOR_RED)
    disp.show(img)
```

## YOLO OBB

For rotated object detection:
```python
detector = nn.YOLO11(model="/root/models/yolo11n_obb.mud")

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th=0.5, iou_th=0.45)
    for obj in objs:
        # OBB has rotation angle
        detector.draw_obb(img, obj.x, obj.y, obj.w, obj.h, obj.angle)
```

## Image Classification

```python
from maix import camera, display, image, nn, app

classifier = nn.Classifier(model="/root/models/mobilenetv2.mud", dual_buff=True)
cam = camera.Camera(classifier.input_width(), classifier.input_height(), classifier.input_format())
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    res = classifier.classify(img)
    max_idx, max_prob = res[0]  # Top result
    msg = f"{max_prob:5.2f}: {classifier.labels[max_idx]}"
    img.draw_string(10, 10, msg, image.COLOR_RED)
    img = img.resize(disp.width(), disp.height(), image.Fit.FIT_CONTAIN)
    disp.show(img)
```

## Face Detection & Recognition

### Face Detection
```python
from maix import camera, display, image, nn, app

detector = nn.Facedetector(model="/root/models/face_det.mud", dual_buff=True)
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())

while not app.need_exit():
    img = cam.read()
    faces = detector.detect(img, conf_th=0.5)
    for face in faces:
        img.draw_rect(face.x, face.y, face.w, face.h, color=image.COLOR_RED)
        # face.points contains facial landmarks
    disp.show(img)
```

### Face Recognition
```python
# Full face recognition with feature extraction
# See: https://github.com/sipeed/MaixPy/tree/main/projects/app_face_recognizer
recognizer = nn.FaceRecognizer(model="/root/models/face_recog.mud")
```

## Self-Learning Classifier

Train custom classes without retraining:
```python
from maix import camera, display, image, nn, app

classifier = nn.SelfLearnClassifier(model="/root/models/self_learn_classifier.mud")

# Capture and learn new classes
classifier.learn_class(img1, 0)  # Learn class 0 from img1
classifier.learn_class(img2, 1)  # Learn class 1 from img2

# Classify
while not app.need_exit():
    img = cam.read()
    res = classifier.classify(img)
    if res.class_id >= 0:
        print(f"Class: {res.class_id}, Score: {res.score}")
```

## OCR

```python
from maix import camera, display, image, nn, app

ocr = nn.PPOCR(model="/root/models/pp_ocr.mud")
cam = camera.Camera(640, 480)

while not app.need_exit():
    img = cam.read()
    results = ocr.detect(img)
    for r in results:
        img.draw_rect(r.x, r.y, r.w, r.h, color=image.COLOR_RED)
        img.draw_string(r.x, r.y - 20, r.text, color=image.COLOR_RED)
    disp.show(img)
```

## Depth Estimation

```python
from maix import camera, display, image, nn, app

depth = nn.DepthAnythingV2(model="/root/models/depth_anything_v2.mud")
cam = camera.Camera(depth.input_width(), depth.input_height(), depth.input_format())

while not app.need_exit():
    img = cam.read()
    depth_map = depth.detect(img)
    # depth_map is a grayscale depth image
    disp.show(depth_map)
```

## Dual Buffer Mode

`dual_buff=True` enables pipelining for better FPS:
- Camera captures next frame while NPU processes current frame
- Recommended for real-time applications

```python
# With dual buffer (recommended)
detector = nn.YOLOv8(model="/root/models/yolov8n.mud", dual_buff=True)

# Without dual buffer (for single-frame processing)
detector = nn.YOLOv8(model="/root/models/yolov8n.mud", dual_buff=False)
```

## Model Input Properties

```python
detector = nn.YOLOv8(model="/root/models/yolov8n.mud")
print(f"Input: {detector.input_width()}x{detector.input_height()}, format: {detector.input_format()}")
print(f"Labels: {detector.labels}")
```

## Performance Tips

1. Use `dual_buff=True` for streaming applications
2. Match camera resolution to model input size
3. Use appropriate confidence threshold (0.3-0.5 typical)
4. For MaixCAM2, use larger models (yolo11s/l) for better accuracy
5. For MaixCAM, use nano models (yolo11n/yolov8n) for real-time
