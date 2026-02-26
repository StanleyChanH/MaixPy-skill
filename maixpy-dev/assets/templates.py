"""
MaixPy Application Template
Copy and modify for your project

This template includes:
- Camera and display initialization
- Back button with touch handling
- FPS display
- Error handling
- Device detection
"""

from maix import camera, display, image, app, time, touchscreen, sys

# ============ Configuration ============
# Device-specific settings
device_id = sys.device_id()
if device_id == "maixcam2":
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
else:
    CAMERA_WIDTH = 320
    CAMERA_HEIGHT = 240

# ============ Utility Functions ============
def is_in_button(x, y, btn_pos):
    """Check if touch coordinates are within button bounds"""
    return (x > btn_pos[0] and x < btn_pos[0] + btn_pos[2] and
            y > btn_pos[1] and y < btn_pos[1] + btn_pos[3])

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

# ============ Main Application ============
def main(disp):
    # Initialize hardware
    cam = camera.Camera(CAMERA_WIDTH, CAMERA_HEIGHT)
    ts = touchscreen.TouchScreen()

    print(f"Camera: {cam.width()}x{cam.height()}")
    print(f"Display: {disp.width()}x{disp.height()}")

    # Setup back button
    img_back = get_back_btn_img(cam.width())
    back_rect = [0, 0, img_back.width(), img_back.height()]

    # Map touch coordinates from display to camera
    back_rect_disp = image.resize_map_pos(
        cam.width(), cam.height(),
        disp.width(), disp.height(),
        image.Fit.FIT_CONTAIN,
        back_rect[0], back_rect[1], back_rect[2], back_rect[3]
    )

    # Main loop
    while not app.need_exit():
        # Read camera
        img = cam.read()

        # === YOUR PROCESSING HERE ===

        # Example: Draw FPS
        fps = time.fps()
        img.draw_string(10, 10, f"FPS: {fps:.1f}", image.COLOR_GREEN)

        # === END PROCESSING ===

        # Draw back button and display
        img.draw_image(0, 0, img_back)
        disp.show(img)

        # Handle touch
        x, y, pressed = ts.read()
        if is_in_button(x, y, back_rect_disp):
            app.set_exit_flag(True)

# ============ Entry Point ============
if __name__ == "__main__":
    disp = display.Display()
    try:
        main(disp)
    except Exception:
        import traceback
        msg = traceback.format_exc()
        print(msg)
        img = image.Image(disp.width(), disp.height(), bg=image.COLOR_BLACK)
        img.draw_string(0, 0, msg, image.COLOR_WHITE)
        disp.show(img)
        while not app.need_exit():
            time.sleep_ms(100)
