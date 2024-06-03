import serial
import tkinter as tk
from tkinter import ttk

# Initialize serial communication with Arduino
arduino_port = '/dev/ttyUSB0'  # Replace with your port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def read_sensor_values():
    # Read data from serial port
    data = ser.readline().decode().strip().split(',')
   
    # Extract sensor values
    humidity = float(data[0])
    temperature = float(data[1])
    distance = float(data[2])
    pir = int(data[3])
    ldr = int(data[4])
    mq2 = int(data[5])

    # Update sensor values in the GUI
    update_sensor_value("humidity", humidity)
    update_sensor_value("temperature", temperature)
    update_sensor_value("distance", distance)
    update_sensor_value("pir", pir)
    update_sensor_value("ldr", ldr)
    update_sensor_value("mq2", mq2)

    # Schedule the function to run again
    root.after(1000, read_sensor_values)

def stop_buzzer():
    ser.write("stopBuzzer\n".encode())

def toggle_buzzer():
    if buzzer_var.get():
        ser.write("startBuzzer\n".encode())
        buzzer_button.config(text="Buzzer: ON", style="On.TButton")
        print("Buzzer turned on")
    else:
        ser.write("stopBuzzer\n".encode())
        buzzer_button.config(text="Buzzer: OFF", style="Off.TButton")
        print("Buzzer turned off")

def create_sensor_frame(sensor, text, row, col):
    frame = tk.Frame(root, padx=10, pady=10, bg=colors[sensor], relief=tk.RAISED, bd=2)
    frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    text_label = tk.Label(frame, text=text, font=("Arial", 16, "bold"), bg=colors[sensor])
    text_label.pack(pady=5)
    progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=200)
    progress_bar.pack(pady=5)
    value_label = tk.Label(frame, text="--", font=("Arial", 14), bg=colors[sensor])
    value_label.pack(pady=5)
    unit_label = tk.Label(frame, text=units[sensor], font=("Arial", 12), bg=colors[sensor])
    unit_label.pack(pady=2)
    frames[sensor] = frame
    labels[sensor] = value_label
    progress_bars[sensor] = progress_bar

def update_sensor_value(sensor, value):
    labels[sensor].config(text=f"{value}")
    progress_bars[sensor]['value'] = value

root = tk.Tk()
root.title("Smart Home Monitoring System")
root.geometry("800x600")
root.configure(bg="lightgray")

colors = {
    "humidity": "lightblue",
    "temperature": "lightgreen",
    "distance": "lightyellow",
    "pir": "lightcoral",
    "ldr": "lightpink",
    "mq2": "lightgray"
}

units = {
    "humidity": "%",
    "temperature": "°C",
    "distance": "cm",
    "pir": "",
    "ldr": "lx",
    "mq2": "ppm"
}

frames = {}
labels = {}
progress_bars = {}

create_sensor_frame("humidity", "Humidity", 0, 0)
create_sensor_frame("temperature", "Temperature", 0, 1)
create_sensor_frame("distance", "Distance", 0, 2)
create_sensor_frame("pir", "PIR Status", 1, 0)
create_sensor_frame("ldr", "LDR Status", 1, 1)
create_sensor_frame("mq2", "MQ2 Gas Level", 1, 2)

buzzer_var = tk.BooleanVar()
buzzer_button = ttk.Checkbutton(root, text="Buzzer: OFF", variable=buzzer_var, command=toggle_buzzer, style="Off.TButton")
buzzer_button.grid(row=2, column=0, columnspan=3, pady=(20, 10), padx=10, sticky="ew")

style = ttk.Style()
style.configure("On.TButton", foreground="green")
style.configure("Off.TButton", foreground="red")

separator = ttk.Separator(root, orient='horizontal')
separator.grid(row=3, column=0, columnspan=3, sticky="ew", pady=20, padx=10)

for i in range(4):  # Rows (including the separator)
    root.grid_rowconfigure(i, weight=1)
for j in range(3):  # Columns
    root.grid_columnconfigure(j, weight=1)

read_sensor_values()

root.mainloop()

ser.close()
