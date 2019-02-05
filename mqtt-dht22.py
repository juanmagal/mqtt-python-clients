import os
import time
import sys
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

from kpn_senml import *

#MQTT_SERVER = '192.168.122.155'
MQTT_SERVER = '192.168.1.162'
#PORT = 1883
PORT = 30643
USER = 'admin'
PASSWORD = 'public'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time() 

client = mqtt.Client("DHT22Sensor")

# Set access token
client.username_pw_set(USER,PASSWORD)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(MQTT_SERVER, PORT, 60)


# Create SenML structures

senml_pack = SenmlPack("MQTTtest")

client.loop_start()

try:
    while True:
        humidity,temperature = dht.read_retry(dht.DHT22, 4)
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(temperature, humidity))
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        senml_data_temp  = SenmlRecord("temperature")
        senml_data_temp.unit = "C"
        senml_data_temp.value= temperature

        senml_pack.add(senml_data_temp)

        # Sending temperature data to MQTT Server
        # client.publish('test/topic', json.dumps(sensor_data), 1)
        client.publish('DataTopic', senml_pack.to_json(),1)

        senml_pack.clear()

        senml_data_humid = SenmlRecord("humidity")
        senml_data_humid.value = humidity
        senml_data_humid.unit = "%RH"

        senml_pack.add(senml_data_humid)

        # Sending humidity data to MQTT Server
        # client.publish('test/topic', json.dumps(sensor_data), 1)
        client.publish('DataTopic', senml_pack.to_json(),1)

        senml_pack.clear()

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
