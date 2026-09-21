from flask import Flask, jsonify
from flask_cors import CORS
import threading
import json
import paho.mqtt.client as mqtt
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)


BROKER = "broker.hivemq.com"
# PORT = 8883 1883
PORT = 8883
#TOPIC = "PRESENCE/LD2410/STATUS"
TOPIC = "PRESENCE/BLR/MANSARVOVAR/A4562/STATUS"

# Latest data for React
latest_sensor_data = {}

# Thread synchronization
data_lock = threading.Lock()


def on_connect(client, userdata, flags, reason_code, properties=None):

    print("Flask MQTT Connected")

    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    global latest_sensor_data

    try:

        sensor_data = json.loads(msg.payload.decode())

        sensor_data["timestamp"] = datetime.now().isoformat()
        print(sensor_data)

        sensor = sensor_data["sensor_room"]

        with data_lock:

            latest_sensor_data[sensor] = sensor_data

    except Exception as e:

        print(e)



mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqtt_client.tls_set()

mqtt_client.on_connect = on_connect

mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT)

mqtt_client.loop_start()


@app.route("/api/sensors")
def sensors():

    with data_lock:

        return jsonify({

            "status": "success",
            "totalSensors": len(latest_sensor_data),
            "data": list(latest_sensor_data.values())

        })


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)