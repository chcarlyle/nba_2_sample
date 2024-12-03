import pandas as pd

# Function to clean the scraped data
def clean_data(df: pd.DataFrame):
    # Example of cleaning: convert columns to appropriate types
    df['date_game'] = pd.to_datetime(df['date_game'], errors='coerce')
    df['vpts'] = pd.to_numeric(df['vpts'], errors='coerce')
    df['hpts'] = pd.to_numeric(df['hpts'], errors='coerce')

    # Drop rows with missing or invalid data
    df = df.dropna(subset=["date_game", "vpts", "hpts"])
    return df
