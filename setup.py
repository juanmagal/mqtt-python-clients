"""Packaging settings."""

from os.path import abspath, dirname, join

from codecs import open

from setuptools import Command, find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name = 'mqttclients',
    version = '0.1.0',
    description = 'Several MQTT clients for differnt sensors.',
    long_description = long_description,
    url = 'https://github.com/juanmagal/mqtt-python-clients',
    author = 'Juan Manuel Fernandez',
    author_email = 'juanma.galmes@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: IoT',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: Raspbian',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'mqtt',
    install_requires = ['Adafruit_DHT','Adafruit_BME280','paho-mqtt','kpn-senml'],
)
