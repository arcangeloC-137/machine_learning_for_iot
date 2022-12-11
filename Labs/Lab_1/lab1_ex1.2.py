import numpy as np
import pandas as pd
import tensorflow as tf
import sounddevice as sd
import sys
import os

from time import time
from scipy.io.wavfile import write

def callback(inputData, frames, callback_time, status):
    # function called for each audio block
    timestamp = time()
    write(f'{timestamp}.wav', 48000, inputData)
    filesize_in_bytes = os.path.getsize(f'{timestamp}.wav')
    filesize_in_kb = filesize_in_bytes / 1024
    print(f'Size: {filesize_in_kb:.2f}KB')

with sd.InputStream(device=1, channels=1, dtype='int32', samplerate=48000, blocksize=48000, callback=callback):
    while True:
        key = input()
        if key in ('q', 'Q'):
            print('Stop recording.')
            break