# H2O Monitor

H2O Monitor is a real-time **water quality monitoring system** that uses **ESP32**, **TDS Sensor**, and **DS18B20 Temperature Sensor** to measure Total Dissolved Solids (TDS) and temperature. The system displays live data on a GUI, stores readings in a CSV file, and allows recording for further analysis.

---

## Features
**Real-time Data Monitoring** - View live TDS and temperature readings <br>
**ESP32-Based Sensor Integration** - Collects data using WiFi<br>
**Flask API Server** - Receives and stores sensor data in a CSV file<br>
**Graphical User Interface (GUI)** - Plots live sensor data<br>
**Data Recording Feature** - Saves readings with timestamps in CSV format<br>
**Auto WiFi Connection** - ESP32 automatically connects to WiFi<br>

---

## Project Structure
```
H2O_Monitor/
│── esp_32_h2o_monitor.ino  # ESP32 Code (Arduino IDE)
│── esp32_server/
│   │── server.py           # Flask server for receiving/storing data        
│   |── gui.py              # Real-time graph plotter GUI
│   |── database.csv        # Stored sensor data
│   |── requirements.txt    # Required Python libraries
│── README.md               # Project documentation
```
---

## Hardware Requirements
- **ESP32-WROOM-32**
- **TDS Sensor**
- **DS18B20 Temperature Sensor**
- **Breadboard & Jumper Wires**
- **USB Cable** (for ESP32 connection)

---

## Installation & Setup

### 1️ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️ Run the Flask Server
```bash
python server.py
```
✔️ Runs on `http://192.168.0.105:5000`  
✔️ Stores data in `database.csv`  
✔️ Provides `/api/latest` for real-time updates  

### 3️ Start the Real-Time GUI
```bash
python gui.py
```
✔️ Displays **live TDS & Temperature data**  
✔️ **Start/Stop Recording** button included  

### 4️⃣ Deploy ESP32 Code
- Flash the `esp32_code` onto the **ESP32** using the **Arduino IDE**  
- Update the **server IP** inside the ESP32 code  
- Restart the ESP32 and check for **real-time data updates!**  

---

## Recording Sensor Data
📌 Click **"Start Recording"** in the GUI to log data.  
📌 Data is stored in a **CSV file with a timestamp**.  
📌 Click **"Stop Recording"** to save the session.  
📌 Files are auto-named (`record_1.csv`, `record_2.csv`, etc.).  

---

## API Endpoints
| Method | Endpoint      | Description                      |
|--------|-------------|----------------------------------|
| `POST`  | `/api/data`  | Accepts sensor data from ESP32 |
| `GET`   | `/api/latest` | Returns the latest sensor data |

---

## Future Enhancements
🚀 **MQTT Integration** for cloud-based monitoring  
📊 **Web Dashboard** for remote access  
📱 **Mobile App** for real-time monitoring  

---

💡 **Developed by Anant Bhadani** | 🌊 **Monitor Your Water Quality!**

