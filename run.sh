#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

USB_PORT=$(bashio::config 'usb_port')
BAUD_RATE=$(bashio::config 'baud_rate')
MQTT_BROKER=$(bashio::services 'mqtt' 'host')
MQTT_PORT=$(bashio::services 'mqtt' 'port')
MQTT_USER=$(bashio::services 'mqtt' 'username')
MQTT_PASSWORD=$(bashio::services 'mqtt' 'password')
MQTT_TOPIC_PREFIX=$(bashio::config 'mqtt_topic_prefix')

export USB_PORT BAUD_RATE MQTT_BROKER MQTT_PORT MQTT_USER MQTT_PASSWORD MQTT_TOPIC_PREFIX
#
## Start the main script
python3 /app/serial2mqtt.py