#!/usr/bin/env python3
"""
Startup script for H2O Monitor Server
This script will show the server IP and start the Flask server
"""

import subprocess
import sys
import os
from config import LOCAL_IP, SERVER_PORT

def install_requirements():
    """Install required packages if not already installed"""
    try:
        import flask
        import requests
        import matplotlib
        print("✅ All required packages are already installed")
    except ImportError:
        print("📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")

def main():
    print("🌊 H2O Monitor Server")
    print("=" * 50)
    
    # Install requirements
    install_requirements()
    
    print(f"\n🚀 Starting server...")
    print(f"📡 Server will be available at: http://{LOCAL_IP}:{SERVER_PORT}")
    print(f"🔗 ESP32 should connect to: http://{LOCAL_IP}:{SERVER_PORT}/api/data")
    print(f"📊 GUI can be accessed at: http://{LOCAL_IP}:{SERVER_PORT}")
    print("\n💡 To start the GUI, run: python gui.py")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask server
    try:
        from server import app
        app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main() 