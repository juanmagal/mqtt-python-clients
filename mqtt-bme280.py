import os
import time
import sys
import paho.mqtt.client as mqtt
import json

from kpn_senml import *

from Adafruit_BME280 import *

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

degrees = sensor.read_temperature()
pascals = sensor.read_pressure()
hectopascals = pascals / 100
humidity = sensor.read_humidity()

print 'Temp      = {0:0.3f} deg C'.format(degrees)
print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
print 'Humidity  = {0:0.2f} %'.format(humidity)



#MQTT_SERVER = '192.168.122.155'
MQTT_SERVER = '192.168.1.137'
USER = 'admin'
PASSWORD = 'public'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0, 'humidity': 0, 'pressure': 0}

next_reading = time.time()

client = mqtt.Client("BMP280Sensor")

# Set access token
client.username_pw_set(USER,PASSWORD)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(MQTT_SERVER, 1883, 60)


# Create SenML structures

senml_pack = SenmlPack("MQTTtest")

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

        senml_data_press = SenmlRecord("pressure")
        senml_data_press.value = pressure
        senml_data_press.unit = "Pa"

        senml_pack.add(senml_data_press)

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

