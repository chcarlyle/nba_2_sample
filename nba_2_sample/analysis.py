if __name__ == '__main__':
    import pandas as pd
    from scipy.stats import ttest_ind, ks_2samp
    import nba_2_sample.data_cleaning as dc

    # Example of a function that calculates average margin for each team
    def average_vorp_by_team(df: pd.DataFrame):
        team_avg = df.groupby(['team']).agg({'vorp': 'mean'}).reset_index()
        return team_avg

    def player_average(df: pd.DataFrame, player: str, metric: str):
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