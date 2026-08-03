from flask import Flask, jsonify
from flask_cors import CORS
import json
import threading
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/motion"

OUTPUT_FILE = "sensor_data.txt"

# Stores latest value of every sensor
latest_sensor_data = {}

# Lock for thread safety
data_lock = threading.Lock()


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT Broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    sensor = json.loads(msg.payload.decode())

    sensor_room = sensor["sensor_room"]

    with data_lock:
        latest_sensor_data[sensor_room] = sensor

    with open(OUTPUT_FILE, "a") as file:
        json.dump(sensor, file)
        file.write("\n")


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT)

mqtt_thread = threading.Thread(
    target=mqtt_client.loop_forever,
    daemon=True
)

mqtt_thread.start()


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