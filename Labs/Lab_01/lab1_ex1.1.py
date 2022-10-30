import numpy as np
import pandas as pd
import tensorflow as tf
import sounddevice as sd
import sys

with sd.InputStream(device=1, channels=1, dtype='int32', samplerate=48000):
    while True:
        key = input()
        if key in ('q', 'Q'):
            print('Stop recording.')
            break