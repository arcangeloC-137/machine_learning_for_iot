import psutil
import time
import uuid

from datetime import datetime, timedelta
from uuid import getnode as get_mac
import pandas as pd

prev_time = time.time()

def get_mac():
    mac = hex(uuid.getnode())
    return mac

while True:

    dt = time.time() - prev_time
    if dt > 2:
        battery = psutil.sensors_battery()
        date = datetime.now()

        print("%s - %s:battery = %s%%" % (date, get_mac(), battery.percent))
        print("%s - %s:power = %s" % (date, get_mac(), str(int(battery.power_plugged))))
        prev_time = time.time()    
