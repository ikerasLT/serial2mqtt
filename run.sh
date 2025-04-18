#!/usr/bin/env bashio

CONFIG_PATH=/data/options.json

#usb_port = '/dev/ttyUSB0'  # read from addon config
#baud_rate = 115200 # read from addon config
#
#logger.info("Connecting to Serial on Port: %s,at Baud Rate: %d", usb_port, baud_rate)
#ser = serial.Serial(usb_port, baud_rate)
#
#
## establish a mqtt connection
#mqtt_broker = "your_mqtt_broker_ip" #read from services API
#mqtt_port = 1883 #read from services API
#mqtt_user = "mqtt_user" #read from services API
#mqtt_password = "mqtt_password" #read from services API
#mqtt_topic_prefix = "homeassistant/sensor/esp" # read from addon config
#mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
#mqtt_client.username_pw_set(mqtt_user, mqtt_password)

USB_PORT = "$(bashio::config 'usb_port')"
BAUD_RATE = "$(bashio::config 'baud_rate')"
MQTT_BROKER = "$(bashio::services 'mqtt' 'host')"
MQTT_PORT = "$(bashio::services 'mqtt' 'port')"
MQTT_USER = "$(bashio::services 'mqtt' 'username')"
MQTT_PASSWORD = "$(bashio::services 'mqtt' 'password')"
MQTT_TOPIC_PREFIX = "$(bashio::config 'mqtt_topic_prefix')"

export USB_PORT, BAUD_RATE, MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPIC_PREFIX

# Start the main script
python3 /app/serial2mqtt.py