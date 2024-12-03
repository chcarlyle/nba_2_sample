import pandas as pd

# Function to calculate the margin of victory for each game
def calculate_margin(df: pd.DataFrame):
    df['margin'] = df['hpts'] - df['vpts']
    return df

# Example of a function that calculates average margin for each team
def average_margin_by_team(df: pd.DataFrame):
    team_margin = df.groupby(['hname']).agg({'margin': 'mean'}).reset_index()
    return team_margin
