import pandas as pd
import data_cleaning as dc

# Function to calculate the margin of victory for each game
def calculate_margin(df: pd.DataFrame):
    df['margin'] = df['hpts'] - df['vpts']
    return df

# Example of a function that calculates average margin for each team
def average_vorp_by_team(df: pd.DataFrame):
    team_avg = df.groupby(['team']).agg({'vorp': 'mean'}).reset_index()
    return team_avg

def player_average(df: pd.DataFrame, player: str, metric: str):
    sub = dc.subsetplayer(df, player)
    player_avg = sub.agg({metric: 'mean'}).reset_index()
    return player_avg
