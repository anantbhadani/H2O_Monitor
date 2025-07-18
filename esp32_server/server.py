from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CSV File Path
CSV_FILE = "database.csv"

# Store the latest data in memory
latest_data = {"tds_value": 0.0, "temperature": 0.0, "timestamp": "N/A"}

# Create CSV if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "tds_value", "temperature"])
    logger.info(f"Created new CSV file: {CSV_FILE}")

@app.route('/api/data', methods=['POST'])
def receive_data():
    global latest_data
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400
        
        tds_value = float(data.get("tds_value", 0.0))
        temperature = float(data.get("temperature", 0.0))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update latest data
        latest_data = {"tds_value": tds_value, "temperature": temperature, "timestamp": timestamp}

        # Save to CSV
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, tds_value, temperature])

        logger.info(f"Data received - TDS: {tds_value}, Temp: {temperature}")
        return jsonify({"status": "success", "message": "Data saved!"}), 200

    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
        return jsonify({"status": "error", "message": "Invalid data format"}), 400
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/latest', methods=['GET'])
def get_latest_data():
    return jsonify(latest_data)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    logger.info(f"Server will be available at: http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
