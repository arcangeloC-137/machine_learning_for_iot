import argparse
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--resolution', type=str, choices=["int16", "int32"])
    parser.add_argument('--samplingRate', type=int, help="Sampling rate in Hz")
    parser.add_argument('--channelsNum', type=int)
    parser.add_argument('--duration', type=int)

    args = parser.parse_args()
    return args