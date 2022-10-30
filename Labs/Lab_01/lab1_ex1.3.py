import numpy as np
import pandas as pd
import tensorflow as tf
import sounddevice as sd
import sys
import os
import parser
import logging

from time import time
from scipy.io.wavfile import write


args = parser.parse_arguments()
logging.info(f"Arguments: {args}")

def callback(inputData, frames, callback_time, status):
    # function called for each audio block
    global recording
    path = r"/Users/arcangelofrigiola/repo/ml4iot/lab01/recordings"
    callback_time = args.duration

    if recording is True:
        timestamp = time()
        timestampPath = os.path.join(path, f'{timestamp}.wav')
        write(timestampPath, int(callback_time / 10 * args.samplingRate), inputData)
        filesize_in_bytes = os.path.getsize(timestampPath)
        filesize_in_kb = filesize_in_bytes / 1024
        print(f'Size: {filesize_in_kb:.2f}KB')

recording = False
while True:

    inputStream = sd.InputStream(device=1, channels=args.channelsNum, 
                                    dtype=args.resolution, samplerate=args.samplingRate, 
                                    blocksize=48000, callback=callback)

    key = input()
    if key in ('P', 'p'):
        if (recording):
            print('Stop recording.')
            recording = not recording
            inputStream.stop()
        else:
            print('Start recording.')
            recording = not recording
            inputStream.start()

    if key in ('q', 'Q'):
        print('Quit recording.')
        break