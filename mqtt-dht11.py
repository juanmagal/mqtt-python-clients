import os
import time
import sys
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

HOST = '127.0.0.1'
CLIENT_ID = "DHT11-Rasp1"
#ACCESS_TOKEN = 'DHT22_DEMO_TOKEN'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT11.
INTERVAL=10

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time() 

client = mqtt.Client(CLIENT_ID)

# Set access token
#client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(HOST, 1883, 60)

client.loop_start()

try:
    while True:
        humidity,temperature = dht.read_retry(dht.DHT11, 18)
        humidity2,temperature2 = dht.read_retry(dht.DHT11, 16, 20)
        humidity3,temperature3 = dht.read_retry(dht.DHT11, 7, 25)
#        humidity = float(humidity)
#        temperature = float(temperature)
        if humidity is None:
            print 'No humidity 1 read'
        if temperature is None:
            print 'No temperature 1 read'
        if humidity2 is None:
            print 'No humidity 2 read'
        if temperature2 is None:
            print 'No temperature 2 read'
        if humidity3 is None:
            print 'No humidity 3 read'
        if temperature3 is None:
            print 'No temperature 3 read'
        if humidity is not None and temperature is not None:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)



        #print(u"Temperature: {:f}\u00b0C, Humidity: {:f}%".format(temperature, humidity))
        #sensor_data['temperature'] = temperature
        #sensor_data['humidity'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        #client.publish('test/topic', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
