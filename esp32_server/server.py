from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

# CSV File Path
CSV_FILE = "database.csv"

# Store the latest data in memory
latest_data = {"tds_value": 0.0, "temperature": 0.0, "timestamp": "N/A"}

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "tds_value", "temperature"])

@app.route('/api/data', methods=['POST'])
def receive_data():
    global latest_data
    try:
        data = request.json
        tds_value = float(data.get("tds_value", 0.0))
        temperature = float(data.get("temperature", 0.0))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update latest data
        latest_data = {"tds_value": tds_value, "temperature": temperature, "timestamp": timestamp}

        # Save to CSV
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, tds_value, temperature])

        return jsonify({"status": "success", "message": "Data saved!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
