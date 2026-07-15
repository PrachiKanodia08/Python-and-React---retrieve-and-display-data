from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "sensor_data.txt"


@app.route("/api/sensors")
def get_sensor_data():

    if not os.path.exists(DATA_FILE):
        return jsonify({
            "status": "error",
            "message": "sensor_data.txt not found"
        }), 404

    latest_sensor_data = {}

    try:
        with open(DATA_FILE, "r") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:
                    sensor = json.loads(line)

                    sensor_room = sensor["sensor_room"]

                    # Keep only the latest record for each sensor
                    latest_sensor_data[sensor_room] = sensor

                except json.JSONDecodeError:
                    continue

        return jsonify({
            "status": "success",
            "totalSensors": len(latest_sensor_data),
            "data": list(latest_sensor_data.values())
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)