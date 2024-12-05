import pandas as pd

# Function to clean the scraped data
def clean_data(df: pd.DataFrame):
    # Example of cleaning: convert columns to appropriate types
    df['mp'] = pd.to_numeric(df['mp'], errors='coerce')
    df['ORtg'] = pd.to_numeric(df['ORtg'], errors='coerce')
    df['DRtg'] = pd.to_numeric(df['DRtg'], errors='coerce')
    df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce')

    # Drop rows with missing or invalid data
    df = df.dropna(subset=["mp", "bpm"])
    return df

def generate_vorp(df: pd.DataFrame):
    # Calculate VORP: BPM * (Minutes Played / 48) / 8
    # Convert seconds to minutes by dividing by 60
    df['vorp'] = (df['bpm'] * (df['mp'] / 60) / 48) / 8
    return df
