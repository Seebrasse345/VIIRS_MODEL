import json
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import random

API_KEY = "9813026307c8bb72b9dc1a1cb2818386"

def format_viirs_time(time_str):
    # Pad the time string with leading zeros to ensure it is 4 digits
    time_str = time_str.zfill(4)
    return f"{time_str[:-2]}:{time_str[-2:]}"

def get_surrounding_dates(date_str, time_str):
    formatted_time = format_viirs_time(time_str)

    # Use the acq_date (datetime object) directly and combine with the formatted_time
    dt = date_str.replace(hour=int(formatted_time[:2]), minute=int(formatted_time[-2:]))

    one_day_before = dt - timedelta(days=2)
    one_day_after = dt + timedelta(days=0)
    return int(one_day_before.timestamp()), int(one_day_after.timestamp())

def openweather(lat, lon, start, end, API_KEY):
    response = requests.get(f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API_KEY}")
    return response.json()  # Convert response to JSON

# Read VIIRS data
viirs_file_path = r'E:\\python_ground\\Modis\\DL_FIRE_J1V-C2_406680\\viirs.csv'
df = pd.read_csv(viirs_file_path)

# Convert acq_date column to datetime 
df['acq_date'] = pd.to_datetime(df['acq_date'], format="%d/%m/%Y")

# Filter by date criteria
df_filtered = df[df['acq_date'] > datetime(2023, 5, 1)]  


# Dictionary to store the API responses with filtered data
filtered_weather_data = {}
counter = 1
limit = 10000

# Process 500 randomly selected rows
random_indices = random.sample(df_filtered.index.tolist(), limit) 
for index in random_indices:
    row = df_filtered.loc[index]
    
    
    start, end = get_surrounding_dates(row['acq_date'], str(row['acq_time']))
    api_response = openweather(row['latitude'], row['longitude'], start, end, API_KEY)
    print(api_response)
    

    # Filter and restructure the data
    filtered_list = []
    for record in api_response.get('list', []):
        filtered_record = {
            'dt': record.get('dt'),
            'temp': record.get('main', {}).get('temp'),
            'humidity': record.get('main', {}).get('humidity'),
            'wind_speed': record.get('wind', {}).get('speed'),
            'rain': record.get('rain', {}).get('1h') if 'rain' in record else 0,
            # Additional potential features for the model
            'clouds': record.get('clouds', {}).get('all', 0),
            'weather_main': record.get('weather', [{}])[0].get('main', ''),
            'weather_description': record.get('weather', [{}])[0].get('description', '')
        }
        filtered_list.append(filtered_record)

    key = f"viirs_point_{index + 1}_{row['acq_date']}_{row['latitude']},{row['longitude']}"
    filtered_weather_data[key] = filtered_list

# Save the filtered data to a JSON file
with open(r'E:\\python_ground\\Modis\\DL_FIRE_J1V-C2_406680\\new_data_non_event.json', 'w') as outfile:
    json.dump(filtered_weather_data, outfile)

print("Filtered weather data collected and saved.")