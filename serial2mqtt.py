import json
import logging
import os
import time

import serial
import paho.mqtt.client as mqtt

# TODO: Better handle discovery messages
# TODO: Add Birth and Will messages

# setup logging
logging.basicConfig(level=logging.INFO,  # or DEBUG for more detail TODO: add config option
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)

logger.info("Starting serial2mqtt...")


# establish a serial connection
usb_port = os.getenv('USB_PORT', '/dev/ttyUSB0')
baud_rate = int(os.getenv('BAUD_RATE', 115200))

logger.info("Connecting to Serial on Port: %s,at Baud Rate: %d", usb_port, baud_rate)
ser = serial.Serial(usb_port, baud_rate)


# establish a mqtt connection
mqtt_broker = os.getenv('MQTT_BROKER', "your_mqtt_broker_ip")
mqtt_port = int(os.getenv('MQTT_PORT', 1883))
mqtt_user = os.getenv('MQTT_USER', "mqtt_user")
mqtt_password = os.getenv('MQTT_PASSWORD', "mqtt_password")
mqtt_topic_prefix = os.getenv('MQTT_TOPIC_PREFIX', "homeassistant/sensor/esp")
mqtt_client = mqtt.Client('serial2mqtt')
mqtt_client.username_pw_set(mqtt_user, mqtt_password)
mqtt_client.on_disconnect = lambda client, userdata, rc: logger.error("Disconnected from MQTT Broker: %s", rc)

logger.info("Connecting to MQTT Broker: %s, Port: %d", mqtt_broker, mqtt_port)
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

autodiscovery_sent = []

# read from serial
def read_serial():
    try:
        line = ser.readline().decode('utf-8').strip()
        logger.info("Received: %s", line)
        return line
    except Exception as e:
        logger.error("Error reading from serial: %s", e)
        return None


def parse_channel(payload):
    return payload.get("unique_id")


def parse_autodiscovery(payload, channel):
    del payload['value']
    del payload['retain']

    payload['origin'] = {
        "name": "serial2mqtt",
    }
    payload['state_topic'] = f"{mqtt_topic_prefix}/{channel}/state"

    payload['device']['identifiers'] = [payload['device']['ids']] # TODO: remove once fixed in firmware
    payload['qos'] = 0

    return payload


def parse_value(payload):
    return payload.get("value")


def parse_data(data):
    payload = json.loads(data)
    value = parse_value(payload)
    channel = parse_channel(payload)
    autodiscovery = parse_autodiscovery(payload, channel)

    return channel, autodiscovery, value

# send mqtt autodiscovery
def send_autodiscovery(channel, autodiscovery):
    if channel in autodiscovery_sent:
        logger.info("Autodiscovery already sent for channel: %s", channel)
        return

    topic = f"{mqtt_topic_prefix}/{channel}/config"
    response = mqtt_client.publish(topic, json.dumps(autodiscovery))
    logger.info("Sent autodiscovery to topic: %s: %s", topic, autodiscovery)
    autodiscovery_sent.append(channel)

# send mqtt data
def send_data(channel, value):
    topic = f"{mqtt_topic_prefix}/{channel}/state"
    response = mqtt_client.publish(topic, json.dumps(value), qos=0) # TODO: remove qos=0 once fixed in firmware
    logger.info("Sent data to topic: %s, %s", topic, value)

# main loop
while True:
    try:
        if ser.in_waiting > 0:
            data = read_serial()
            if data:
                channel, autodiscovery, value = parse_data(data)
                send_autodiscovery(channel, autodiscovery)
                send_data(channel, value)

    except Exception as e:
        logger.error("Error: %s", e)

    time.sleep(1)