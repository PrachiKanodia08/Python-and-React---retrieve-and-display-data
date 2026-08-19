import json
import paho.mqtt.client as mqtt


BROKER = "broker.hivemq.com"
PORT = 8883
# TOPIC = "factory/motion"

OUTPUT_FILE = "sensor_data.txt"


def on_connect(client, userdata, flags, rc):
    print("Connected")
    client.subscribe("HP/CONSUMER_NO/+/+")


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    print(data)

    with open(OUTPUT_FILE, "a") as file:
        json.dump(data, file)
        file.write("\n")


client = mqtt.Client()
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message


client.connect(BROKER, PORT)

client.loop_forever()