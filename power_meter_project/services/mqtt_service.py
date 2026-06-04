import paho.mqtt.client as mqtt

from config.mqtt_config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD
)

mqtt_client = mqtt.Client()

mqtt_client.username_pw_set(
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD
)

mqtt_client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)

mqtt_client.loop_start()