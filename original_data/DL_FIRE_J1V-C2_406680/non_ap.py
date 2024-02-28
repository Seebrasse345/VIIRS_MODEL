import json
import csv
import pandas as pd
from datetime import datetime, timedelta
import os

def round_to_nearest_hour(t):
    dt = datetime.strptime(t, "%d/%m/%Y %H:%M")
    rounded_dt = dt + timedelta(minutes=30)
    return rounded_dt.replace(minute=0, second=0, microsecond=0)
def format_time(t):
    return f"{int(t)//100:02}:{int(t)%100:02}"
# Load VIIRS data and JSON data
data_dir = os.getcwd()
data_dir = data_dir + "\\viirs.csv"
viirs_data = pd.read_csv(data_dir)
json_dir = os.getcwd() + "\\new_data_non_event.json"
with open(json_dir, 'r') as file:
    weather_data = json.load(file)

# Process VIIRS data to get timestamps (Assuming this is needed)
viirs_data['formatted_time'] = viirs_data['acq_time'].apply(format_time)
viirs_data['rounded_time'] = viirs_data['acq_date'] + ' ' + viirs_data['formatted_time']
viirs_data['rounded_timestamp'] = viirs_data['rounded_time'].apply(lambda x: round_to_nearest_hour(x).timestamp())

# Create a mapping of viirs_point to timestamps (Assuming this is needed)
fire_event_mapping = {}
for index, row in viirs_data.iterrows():
    key = f"viirs_point_{index+1}_{row['acq_date']}_{row['latitude']},{row['longitude']}"
    fire_event_mapping[key] = row['rounded_timestamp']

# Create the output directory
output_dir = "non_event_folder"
os.makedirs(output_dir, exist_ok=True)  

# Process each VIIRS point separately
for viirs_point, hourly_data in weather_data.items():
    fire_timestamp = fire_event_mapping.get(viirs_point, None)

    if fire_timestamp:
        # Calculate the start of the 24-hour window 1.5 days before the event
        start_dt = datetime.fromtimestamp(fire_timestamp) - timedelta(hours=36) 

        # Format filename to avoid errors
        formatted_viirs_point = viirs_point.replace('/', '-').replace(',', '_')

        # Open a CSV file for this VIIRS point
        with open(os.path.join(output_dir, f'{formatted_viirs_point}.csv'), 'w', newline='') as csvfile: 
            fieldnames = ['viirs_point', 'dt', 'temperature', 'humidity', 'wind_speed', 'rain', 'clouds', 'weather_main', 'weather_description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            hours_written = 0

            # Filter and write weather data until we have at least 24 hours
            for hour in hourly_data:
                dt = hour['dt']
                if start_dt <= datetime.fromtimestamp(dt):  # Check if within the window
                    writer.writerow({
                        'viirs_point': viirs_point, 'dt': dt, 'temperature': hour['temp'],
                        'humidity': hour['humidity'], 'wind_speed': hour['wind_speed'],
                        'rain': hour.get('rain', 0), 'clouds': hour['clouds'],
                        'weather_main': hour['weather_main'], 'weather_description': hour['weather_description']
                    })
                    hours_written += 1

                    if hours_written >= 24:
                        break  # Exit the loop once we have enough data 
            
            # Save the CSV file
            csvfile.close()