import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 8883
# BASE_TOPIC = "HP/CONSUMER_NO"
TOPIC = "PRESENCE/LD2410/STATUS"

# EVENTS = {
#     "DETECTED": "Movement Detected",
#     "MOVED_AWAY": "Object Moved Away",
#     "ROOM EMPTY": "Room Empty"
# }

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.tls_set()

client.connect(BROKER, PORT)

SENSOR_ROOM = "Kitchen"
SENSOR_ID = "3"

print("Publishing sensor data...")

while True:

    # event_key = random.choice(list(EVENTS.keys()))
        
    # TOPIC = f"{BASE_TOPIC}/{SENSOR_ROOM}/{event_key}"

    #Randomly choose which type of payload to generate
    payload_type = random.choice(["status", "keep_alive"])

    # OPTION 1: SENSOR STATUS PAYLOAD
    #-----------------------------------

    if payload_type == "status":

        status = random.choice(["Detected", "Not Detected"])

        if status == "Detected":

            moving_target = random.choice([True, False])
            stationary_target = random.choice([True, False])

            # Make sure at least one target exists
            if not moving_target and not stationary_target:
                moving_target = True

            moving_target_dist = random.randint(1, 30) if moving_target else 0
            stationary_target_dist = random.randint(1, 30) if stationary_target else 0

        else:

            moving_target = False
            moving_target_dist = 0

            stationary_target = False
            stationary_target_dist = 0

        payload = {
            "sensor_room": SENSOR_ROOM,
            "status": status,
            "Moving Target": moving_target,
            "Moving Target Dist": moving_target_dist,
            "Stationary Target": stationary_target,
            "Stationary Target Dist": stationary_target_dist,
            "Wifi": random.randint(0, 90)
        }

    # OPTION 2: KEEP ALIVE PAYLOAD
    # -----------------------------------

    else:

        payload = {
            "Message": f"{SENSOR_ROOM} Keep Alive",
            "Wifi": str(random.randint(0, 90))
        }

    client.publish(TOPIC, json.dumps(payload))
    print(payload)

    time.sleep(10)