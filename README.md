# mqtt-python-clients
MQTT Python clients for different sensors

Purpose
-------

Python Scripts to execute MQTT clients in RPI to get data from different vendors and send it to an MQTT Server.

Installation
------------

In order to install the library (*and all development dependencies*), run the following command in a Raspberry Pi using Raspbian (Adafruit DHT does not install in regular Linux systems):

    $ pip3 install -e .

Note so far it is only working with pip3

Usage
-----

To get temperature, humidity and pressure from bme280:

    $ python3 mqtt-bme280.py <client> <topic> --server <mqtt-server-address> --port <mqtt-port> --user <mqtt-server-user> --password <mqtt-server-user-password> --interval <int> --keepalive <int>

To get temperature and humidity from DHT11:

    $ python3 mqtt-dht11.py <client> <rpi-gpio-pin> <topic> -server <mqtt-server-address> --port <mqtt-port> --user <mqtt-server-user> --password <mqtt-server-user-password> --interval <int> --keepalive <int>

To get temperature and humidity from DHT22:

    $ python3 mqtt-dht22.py <client> <rpi-gpio-pin> <topic> -server <mqtt-server-address> --port <mqtt-port> --user <mqtt-server-user> --password <mqtt-server-user-password> --interval <int> --keepalive <int>
