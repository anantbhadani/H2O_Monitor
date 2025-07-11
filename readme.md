# H2O Monitor - Water Quality Monitoring System

A real-time water quality monitoring system using ESP32, TDS sensor, and DS18B20 temperature sensor. The system displays live data on a GUI, stores readings in a CSV file, and allows recording for further analysis.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd H2O_Monitor/esp32_server
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python start_server.py
```
This will:
- Show your computer's IP address
- Start the Flask server
- Display connection information for the ESP32

### 3. Start the GUI (in a new terminal)
```bash
python gui.py
```

### 4. Configure ESP32
Update the server IP in `esp32_h2o_monitor.ino` with your computer's IP address (shown by the server).

## 🔧 Fixed Issues

### ✅ Requirements.txt
- Removed built-in Python modules (csv, datetime, os)
- Added correct package names
- Added flask-cors for CORS support

### ✅ GUI Improvements
- Made server URL configurable (defaults to localhost)
- Added better error handling for network issues
- Added "Configure Server" button
- Improved data validation
- Added user-friendly error messages
- Fixed potential threading issues

### ✅ Server Improvements
- Added CORS support
- Better error handling and logging
- Added health check endpoint
- Improved data validation
- Added proper HTTP status codes

### ✅ New Features
- Configuration file (`config.py`) for centralized settings
- Startup script (`start_server.py`) for easy server launch
- Automatic IP detection
- Better user feedback and error messages

## 📁 Project Structure
```
H2O_Monitor/
├── esp32_h2o_monitor.ino     # ESP32 Arduino code
├── esp32_server/
│   ├── server.py             # Flask server
│   ├── gui.py                # Real-time GUI
│   ├── config.py             # Configuration settings
│   ├── start_server.py       # Startup script
│   ├── requirements.txt      # Python dependencies
│   └── database.csv          # Data storage
└── README.md                 # This file
```

## 🔌 Hardware Setup

### Required Components
- ESP32-WROOM-32
- TDS Sensor (connected to GPIO32)
- DS18B20 Temperature Sensor (connected to GPIO4)
- Breadboard & Jumper Wires
- USB Cable

### Wiring
- **TDS Sensor**: GPIO32
- **DS18B20**: GPIO4
- **Stop Button**: GPIO13 (optional)

## 🌐 Network Configuration

### Finding Your IP Address
The server will automatically detect and display your IP address when you run `start_server.py`.

### ESP32 Configuration
Update line 13 in `esp32_h2o_monitor.ino`:
```cpp
const char* server_host = "YOUR_COMPUTER_IP"; // Replace with your IP
```

## 📊 Using the GUI

### Features
- **Real-time plotting** of TDS and temperature data
- **Start/Stop Recording** to save data to CSV files
- **Configure Server** button to change server URL
- **Auto-reconnection** if server is unavailable

### Recording Data
1. Click "Start Recording" to begin logging
2. Data is stored in memory during recording
3. Click "Stop Recording" to save to a CSV file
4. Files are auto-named (record_1.csv, record_2.csv, etc.)

## 🔍 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. GUI shows "No Data Available"**
- Check if the server is running
- Verify ESP32 is connected to the same network
- Use "Configure Server" button to set correct IP

**3. ESP32 can't connect to server**
- Ensure server is running on `0.0.0.0:5000`
- Check firewall settings
- Verify IP address in ESP32 code

**4. Permission errors on Windows**
- Run PowerShell as Administrator
- Or use: `python -m pip install -r requirements.txt`

### Debug Mode
The server runs in debug mode by default. Check the console for detailed error messages.

## 📈 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/data` | Accepts sensor data from ESP32 |
| GET | `/api/latest` | Returns latest sensor data |
| GET | `/health` | Health check endpoint |

## 🔮 Future Enhancements
- MQTT integration for cloud monitoring
- Web dashboard for remote access
- Mobile app for real-time monitoring
- Data analytics and trend analysis
- Alert system for water quality thresholds

## 👨‍💻 Development

### Adding New Features
1. Update `config.py` for new settings
2. Modify `server.py` for new API endpoints
3. Update `gui.py` for new UI features
4. Test with ESP32 code

### Testing
- Use the health check endpoint: `http://localhost:5000/health`
- Monitor server logs for debugging
- Test GUI with different network conditions

---

💡 **Developed by Anant Bhadani** | 🌊 **Monitor Your Water Quality!**

## 🆘 Support
If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure ESP32 and computer are on the same network
4. Check server logs for error messages

