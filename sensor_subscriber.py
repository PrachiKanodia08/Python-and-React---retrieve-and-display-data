import json
import paho.mqtt.client as mqtt
from datetime import datetime


BROKER = "broker.hivemq.com"
PORT = 8883
# TOPIC = "factory/motion"
# TOPIC = "HP/CONSUMER_NO/+/+"
#TOPIC = "PRESENCE/LD2410/STATUS"
TOPIC = "PRESENCE/BLR/MANSARVOVAR/A4562/STATUS"

SENSOR_DATA_FILE = "sensor_room_data.txt"
SENSOR_STATUS_FILE = "sensor_status_data.txt"


def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    try:

        data = json.loads(msg.payload.decode())
        print(data)

        data["timestamp"] = datetime.now().isoformat()

        status = data.get("status", "")

        if status in ["DETECTED", "NOT_DETECTED"]:

            with open(SENSOR_DATA_FILE, "a") as file:
                json.dump(data, file)
                file.write("\n")

        elif status in ["OFF_LINE", "ON_LINE", "KEEP_ALIVE"]:

            with open(SENSOR_STATUS_FILE, "a") as file:
                json.dump(data, file)
                file.write("\n")

        else:

            print(f"Unknown status received: {status}")


    except json.JSONDecodeError:

        print("Invalid JSON received")


    except Exception as e:

        print(f"Error processing MQTT message: {e}")



client = mqtt.Client()
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER, PORT)

client.loop_forever()