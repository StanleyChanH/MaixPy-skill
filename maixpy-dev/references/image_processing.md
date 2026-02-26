# Image Processing Reference

## Table of Contents
- [Image Creation & Loading](#image-creation--loading)
- [Drawing Operations](#drawing-operations)
- [Color Operations](#color-operations)
- [Find Blobs (Color Tracking)](#find-blobs)
- [Find Lines & Edges](#find-lines--edges)
- [Find Shapes](#find-shapes)
- [Find QR Codes & Barcodes](#find-qr-codes--barcodes)
- [Image Transformations](#image-transformations)
- [Pixel Operations](#pixel-operations)

## Image Creation & Loading

### Create Image
```python
from maix import image

# Create blank image
img = image.Image(640, 480, image.Format.FMT_RGB888)

# Create with background color
img = image.Image(640, 480, image.Format.FMT_RGB888, bg=image.COLOR_BLACK)
img = image.Image(640, 480, image.Format.FMT_RGB888, bg=image.Color.from_rgb(255, 0, 0))
```

### Load Image
```python
# Load from file
img = image.load("/path/to/image.jpg")
img = image.load("/path/to/image.png")

# Load from bytes
with open("image.jpg", "rb") as f:
    img = image.load(f.read())
```

### Save Image
```python
img.save("/path/to/output.jpg")
img.save("/path/to/output.png")
```

### Image Format
```python
from maix import image

print(f"Width: {img.width()}")
print(f"Height: {img.height()}")
print(f"Format: {img.format()}")  # FMT_RGB888, FMT_RGBA8888, FMT_GRAYSCALE, etc.
```

## Drawing Operations

### Draw Rectangle
```python
# Outline rectangle
img.draw_rect(10, 10, 100, 50, color=image.COLOR_RED)

# Filled rectangle (thickness=-1)
img.draw_rect(10, 10, 100, 50, color=image.COLOR_BLUE, thickness=-1)

# Custom thickness
img.draw_rect(10, 10, 100, 50, color=image.COLOR_GREEN, thickness=3)
```

### Draw Circle
```python
img.draw_circle(100, 100, 30, color=image.COLOR_RED)
img.draw_circle(100, 100, 30, color=image.COLOR_RED, thickness=-1)  # Filled
```

### Draw Line
```python
img.draw_line(0, 0, 100, 100, color=image.COLOR_RED)
img.draw_line(0, 0, 100, 100, color=image.COLOR_RED, thickness=2)
```

### Draw String
```python
# Basic text
img.draw_string(10, 10, "Hello MaixPy", color=image.COLOR_RED)

# With scale
img.draw_string(10, 10, "Large Text", color=image.COLOR_WHITE, scale=2)

# Get text size
size = image.string_size("Hello", scale=2)
print(f"Text size: {size.width()}x{size.height()}")
```

### Draw Image on Image
```python
overlay = image.load("logo.png")
img.draw_image(10, 10, overlay)
```

## Color Operations

### Predefined Colors
```python
image.COLOR_RED
image.COLOR_GREEN
image.COLOR_BLUE
image.COLOR_WHITE
image.COLOR_BLACK
image.COLOR_YELLOW
image.COLOR_CYAN
image.COLOR_MAGENTA
```

### Create Custom Color
```python
# From RGB
color = image.Color.from_rgb(255, 128, 0)

# From RGBA
color = image.Color.from_rgba(255, 128, 0, 200)  # With alpha

# From grayscale
color = image.Color.from_grayscale(128)
```

## Find Blobs

Color blob detection for tracking colored objects:
```python
from maix import camera, display, image

cam = camera.Camera(320, 240)
disp = display.Display()

# Color thresholds: [L_min, L_max, A_min, A_max, B_min, B_max]
# LAB color space
thresholds_red = [[0, 80, 40, 80, 10, 80]]
thresholds_green = [[0, 80, -120, -10, 0, 30]]
thresholds_blue = [[0, 80, 30, 100, -120, -60]]

while True:
    img = cam.read()

    blobs = img.find_blobs(
        thresholds_green,
        area_threshold=1000,      # Minimum blob area
        pixels_threshold=1000     # Minimum pixel count
    )

    for b in blobs:
        # Draw bounding box
        corners = b.corners()
        for i in range(4):
            img.draw_line(
                corners[i][0], corners[i][1],
                corners[(i + 1) % 4][0], corners[(i + 1) % 4][1],
                image.COLOR_RED
            )

        # Blob properties
        print(f"Center: ({b.cx()}, {b.cy()}), Area: {b.area()}")

    disp.show(img)
```

## Find Lines & Edges

### Find Lines
```python
lines = img.find_lines(
    threshold=1000,       # Line detection threshold
    theta_margin=25,      # Theta merge margin
    rho_margin=25         # Rho merge margin
)

for line in lines:
    img.draw_line(line.x1(), line.y1(), line.x2(), line.y2(), image.COLOR_RED)
    print(f"Line: theta={line.theta()}, rho={line.rho()}")
```

### Find Line Segments
```python
segments = img.find_line_segments(
    merge_distance=10,    # Merge segments within this distance
    max_degree_diff=15    # Max angle difference for merging
)

for seg in segments:
    img.draw_line(seg.x1(), seg.y1(), seg.x2(), seg.y2(), image.COLOR_GREEN)
```

### Find Edges (Canny)
```python
# Apply edge detection
edges = img.find_edges(image.EdgeDetector.EDGE_CANNY, threshold=(50, 150))
disp.show(edges)
```

## Find Shapes

### Find Circles (Hough Circle)
```python
circles = img.find_circles(
    threshold=2000,
    x_margin=10,
    y_margin=10,
    r_margin=10
)

for c in circles:
    img.draw_circle(c.x(), c.y(), c.r(), color=image.COLOR_RED)
    print(f"Circle at ({c.x()}, {c.y()}), radius={c.r()}")
```

### Find Rectangles
```python
rects = img.find_rects(threshold=10000)

for r in rects:
    corners = r.corners()
    for i in range(4):
        img.draw_line(
            corners[i][0], corners[i][1],
            corners[(i + 1) % 4][0], corners[(i + 1) % 4][1],
            image.COLOR_RED
        )
```

## Find QR Codes & Barcodes

### QR Codes
```python
# Basic QR code detection
qrcodes = img.find_qrcodes()

for qr in qrcodes:
    img.draw_rect(qr.x(), qr.y(), qr.w(), qr.h(), color=image.COLOR_RED)
    print(f"QR Content: {qr.payload()}")

# Faster QR detection (with ROI)
roi = (100, 100, 200, 200)  # x, y, w, h
qrcodes = img.find_qrcodes(roi=roi)
```

### Barcodes
```python
barcodes = img.find_barcodes()

for b in barcodes:
    img.draw_rect(b.x(), b.y(), b.w(), b.h(), color=image.COLOR_GREEN)
    print(f"Barcode: {b.payload()}, Type: {b.type()}")
```

### AprilTags
```python
apriltags = img.find_apriltags()

for tag in apriltags:
    img.draw_rect(tag.x(), tag.y(), tag.w(), tag.h(), color=image.COLOR_BLUE)
    print(f"Tag ID: {tag.id()}, Rotation: {tag.rotation()}")
```

## Image Transformations

### Resize
```python
# Simple resize
resized = img.resize(320, 240)

# With fit mode
resized = img.resize(640, 480, image.Fit.FIT_CONTAIN)  # Keep aspect ratio
resized = img.resize(640, 480, image.Fit.FIT_COVER)    # Cover, may crop
resized = img.resize(640, 480, image.Fit.FIT_FILL)     # Stretch to fill
```

### Rotate
```python
rotated = img.rotate(90)   # Rotate 90 degrees
rotated = img.rotate(180)
rotated = img.rotate(270)
```

### Flip
```python
flipped = img.flip(image.Flip.FLIP_HORIZONTAL)
flipped = img.flip(image.Flip.FLIP_VERTICAL)
```

### Crop
```python
cropped = img.crop(100, 100, 200, 150)  # x, y, w, h
```

## Pixel Operations

### Get/Set Pixel
```python
# Get pixel color
color = img.get_pixel(100, 100)
print(f"R: {color.r()}, G: {color.g()}, B: {color.b()}")

# Set pixel
img.set_pixel(100, 100, image.COLOR_RED)
```

### Convert Format
```python
# Convert to grayscale
gray = img.to_format(image.Format.FMT_GRAYSCALE)

# Convert to RGB888
rgb = img.to_format(image.Format.FMT_RGB888)
```

### Binary Threshold
```python
# Convert to binary image
binary = img.binary([(100, 200)])  # Threshold range
```

### Histogram
```python
# Get histogram
hist = img.get_histogram()
print(f"Mean: {hist.mean()}, StdDev: {hist.stdev()}")
```

### Statistics
```python
stats = img.get_statistics()
print(f"Min: {stats.min()}, Max: {stats.max()}")
print(f"Mean: {stats.mean()}, Median: {stats.median()}")
```

## Image Arithmetic

```python
# Blend two images
result = img1.blend(img2, alpha=0.5)

# Add/Subtract
result = img1.add(img2)
result = img1.sub(img2)

# Bitwise operations
result = img1.bitwise_and(img2)
result = img1.bitwise_or(img2)
result = img1.bitwise_xor(img2)
result = img1.bitwise_not()
```

## Morphological Operations

```python
# Erosion
eroded = img.erode(kernel_size=3)

# Dilation
dilated = img.dilate(kernel_size=3)

# Morphology (opening/closing)
result = img.morph(kernel_size=3, iterations=1)
```

## Filter Operations

```python
# Gaussian blur
blurred = img.gaussian(kernel_size=5)

# Median filter
filtered = img.median(kernel_size=3)

# Bilateral filter
filtered = img.bilateral(d=5, sigma_color=75, sigma_space=75)
```
