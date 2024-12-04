import csv
import os
from datetime import datetime

def save_telemetry(telem, filename='tel.csv'):
    fieldnames = [
        'time', 'latitude', 'longitude', 'altitude', 'x', 'y', 'z', 'vx', 'vy', 'vz',
        'roll', 'pitch', 'yaw', 'roll_rate', 'pitch_rate', 'yaw_rate',
        'voltage', 'cell_voltage', 'mode', 'armed', 'connected'
    ]
    if os.path.exists(filename):
        mode = 'a'
    else:
        mode = 'w'

    with open(filename, mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        if mode == 'w':
            writer.writeheader()

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        writer.writerow({
            'time': current_time,
            'latitude': telem.lat,
            'longitude': telem.lon,
            'altitude' : telem.alt,
            'x': telem.x,
            'y': telem.y,
            'z': telem.z,
            'vx': telem.vx,
            'vy': telem.vy,
            'vz': telem.vz,
            'roll': telem.roll,
            'pitch': telem.pitch,
            'yaw': telem.yaw,
            'roll_rate': telem.roll_rate,
            'pitch_rate': telem.pitch_rate,
            'yaw_rate': telem.yaw_rate,
            'voltage': telem.voltage,
            'cell_voltage': telem.cell_voltage,
            'mode': telem.mode,
            'armed': telem.armed,
            'connected': telem.connected
        })