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

SENSOR_ROOM = "Toilet-1"
SENSOR_ID = "5"

print("Publishing sensor data...")

while True:

    #Randomly choose which type of payload to generate
    status = random.choice(["OFF_LINE", "ON_LINE", "KEEP_ALIVE", "DETECTED", "NOT_DETECTED"])

    # OPTION 1: SENSOR DETECETED/NOT_DETECTED PAYLOAD
    #-----------------------------------

    if ((status == "DETECTED") or (status == "NOT_DETECTED")):

        if status == "DETECTED":

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
            "Wifi": random.randint(1, 90)
        }

    # OPTION 2: KEEP_ALIVE/ON_LINE PAYLOAD
    # -----------------------------------

    else:

        if ((status == "KEEP_ALIVE") or (status == "ON_LINE")):

            payload = {
                "sensor_room": SENSOR_ROOM,
                "status": status,
                "Wifi": str(random.randint(1, 90))
            }

    # OPTION 3: OFF_LINE PAYLOAD
    # -----------------------------------

        else:
            payload = {
                "sensor_room": SENSOR_ROOM,
                "status": status
            }


    client.publish(TOPIC, json.dumps(payload))
    print(payload)

    time.sleep(10)