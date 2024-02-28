import pandas as pd

# Debugging Script
df = pd.read_csv('data_combined.csv', sep='\t') 

# 1. Verify Column Existence
print(df.columns)  

# 2. Sample Data Inspection
print(df.head(3))  # Print the first 3 rows

# 3. Detailed Info for the 'hour_of_day' Column
print(df['hour_of_day '].describe())  

# 4. Check for Missing Values
print(df['hour_of_day '].isnull().sum()) 