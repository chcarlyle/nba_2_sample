import pandas as pd
import re

# Function to clean the scraped data
def clean_data(df: pd.DataFrame):
    """
    Cleans and preprocesses the scraped basketball data.

    This function converts specific columns to appropriate data types, calculates
    new columns, and removes invalid or missing data.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing scraped data. 
                           Expected columns include 'mp', 'ORtg', 'DRtg', 'bpm', and 'date'.

    Returns:
        pd.DataFrame: A cleaned DataFrame with valid data.

    Example:
        cleaned_df = clean_data(df)
    """
    df['mp'] = pd.to_numeric(df['mp'], errors='coerce') / 60  # Convert minutes played from seconds to minutes
    df['ORtg'] = pd.to_numeric(df['ORtg'], errors='coerce')  # Convert offensive rating to numeric
    df['DRtg'] = pd.to_numeric(df['DRtg'], errors='coerce')  # Convert defensive rating to numeric
    df['bpm'] = pd.to_numeric(df['bpm'], errors='coerce')    # Convert BPM to numeric
    df['date'] = pd.to_datetime(df['date_game'])             # Convert date_game to datetime
    df.drop('date_game', axis=1, inplace=True)               #Drop the old date column

    # Drop rows with missing or invalid data for 'mp' and 'bpm'
    df = df.dropna(subset=["mp", "bpm"])
    return df

# Function to generate VORP
def generate_vorp(df: pd.DataFrame):
    """
    Calculates the Value Over Replacement Player (VORP) metric.

    VORP is calculated using the formula:
    VORP = (BPM * (Minutes Played / 48)) / 8

    Parameters:
        df (pd.DataFrame): The input DataFrame containing a 'bpm' column 
                           and 'mp' (minutes played) column.

    Returns:
        pd.DataFrame: The DataFrame with a new 'vorp' column.

    Example:
        df = generate_vorp(df)
    """
    df['vorp'] = (df['bpm'] * (df['mp']) / 48) / 8
    return df

# Function to calculate Net Rating
def generate_net(df: pd.DataFrame):
    """
    Calculates the Net Rating for each row in the DataFrame.

    Net Rating is defined as the difference between Offensive Rating (ORtg) 
    and Defensive Rating (DRtg):
    Net Rating = ORtg - DRtg

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'ORtg' and 'DRtg' columns.

    Returns:
        pd.DataFrame: The DataFrame with a new 'net' column representing Net Rating.

    Example:
        df = generate_net(df)
    """
    df['net'] = df['ORtg'] - df['DRtg']
    return df

# Function to compile yearly data
def compile_yearly_data(year, directory="."):
    """
    Compiles all CSV files for a specified year into a single DataFrame.

    This function searches for CSV files in the given directory with filenames 
    following the format 'monthyear.csv' (e.g., 'january2023.csv'). The year 
    is extracted from the filename using a regex pattern.

    Parameters:
        year (int): The year to match in the filenames.
        directory (str): The directory to search for CSV files (default is the current directory).

    Returns:
        pd.DataFrame: A single DataFrame containing the compiled data from all matching files.

    Raises:
        ValueError: If no files matching the specified year are found.

    Example:
        df = compile_yearly_data(2023, directory="data")
    """
    from pathlib import Path
    all_files = list(Path(directory).glob("*.csv"))

    # Match files with the format 'monthyear.csv'
    pattern = re.compile(r"^[a-zA-Z]+(" + str(year) + r")\.csv$")
    matching_files = [file for file in all_files if pattern.match(file.name)]

    # Compile the data into a single DataFrame
    data_frames = [pd.read_csv(file) for file in matching_files]
    if not data_frames:
        raise ValueError(f"No files found for year {year} in directory '{directory}'.")
    
    compiled_df = pd.concat(data_frames, ignore_index=True)
    return compiled_df

# Function to subset data for a specific player
def subsetplayer(df: pd.DataFrame, player: str):
    """
    Filters the DataFrame to include only data for a specified player.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing player performance data.
        player (str): The name or identifier of the player to filter.

    Returns:
        pd.DataFrame: A filtered DataFrame containing data for the specified player.

    Notes:
        Prints a message if no data is found for the specified player.

    Example:
        player_data = subsetplayer(df, player="LeBron James")
    """
    filtered_df = df[df['player'] == player].reset_index(drop=True)
    
    if filtered_df.empty:
        print(f"No data found for player '{player}'.")
    
    return filtered_df

# Function to subset data by date range
def subsetdates(df: pd.DataFrame, date1, date2):
    """
    Filters the DataFrame to include rows within a specified date range.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing a 'date' column.
        date1 (str or datetime): The start date (inclusive).
        date2 (str or datetime): The end date (inclusive).

    Returns:
        pd.DataFrame: A filtered DataFrame with rows within the specified date range.

    Notes:
        Prints a message if no data is found within the date range.

    Example:
        date_filtered_data = subsetdates(df, "2023-01-01", "2023-12-31")
    """
    # Ensure the 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Filter the DataFrame for the specified date range
    filtered_df = df[(df['date'] >= pd.to_datetime(date1)) & (df['date'] <= pd.to_datetime(date2))].reset_index(drop=True)
    
    if filtered_df.empty:
        print(f"No data found between {date1} and {date2}.")
    
    return filtered_df
