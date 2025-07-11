# Configuration file for H2O Monitor Server
import socket

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

# Server Configuration
SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
SERVER_PORT = 5000
LOCAL_IP = get_local_ip()

# ESP32 Configuration (update this with your computer's IP address)
ESP32_SERVER_HOST = LOCAL_IP  # This will be your computer's IP address
ESP32_SERVER_PORT = 5000

# Database Configuration
CSV_FILE = "database.csv"

# GUI Configuration
GUI_UPDATE_INTERVAL = 2000  # milliseconds
GUI_MAX_DATA_POINTS = 50

print(f"Server will be available at: http://{LOCAL_IP}:{SERVER_PORT}")
print(f"ESP32 should connect to: http://{ESP32_SERVER_HOST}:{ESP32_SERVER_PORT}/api/data") 