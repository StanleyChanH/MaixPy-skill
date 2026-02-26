"""
MaixPy Application Template
Copy and modify for your project
"""

from maix import camera, display, image, app, time

# ============ Configuration ============
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# ============ Initialize Hardware ============
cam = camera.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
disp = display.Display()

print(f"Camera: {cam.width()}x{cam.height()}")
print(f"Display: {disp.width()}x{disp.height()}")

# ============ Main Loop ============
while not app.need_exit():
    t_start = time.ticks_ms()

    # Read camera
    img = cam.read()

    # === YOUR PROCESSING HERE ===

    # Example: Draw FPS
    fps = time.fps()
    img.draw_string(10, 10, f"FPS: {fps:.1f}", image.COLOR_GREEN)

    # === END PROCESSING ===

    # Display
    disp.show(img)

print("Application exited")
