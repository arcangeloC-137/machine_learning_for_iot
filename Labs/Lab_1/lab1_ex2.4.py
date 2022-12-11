import psutil
import time
import uuid
import redis
import redis_connection

from datetime import datetime
from uuid import getnode as get_mac

def get_mac_addr():
    mac = hex(uuid.getnode())
    return mac

# Redis Connection Configuration
connection = redis_connection.get_connection()
redis_client = redis.Redis(host=connection['REDIS_HOST'], port=connection['REDIS_PORT'], username=connection['REDIS_USERNAME'], password=connection['REDIS_PASSWORD'])
is_connected = redis_client.ping()
print('Reddis Connected: ', is_connected)

# Create a time series named 'mac:battery'
try:

    k1 = get_mac_addr() + ':battery_v01'
    k2 = get_mac_addr() + ':power_v01'

    print(f'Keys: {k1} and {k2}')

    redis_client.ts().create(k1)
    redis_client.ts().create(k2)
    print('Time series created!')

except redis.ResponseError:
    print('An Error Occured!')
    pass

# We create ten records
prev_time = time.time()
records = 0

while(records < 10):

    dt = time.time() - prev_time
    if dt > 2:
        battery = psutil.sensors_battery()
        date = datetime.now()

        timestamp_ms = int(time.time() * 1000) # Redis requires the ts in ms

        # create battery timeseries
        redis_client.ts().add(f'{get_mac_addr()}:battery_v01', timestamp_ms, battery.percent)
        last_timestamp_ms, last_value = redis_client.ts().get(f'{get_mac_addr()}:battery_v01')
        print(last_timestamp_ms, last_value)

        # create power timeseries
        redis_client.ts().add(f'{get_mac_addr()}:power_v01', timestamp_ms, int(battery.power_plugged))
        last_timestamp_ms, last_value = redis_client.ts().get(f'{get_mac_addr()}:power_v01')
        print(last_timestamp_ms, last_value)

        records = records + 1
        prev_time = time.time()

