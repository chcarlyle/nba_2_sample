import pandas as pd
import re

# Function to clean the scraped data
def clean_data(df: pd.DataFrame):
    # Example of cleaning: convert columns to appropriate types
    df['mp'] = pd.to_numeric(df['mp'], errors='coerce')/60
    df['ORtg'] = pd.to_numeric(df['ORtg'], errors='coerce')
    df['DRtg'] = pd.to_numeric(df['DRtg'], errors='coerce')
    df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce)

    # Drop rows with missing or invalid data
    df = df.dropna(subset=["mp", "bpm"])
    return df

def generate_vorp(df: pd.DataFrame):
    # Calculate VORP: BPM * (Minutes Played / 48) / 8
    # Convert seconds to minutes by dividing by 60
    df['vorp'] = (df['bpm'] * (df['mp']) / 48) / 8
    return df

def generate_net(df: pd.DataFrame):
    df['net'] = (df['ORtg']) - (df['DRtg'])
    return df

def compile_yearly_data(year, directory="."):
    # List all files in the specified directory
    from pathlib import Path
    all_files = list(Path(directory).glob("*.csv"))
    
    # Use a regex pattern to match files with the format 'monthyear.csv' for the specified year
    pattern = re.compile(r"^[a-zA-Z]+(" + str(year) + r")\.csv$")
    matching_files = [file for file in all_files if pattern.match(file.name)]
    
    # Read and compile the data into a single DataFrame
    data_frames = [pd.read_csv(file) for file in matching_files]
    if not data_frames:
        raise ValueError(f"No files found for year {year} in directory '{directory}'.")
    
    compiled_df = pd.concat(data_frames, ignore_index=True)
    return compiled_df

def subsetplayer(df: pd.DataFrame, player: str):
    # Filter the DataFrame
    filtered_df = df[df['player'] == player].reset_index(drop=True)
    
    if filtered_df.empty:
        print(f"No data found for player '{player}'.")
    
    return filtered_df

def subsetdates(df: pd.DataFrame, date1, date2):
    """
    Subset a DataFrame for rows within a specified date range.

    Parameters:
    df (pd.DataFrame): The input DataFrame with a 'date' column.
    date1: The start date (inclusive).
    date2: The end date (inclusive).

    Returns:
    pd.DataFrame: The filtered DataFrame.
    """
    # Ensure the 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Filter the DataFrame for the specified date range
    filtered_df = df[(df['date'] >= pd.to_datetime(date1)) & (df['date'] <= pd.to_datetime(date2))].reset_index(drop=True)
    
    if filtered_df.empty:
        print(f"No data found between {date1} and {date2}.")
    
    return filtered_df

