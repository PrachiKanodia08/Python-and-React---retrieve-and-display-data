import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/motion"

client = mqtt.Client()
client.connect(BROKER, PORT)

sensor_names = [
    "Bed Room",
    "Kitchen",
    "Toilet",
    "Living Room",
    "Dining Room"
]

print("Publishing sensor data...")

while True:

    for sensor in sensor_names:

        payload = {
            "sensor_room": sensor,
            "motion": random.choice([True, False]),
            "timestamp": datetime.now().isoformat()
        }

        client.publish(TOPIC, json.dumps(payload))
        print(payload)

    time.sleep(5)