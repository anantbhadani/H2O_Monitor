import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import csv
import os
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Server URL (Update with your actual server IP)
SERVER_URL = "http://192.168.0.105:5000/api/latest"

# Data storage for real-time plotting
time_stamps = deque(maxlen=50)
tds_values = deque(maxlen=50)
temperature_values = deque(maxlen=50)

# Recording variables
recording = False
recorded_data = []
record_count = 1  # File counter for recorded datasets

def fetch_data():
    """Fetch the latest data from Flask server."""
    try:
        response = requests.get(SERVER_URL)
        data = response.json()

        time_stamps.append(data["timestamp"])
        tds_values.append(data["tds_value"])
        temperature_values.append(data["temperature"])

        # If recording, store the data
        if recording:
            recorded_data.append([data["timestamp"], data["tds_value"], data["temperature"]])

    except Exception as e:
        print(f"⚠️ Error fetching data: {e}")

def update_plot(i):
    """Update plot in real-time."""
    fetch_data()
    ax1.clear()
    ax2.clear()

    ax1.plot(time_stamps, tds_values, label="TDS (ppm)", color='b', marker='o', linestyle='-')
    ax2.plot(time_stamps, temperature_values, label="Temperature (°C)", color='r', marker='x', linestyle='-')

    ax1.set_title("Real-Time TDS and Temperature Data")
    ax1.set_ylabel("TDS (ppm)")
    ax2.set_ylabel("Temperature (°C)")
    ax2.set_xlabel("Time")

    ax1.legend()
    ax2.legend()
    plt.xticks(rotation=45)

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
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "tds_value", "temperature"])  # Header
            writer.writerows(recorded_data)

        label_status.config(text=f"Saved: {filename}", fg="blue")
    else:
        label_status.config(text="No data recorded!", fg="red")

# Create Tkinter GUI Window
root = tk.Tk()
root.title("Water Quality Monitoring")

# Create Matplotlib figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Buttons in Tkinter inside the graph window
frame = tk.Frame(root)
frame.pack()

btn_start = tk.Button(frame, text="Start Recording", command=start_recording, bg="green", fg="white", width=15)
btn_start.pack(side=tk.LEFT, padx=10, pady=10)

btn_stop = tk.Button(frame, text="Stop Recording", command=stop_recording, bg="red", fg="white", width=15)
btn_stop.pack(side=tk.LEFT, padx=10, pady=10)

# Status Label
label_status = tk.Label(root, text="Recording: OFF", fg="black")
label_status.pack()

# Start Animation
ani = animation.FuncAnimation(fig, update_plot, interval=2000)
root.mainloop()
