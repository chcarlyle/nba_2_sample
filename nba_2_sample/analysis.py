import pandas as pd
from scipy.stats import ttest_ind, ks_2samp
import nba_2_sample.data_cleaning as dc
import matplotlib.pyplot as plt
import seaborn as sns

def average_vorp_by_team(df: pd.DataFrame):
    """
    Calculates the average VORP (Value Over Replacement Player) for each team in the given DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing at least the columns 'team' and 'vorp'.

    Returns:
        pd.DataFrame: A new DataFrame with two columns: 'team' and the average VORP for each team.

    Example:
        import pandas as pd

        # Example data
        data = {'team': ['A', 'A', 'B', 'B'], 'vorp': [1.5, 2.5, 3.0, 4.0]}
        df = pd.DataFrame(data)

        # Call the function
        team_avg = average_vorp_by_team(df)
        print(team_avg)
    """
    team_avg = df.groupby(['team']).agg({'vorp': 'mean'}).reset_index()
    return team_avg


def player_average(df: pd.DataFrame, player: str, metric: str):
    """
    Calculates the average value of a specified metric for a given player.

    Parameters:
        df (pd.DataFrame): The DataFrame containing player performance data.
        player (str): The name or identifier of the player for whom the average is calculated.
        metric (str): The column name representing the metric to calculate the average for.

    Returns:
        pd.DataFrame: A DataFrame with the average value of the specified metric for the given player.

    Notes:
        This function assumes the presence of a helper function `dc.subsetplayer` 
        that filters the DataFrame for the given player.

    Example:
        import pandas as pd

        # Example data
        data = {'player': ['John', 'John', 'Doe', 'Doe'], 'points': [10, 20, 15, 25]}
        df = pd.DataFrame(data)

        # Define a dummy dc.subsetplayer function
        def subsetplayer(df, player):
            return df[df['player'] == player]

        # Monkey patch for demonstration
        import types
        dc = types.SimpleNamespace(subsetplayer=subsetplayer)

        # Call the function
        player_avg = player_average(df, player='John', metric='points')
        print(player_avg)
    """
    sub = dc.subsetplayer(df, player)
    player_avg = sub.agg({metric: 'mean'}).reset_index()
    return player_avg


def two_sample(df1: pd.DataFrame, df2: pd.DataFrame, metric: str):
    """
    Perform a two-sample t-test and a Kolmogorov-Smirnov test on a specified metric.

    Parameters:
    df1 (pd.DataFrame): The first DataFrame.
    df2 (pd.DataFrame): The second DataFrame.
    metric (str): The name of the metric/column to test.

    Returns:
    dict: A dictionary with the results of the t-test and KS-test.
    """
    if metric not in df1.columns or metric not in df2.columns:
        raise ValueError(f"The metric '{metric}' must exist in both DataFrames.")

    # Extract the data for the metric
    data1 = df1[metric].dropna()
    data2 = df2[metric].dropna()

    # Perform the two-sample t-test
    t_stat, t_p_value = ttest_ind(data1, data2, equal_var=False)  # Welch's t-test

    # Perform the Kolmogorov-Smirnov test
    ks_stat, ks_p_value = ks_2samp(data1, data2)

    # Return results as a dictionary
    results = {
        't-test': {'t-statistic': t_stat, 'p-value': t_p_value},
        'ks-test': {'ks-statistic': ks_stat, 'p-value': ks_p_value}
    }

    return results

def plot_density(df: pd.DataFrame, metric: str):
    """
    Plots a density curve for a specified metric from a given DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to plot.
        metric (str): The column name in the DataFrame for which the density plot will be generated.

    Returns:
        None: Displays the density plot.

    Example:
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt

        # Example data
        df = pd.DataFrame({'metric': [1, 2, 3, 4, 5]})

        # Call the function
        plot_density(df, metric='metric')
    """
    sns.kdeplot(data=df, x=metric, fill=True, alpha=0.5)
    plt.title(f'Density Plot for {metric}')
    plt.xlabel(metric)
    plt.ylabel('Density')
    plt.show()

def plot_double_density(df1: pd.DataFrame, df2: pd.DataFrame, metric: str, label1: str = 'DataFrame 1', label2: str = 'DataFrame 2'):
    """
    Plots density curves for the specified metric from two dataframes on the same plot.
    
    Parameters:
        df1 (pd.DataFrame): The first dataframe.
        df2 (pd.DataFrame): The second dataframe.
        metric (str): The column name to plot the density for.
        label1 (str): Label for the first dataframe's density curve.
        label2 (str): Label for the second dataframe's density curve.
    """
    sns.kdeplot(data=df1, x=metric, fill=True, alpha=0.5, label=label1)
    sns.kdeplot(data=df2, x=metric, fill=True, alpha=0.5, label=label2)
    plt.title(f'Density Plot for {metric}')
    plt.xlabel(metric)
    plt.ylabel('Density')
    plt.legend()
    plt.show()
