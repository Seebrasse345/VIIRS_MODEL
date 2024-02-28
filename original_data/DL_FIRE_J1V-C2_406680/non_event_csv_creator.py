import json
import csv
import pandas as pd
from datetime import datetime, timedelta
import os

# Load JSON data 
json_dir = os.getcwd() + "\\new_data_non_event.json"
with open(json_dir, 'r') as file:
    weather_data = json.load(file)

# Create the output directory
output_dir = "non_event_folder"
os.makedirs(output_dir, exist_ok=True) 

# Process each VIIRS point separately (we'll still use the same loop structure)
for viirs_point, hourly_data in weather_data.items(): 
    # Format filename to avoid errors
    formatted_viirs_point = viirs_point.replace('/', '-').replace(',', '_')
    formatted_viirs_point = viirs_point.replace('/', '-').replace(',', '_').replace(':', '-')


    # Open a CSV file for this VIIRS point
    with open(os.path.join(output_dir, f'{formatted_viirs_point}.csv'), 'w', newline='') as csvfile: 
        fieldnames = ['viirs_point', 'dt', 'temperature', 'humidity', 'wind_speed', 'rain', 'clouds', 'weather_main', 'weather_description', 'fire'] 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        hours_written = 0

        # Filter and write weather data until we have at least 24 hours
        for hour in hourly_data:
            dt = hour['dt']
            writer.writerow({
                'viirs_point': viirs_point, 
                'dt': dt, 'temperature': hour['temp'],
                'humidity': hour['humidity'], 'wind_speed': hour['wind_speed'],
                'rain': hour.get('rain', 0), 'clouds': hour['clouds'],
                'weather_main': hour['weather_main'], 
                'weather_description': hour['weather_description'],
                'fire': 0  # Add the fire column with a value of 0
            })
            hours_written += 1

            if hours_written >= 24:
                break  # Exit the loop once we have enough data 