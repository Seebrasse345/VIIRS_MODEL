import pandas as pd
import os

# Set data directories
data_dir = "C:\\Users\\seebr\\OneDrive\\Desktop\\Model_fire\\data\\features" 

def combine_features_with_separators(data_dir):
    all_data = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(data_dir, file_name)
            df = pd.read_csv(file_path)

            # Add separator rows (adjust the number of separators as needed)
            separator = pd.DataFrame({'fire': [None] * df.shape[1]}) # Create a row of NaNs
            for _ in range(2): 
                df = pd.concat([df, separator], ignore_index=True) 

            all_data.append(df)

    # Combine DataFrames
    combined_df = pd.concat(all_data, ignore_index=True)

    # Save the combined DataFrame
    combined_df.to_csv("data_combined.csv", index=False)

# Combine the CSVs
combine_features_with_separators(data_dir)
