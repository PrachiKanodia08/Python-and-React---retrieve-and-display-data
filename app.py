from flask import Flask, jsonify
from flask_cors import CORS
import threading
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)

# HP/APT_NAME/HOUSE_NO/Sensor1/MOVED_AWAY -> Object Moved Away
# HP/APT_NAME/HOUSE_NO/Sensor1/DETECTED -> Movement Detected
# HP/APT_NAME/HOUSE_NO/Sensor1/ROOM EMPTY -> Room Empty

BROKER = "broker.hivemq.com"
# PORT = 8883 1883
PORT = 8883
# TOPIC = "HP/CONSUMER_NO/+/+"

# Latest data for React
latest_sensor_data = {}

# Thread synchronization
data_lock = threading.Lock()


def on_connect(client, userdata, flags, reason_code, properties=None):

    print("Flask MQTT Connected")

    client.subscribe("HP/CONSUMER_NO/+/+")


def on_message(client, userdata, msg):

    try:

        sensor = json.loads(msg.payload.decode())
        print("sensor: ",sensor)

        sensor_room = sensor["sensor_room"]

        with data_lock:

            latest_sensor_data[sensor_room] = sensor

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