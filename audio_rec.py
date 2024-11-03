import sounddevice as sd
import soundfile as sf
from logger_setup import operation_logger
import os

log_dir = "/Users/mannatvirk/.hiddenfolder"

def record_audio(filename, duration, samplerate=44100, channels=1):
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()  
        sf.write(filename, recording, samplerate)
        operation_logger.info(f"Audio recording saved to {filename}")
    except Exception as e:
        operation_logger.error(f"Error during audio recording: {e}")
