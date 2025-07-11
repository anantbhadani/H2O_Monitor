import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Server URL (Configurable)
SERVER_URL = "http://localhost:5000/api/latest"  # Default to localhost

# Data storage for real-time plotting
time_stamps = deque(maxlen=50)
tds_values = deque(maxlen=50)
temperature_values = deque(maxlen=50)

# Recording variables
recording = False
recorded_data = []
record_count = 1  # File counter for recorded datasets

def configure_server():
    """Allow user to configure server URL"""
    global SERVER_URL
    new_url = simpledialog.askstring("Server Configuration", 
                                   "Enter server URL (e.g., http://192.168.0.105:5000/api/latest):",
                                   initialvalue=SERVER_URL)
    if new_url:
        SERVER_URL = new_url
        label_status.config(text=f"Server: {SERVER_URL}", fg="blue")

def fetch_data():
    """Fetch the latest data from Flask server."""
    try:
        response = requests.get(SERVER_URL, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # Validate data structure
        if "timestamp" in data and "tds_value" in data and "temperature" in data:
            time_stamps.append(data["timestamp"])
            tds_values.append(data["tds_value"])
            temperature_values.append(data["temperature"])

            # If recording, store the data
            if recording:
                recorded_data.append([data["timestamp"], data["tds_value"], data["temperature"]])

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error: {e}")
        # Add placeholder data to keep plot alive
        if len(time_stamps) == 0:
            time_stamps.append("No Data")
            tds_values.append(0)
            temperature_values.append(0)
    except Exception as e:
        print(f"⚠️ Error fetching data: {e}")

def update_plot(i):
    """Update plot in real-time."""
    fetch_data()
    
    if len(time_stamps) == 0:
        return
        
    ax1.clear()
    ax2.clear()

    # Only plot if we have valid data
    if time_stamps[0] != "No Data":
        ax1.plot(list(time_stamps), list(tds_values), label="TDS (ppm)", color='b', marker='o', linestyle='-')
        ax2.plot(list(time_stamps), list(temperature_values), label="Temperature (°C)", color='r', marker='x', linestyle='-')
    else:
        ax1.text(0.5, 0.5, 'No Data Available', ha='center', va='center', transform=ax1.transAxes)
        ax2.text(0.5, 0.5, 'No Data Available', ha='center', va='center', transform=ax2.transAxes)

    ax1.set_title("Real-Time TDS and Temperature Data")
    ax1.set_ylabel("TDS (ppm)")
    ax2.set_ylabel("Temperature (°C)")
    ax2.set_xlabel("Time")

    ax1.legend()
    ax2.legend()
    
    # Rotate x-axis labels only if we have data
    if time_stamps[0] != "No Data":
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

def get_next_filename():
    """Generate a unique filename like record_1.csv, record_2.csv, etc."""
    global record_count
    while True:
        filename = f"record_{record_count}.csv"
        if not os.path.exists(filename):
            return filename
        record_count += 1

def start_recording():
    """Start recording data."""
    global recording, recorded_data
    recording = True
    recorded_data = []  # Clear previous recorded data
    label_status.config(text="Recording: ON", fg="green")

def stop_recording():
    """Stop recording and save to a CSV file."""
    global recording
    recording = False
    if recorded_data:
        filename = get_next_filename()
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "tds_value", "temperature"])  # Header
                writer.writerows(recorded_data)

            label_status.config(text=f"Saved: {filename}", fg="blue")
            messagebox.showinfo("Success", f"Data saved to {filename}")
        except Exception as e:
            label_status.config(text="Error saving file!", fg="red")
            messagebox.showerror("Error", f"Failed to save file: {e}")
    else:
        label_status.config(text="No data recorded!", fg="red")
        messagebox.showwarning("Warning", "No data was recorded!")

# Create Tkinter GUI Window
root = tk.Tk()
root.title("Water Quality Monitoring")

# Create Matplotlib figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Buttons in Tkinter inside the graph window
frame = tk.Frame(root)
frame.pack()

btn_start = tk.Button(frame, text="Start Recording", command=start_recording, bg="green", fg="white", width=15)
btn_start.pack(side=tk.LEFT, padx=10, pady=10)

btn_stop = tk.Button(frame, text="Stop Recording", command=stop_recording, bg="red", fg="white", width=15)
btn_stop.pack(side=tk.LEFT, padx=10, pady=10)

btn_config = tk.Button(frame, text="Configure Server", command=configure_server, bg="blue", fg="white", width=15)
btn_config.pack(side=tk.LEFT, padx=10, pady=10)

# Status Label
label_status = tk.Label(root, text="Recording: OFF", fg="black")
label_status.pack()

# Start Animation
ani = animation.FuncAnimation(fig, update_plot, interval=2000)
root.mainloop()
