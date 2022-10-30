import redis
import redis_connection

REDIS_HOST = '*****'
REDIS_PORT = ****
REDIS_USERNAME = 'default'
REDIS_PASSWORD = '******'

connection = redis_connection.get_connection()
redis_client = redis.Redis(host=connection['REDIS_HOST'], port=connection['REDIS_PORT'], username=connection['REDIS_USERNAME'], password=connection['REDIS_PASSWORD'])
is_connected = redis_client.ping()
print('Redis Connected:', is_connected)

written = redis_client.set("message", "Hello World!")
print('Message written:', written)

msg = redis_client.get("message")
print(msg.decode())
