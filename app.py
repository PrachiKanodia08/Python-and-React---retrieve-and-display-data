from datetime import datetime, timezone
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows your React app to talk to Python

current_count = -1

@app.route('/api/counter')
def counter():
    global current_count
    current_count+=1
    # current_time = datetime.now().strftime("%H:%M:%S")
    current_time = datetime.now(timezone.utc).isoformat()
    return jsonify({
        "count": current_count,
        "timestamp": current_time,
        "role": "Viewer"
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)