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
TOPIC = "PRESENCE/LD2410/STATUS"
#TOPIC = "PRESENCE/BLR/MANSARVOVAR/A4562/STATUS"

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

        print("\nMQTT Message Received:")
        print("sensor_data : ", sensor_data)


        # -------------------------------------------------
        # Get sensor room
        # -------------------------------------------------

        sensor = sensor_data.get("sensor_room")

        if not sensor:
            print("sensor_room not found in payload")
            return


        # -------------------------------------------------
        # Get incoming status
        # -------------------------------------------------

        incoming_status = sensor_data.get("status", "").strip().upper()
        print("incoming_status : ", incoming_status)


        # -------------------------------------------------
        # Timestamp for the latest received message
        # -------------------------------------------------

        timestamp = datetime.now().isoformat()


        # -------------------------------------------------
        # SENSOR STATUS MESSAGE
        #
        # DETECETED / NOT_DETECETED
        # -------------------------------------------------

        if incoming_status in ["DETECTED", "NOT_DETECTED"]:

            with data_lock:

                # Check whether this sensor already has data
                existing_sensor_data = latest_sensor_data.get(sensor, {})


                # Start with the NEW sensor reading
                updated_sensor_data = sensor_data.copy()


                # Preserve previously received sensor_status
                if "sensor_status" in existing_sensor_data:

                    updated_sensor_data["sensor_status"] = (
                        existing_sensor_data["sensor_status"]
                    )


                # Update timestamp
                updated_sensor_data["timestamp"] = timestamp


                # Save updated sensor data
                latest_sensor_data[sensor] = updated_sensor_data


        # -------------------------------------------------
        # SENSOR STATUS / CONNECTIVITY MESSAGE
        #
        # OFF_LINE / ON_LINE / KEEP_ALIVE
        # -------------------------------------------------

        elif incoming_status in ["OFF_LINE", "ON_LINE", "KEEP_ALIVE"]:

            with data_lock:

                # Get existing data for this sensor
                existing_sensor_data = latest_sensor_data.get(
                    sensor,
                    {}
                ).copy()


                # If there is no previous data,
                # create the basic sensor record
                if not existing_sensor_data:

                    existing_sensor_data["sensor_room"] = sensor


                # Add / update sensor_status
                existing_sensor_data["sensor_status"] = incoming_status


                # Update timestamp
                #existing_sensor_data["timestamp"] = timestamp


                # Save the merged data
                latest_sensor_data[sensor] = existing_sensor_data


        # -------------------------------------------------
        # UNKNOWN STATUS
        # -------------------------------------------------

        else:

            print(
                f"Unknown status received from {sensor}: "
                f"{incoming_status}"
            )

    except Exception as e:

        print("Error processing MQTT message:", e)



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