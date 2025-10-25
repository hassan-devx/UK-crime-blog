import os
import pandas as pd

# Define the path to the CSV relative to this file
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'data', 'cleaned_crime_data.csv'))

def load_cleaned_data():
    df = pd.read_csv(DATA_PATH)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Inject default region for dashboard filtering
    df['region'] = 'South Wales'  # You can later map this dynamically

    # Clean city column if it exists
    if 'city' in df.columns:
        df['city'] = df['city'].fillna("Unknown").str.strip().str.title()
        df['city'] = df['city'].replace({'The Vale Of Glamorgan': 'Vale Of Glamorgan'})

    # Ensure month is datetime and add month_str
    if 'month' in df.columns:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
        df['month_str'] = df['month'].dt.strftime('%Y-%m')

    return df