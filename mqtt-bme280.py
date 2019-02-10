import os
import time
import sys
import paho.mqtt.client as mqtt
import json

from kpn_senml import *

from Adafruit_BME280 import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name",
                    help="Name of the MQTT client")
parser.add_argument("topic",
                    help="Topic on the MQTT server")
parser.add_argument("--server",
                    help="ip address of the MQTT server")
parser.add_argument("--port", type=int,
                    help="MQTT port in the server (default 1883)")
parser.add_argument("--user",
                    help="User of the MQTT server (default no user)")
parser.add_argument("--password",
                    help="Password of the user's  MQTT server (default no user-password)")
parser.add_argument("--interval", type=int,
                    help="Interval to read sensor data (minimum and default 2 seconds)")
parser.add_argument("--keepalive", type=int,
                    help="MQTT Keep Alive interval (minimum 10 seconds, default 60 seconds)")

args = parser.parse_args()

MQTT_CLIENT = args.name
TOPIC = args.topic

MQTT_SERVER=args.server

if not MQTT_SERVER:
   MQTT_SERVER="127.0.0.1"

MQTT_PORT=args.port

if MQTT_PORT == 0:
   MQTT_PORT=1883

MQTT_SERVER_USER = args.user

MQTT_SERVER_PASSWORD=""

if args.user:
   MQTT_SERVER_PASSWORD=args.password

INTERVAL = 2

if args.interval > 2:
   INTERVAL = args.interval

MQTT_KEEPALIVE = 60

if args.keepalive > 10:
   MQTT_KEEPALIVE = args.keepalive

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()

print 'Temp      = {0:0.3f} deg C'.format(degrees)
print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
print 'Humidity  = {0:0.2f} %'.format(humidity)

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.

sensor_data = {'temperature': 0, 'humidity': 0, 'pressure': 0}

next_reading = time.time()

client = mqtt.Client(MQTT_CLIENT)

# Set access token
client.username_pw_set(MQTT_SERVER_USER,MQTT_SERVER_PASSWORD)

# Connect to MQTT_SERVER
client.connect(MQTT_SERVER, MQTT_PORT, MQTT_KEEPALIVE)

# Create SenML structures

senml_pack = SenmlPack(MQTT_CLIENT)

client.loop_start()

try:
    while True:
        pressure = sensor.read_pressure()
        humidity = sensor.read_humidity()
        temperature = sensor.read_temperature()
        print(u"Temperature: {:g}\u00b0C, Pressure: {:g}Pa, Humidity: {:g}%".format(temperature, pressure, humidity))
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity
        sensor_data['pressure'] = pressure


        senml_data_temp  = SenmlRecord("temperature")
        senml_data_temp.unit = "C"
        senml_data_temp.value= temperature

        senml_pack.add(senml_data_temp)

        # Sending temperature data to MQTT Server
        client.publish(TOPIC, senml_pack.to_json(),1)

        senml_pack.clear()

        senml_data_humid = SenmlRecord("humidity")
        senml_data_humid.value = humidity
        senml_data_humid.unit = "%RH"

        senml_pack.add(senml_data_humid)

        # Sending humidity data to MQTT Server
        client.publish(TOPIC, senml_pack.to_json(),1)

        senml_pack.clear()

        senml_data_press = SenmlRecord("pressure")
        senml_data_press.value = pressure
        senml_data_press.unit = "Pa"

        senml_pack.add(senml_data_press)

        # Sending humidity data to MQTT Server
        client.publish(TOPIC, senml_pack.to_json(),1)

        senml_pack.clear()

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()

