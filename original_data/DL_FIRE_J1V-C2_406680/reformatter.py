import pandas as pd
import os
from datetime import datetime, timedelta

# Function to convert Unix timestamp to datetime and format as MM/DD/YYYY HH:MM
def convert_timestamp(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%m/%d/%Y %H:%M')

# Assuming all CSV files are in the 'non_event' directory
# Assuming all CSV files are in the 'non_event' directory
directory = 'non_event_folder'
new_folder = 'converted'


if not os.path.exists(os.path.join(directory, new_folder)):
    os.makedirs(os.path.join(directory, new_folder))
# Iterate over all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(os.path.join(directory, filename), sep=',', header=0)
        print(df.columns)
        print(df['dt'].head())
        # Extract timestamp from 'viirs_point' and convert to datetime
        df['dt'] = df['viirs_point'].str.split('_').str[2]
        df['dt'] = pd.to_datetime(df['dt'], unit='s')
       
        #df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d %H:%M:%S')
        
        # Calculate day_of_week and hour_of_day
        df['day_of_week'] = df['dt'].dt.dayofweek
        df['hour_of_day'] = df['dt'].dt.hour
        
        # Convert dt to the desired format
        df['dt'] = df['dt'].apply(lambda x: x.strftime('%m/%d/%Y %H:%M'))
        
        # Reorder and rename columns to match the desired format
        df = df[['clouds', 'wind_speed', 'hour_of_day', 'fire', 'rain', 'dt', 'day_of_week', 'humidity', 'viirs_point', 'temperature']]
        
        # Write the transformed DataFrame to a new CSV file
        new_filename = f'converted_{filename}'
        df.to_csv(os.path.join(directory, new_folder, new_filename), index=False)

print("Conversion completed.")
