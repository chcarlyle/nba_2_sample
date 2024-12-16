"""
app.py

This module defines a Streamlit application for scraping, cleaning, and analyzing NBA game data. 
It integrates functionalities from the `data_scraping`, `data_cleaning`, and `analysis` modules into 
a user-friendly interface.

Features:
- **Scraping**: Allows users to scrape NBA game data for a specific year and month.
- **Cleaning**: Upload raw data, clean it, and generate advanced metrics like VORP and NET rating.
- **Analysis**: Visualize data with density plots and perform statistical tests (e.g., t-tests, KS tests).

Key sections in the app:
- Sidebar options for "Scrape Data," "Clean Data," and "Analyze Data."
- Interactive widgets for user inputs like player names, date ranges, and metric selection.

Dependencies:
- Requires `Streamlit` for the user interface and other libraries (`pandas`, `seaborn`, etc.) for data handling.
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ks_2samp
from nba_2_sample import data_cleaning, data_scraping, analysis

# Import functions from the repository
from data_scraping import scrape_nba_ids, scrape_month
from data_cleaning import clean_data, generate_vorp, generate_net, subsetplayer, subsetdates
from analysis import plot_density, two_sample

# Streamlit app
st.set_page_config(page_title="NBA Player Performance Analysis", layout="wide")

# Sidebar
st.sidebar.title("NBA Analysis Options")
option = st.sidebar.radio("Select an option:", [
    "Scrape Data",
    "Clean Data",
    "Analyze Data"
])

# Global variables
game_data = None  # Stores scraped game data
cleaned_data = None  # Stores cleaned and processed data

# Scrape Data
if option == "Scrape Data":
    """
    Handles the data scraping functionality, allowing users to scrape game and advanced statistics data
    for a specified year and month.
    """
    st.title("Scrape NBA Game Data")
    year = st.number_input("Enter the year:", min_value=2000, max_value=2025, step=1, value=2024)
    month = st.text_input("Enter the month (e.g., 'october'):", value="october")

    if st.button("Scrape Data"):
        with st.spinner("Scraping game data..."):
            game_data = scrape_nba_ids(year, month)  # Fetch game data
        
        if not game_data.empty:
            st.success("Game data scraped successfully!")
            st.dataframe(game_data)

            if st.button("Scrape Advanced Stats"):
                with st.spinner("Scraping advanced stats for games..."):
                    advanced_data = scrape_month(game_data)  # Fetch advanced stats
                if not advanced_data.empty:
                    st.success("Advanced stats scraped successfully!")
                    st.dataframe(advanced_data)
                else:
                    st.error("Failed to scrape advanced stats.")
        else:
            st.error("No game data found for the specified month and year.")

# Clean Data
elif option == "Clean Data":
    """
    Handles data cleaning, allowing users to upload raw scraped data, clean it, and download the
    cleaned version with additional metrics such as VORP and NET added.
    """
    st.title("Clean and Process Data")
    uploaded_file = st.file_uploader("Upload a CSV file of scraped data:", type="csv")

    if uploaded_file is not None:
        raw_data = pd.read_csv(uploaded_file)
        st.write("Raw Data:")
        st.dataframe(raw_data)

        with st.spinner("Cleaning data..."):
            cleaned_data = clean_data(raw_data)  # Clean raw data
            cleaned_data = generate_vorp(cleaned_data)  # Add VORP metric
            cleaned_data = generate_net(cleaned_data)  # Add NET metric

        st.success("Data cleaned successfully!")
        st.write("Cleaned Data:")
        st.dataframe(cleaned_data)

        if st.button("Download Cleaned Data"):
            csv = cleaned_data.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download as CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

# Analyze Data
elif option == "Analyze Data":
    """
    Handles data analysis, including density plots, statistical tests, and subsetting data by player
    and date range.
    """
    st.title("Analyze and Visualize Data")
    uploaded_file = st.file_uploader("Upload a CSV file of cleaned data:", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Cleaned Data:")
        st.dataframe(data)

        analysis_option = st.selectbox("Select an analysis option:", [
            "Density Plot",
            "Two-Sample Test",
            "Subset by Player and Date"
        ])

        if analysis_option == "Density Plot":
            """
            Allows users to generate a density plot for a selected metric.
            """
            metric = st.selectbox("Select a metric to plot:", options=["vorp", "net", "bpm", "ORtg", "DRtg"])

            if st.button("Plot Density"):
                st.write(f"Density Plot for {metric}")
                fig, ax = plt.subplots()
                sns.kdeplot(data=data, x=metric, fill=True, alpha=0.5, ax=ax)
                ax.set_title(f"Density Plot for {metric}")
                ax.set_xlabel(metric)
                ax.set_ylabel("Density")
                st.pyplot(fig)

        elif analysis_option == "Two-Sample Test":
            """
            Performs two-sample t-tests and Kolmogorov-Smirnov tests for a selected metric
            between two teams.
            """
            metric = st.selectbox("Select a metric for testing:", options=["vorp", "net", "bpm", "ORtg", "DRtg"])
            team1 = st.text_input("Enter the name of the first team:")
            team2 = st.text_input("Enter the name of the second team:")

            if st.button("Run Tests"):
                df1 = data[data['team'] == team1]
                df2 = data[data['team'] == team2]

                if not df1.empty and not df2.empty:
                    with st.spinner("Performing statistical tests..."):
                        results = two_sample(df1, df2, metric)  # Run tests
                    
                    st.write(f"Two-Sample T-Test Results for {metric}:")
                    st.json(results["t-test"])

                    st.write(f"Kolmogorov-Smirnov Test Results for {metric}:")
                    st.json(results["ks-test"])
                else:
                    st.error("One or both teams have no data.")

        elif analysis_option == "Subset by Player and Date":
            """
            Subsets data for a specific player and/or date range, displaying the filtered
            data in a table.
            """
            player_name = st.text_input("Enter the player's name:")
            date_range = st.date_input("Select date range:", [])

            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_data = subsetdates(data, start_date, end_date)  # Subset by date

                if player_name:
                    filtered_data = subsetplayer(filtered_data, player_name)  # Subset by player

                if not filtered_data.empty:
                    st.success(f"Data subset for player {player_name} from {start_date} to {end_date}")
                    st.dataframe(filtered_data)
                else:
                    st.error("No data found for the specified player and date range.")
