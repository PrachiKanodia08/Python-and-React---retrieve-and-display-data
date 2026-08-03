import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "factory/motion"

client = mqtt.Client(client_id="bedroom_sensor")
client.connect(BROKER, PORT)

SENSOR_ROOM = "Bed Room"

print("Publishing sensor data...")

while True:

    payload = {
        "sensor_room": SENSOR_ROOM,
        "motion": random.choice([True, False]),
        "timestamp": datetime.now().isoformat()
    }

    client.publish(TOPIC, json.dumps(payload))
    print(payload)

    time.sleep(6)