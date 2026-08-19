import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 8883
BASE_TOPIC = "HP/CONSUMER_NO"

EVENTS = {
    "DETECTED": "Movement Detected",
    "MOVED_AWAY": "Object Moved Away",
    "ROOM EMPTY": "Room Empty"
}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.tls_set()

client.connect(BROKER, PORT)

SENSOR_ROOM = "Living Room"
SENSOR_ID = "R1004"

print("Publishing sensor data...")

while True:

    event_key = random.choice(list(EVENTS.keys()))
            
    TOPIC = f"{BASE_TOPIC}/{SENSOR_ROOM}/{event_key}"

    payload = {
        "sensor_id": SENSOR_ID,
        "sensor_room": SENSOR_ROOM,
        "motion": EVENTS[event_key],
        "timestamp": datetime.now().isoformat()
    }

    client.publish(TOPIC, json.dumps(payload))
    print(payload)

    time.sleep(6)