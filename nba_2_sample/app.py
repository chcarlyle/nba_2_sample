import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ks_2samp

# Import functions from the repository
from data_scraping import scrape_nba_ids, scrape_month
from data_cleaning import clean_data, generate_vorp, generate_net
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
game_data = None
cleaned_data = None

# Scrape Data
if option == "Scrape Data":
    st.title("Scrape NBA Game Data")
    year = st.number_input("Enter the year:", min_value=2000, max_value=2025, step=1, value=2024)
    month = st.text_input("Enter the month (e.g., 'october'):", value="october")

    if st.button("Scrape Data"):
        with st.spinner("Scraping game data..."):
            game_data = scrape_nba_ids(year, month)
        
        if not game_data.empty:
            st.success("Game data scraped successfully!")
            st.dataframe(game_data)

            if st.button("Scrape Advanced Stats"):
                with st.spinner("Scraping advanced stats for games..."):
                    advanced_data = scrape_month(game_data)
                if not advanced_data.empty:
                    st.success("Advanced stats scraped successfully!")
                    st.dataframe(advanced_data)
                else:
                    st.error("Failed to scrape advanced stats.")
        else:
            st.error("No game data found for the specified month and year.")

# Clean Data
elif option == "Clean Data":
    st.title("Clean and Process Data")
    uploaded_file = st.file_uploader("Upload a CSV file of scraped data:", type="csv")

    if uploaded_file is not None:
        raw_data = pd.read_csv(uploaded_file)
        st.write("Raw Data:")
        st.dataframe(raw_data)

        with st.spinner("Cleaning data..."):
            cleaned_data = clean_data(raw_data)
            cleaned_data = generate_vorp(cleaned_data)
            cleaned_data = generate_net(cleaned_data)

        st.success("Data cleaned successfully!")
        st.write("Cleaned Data:")
        st.dataframe(cleaned_data)

        if st.button("Download Cleaned Data"):
            csv = cleaned_data.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download as CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

# Analyze Data
elif option == "Analyze Data":
    st.title("Analyze and Visualize Data")
    uploaded_file = st.file_uploader("Upload a CSV file of cleaned data:", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Cleaned Data:")
        st.dataframe(data)

        analysis_option = st.selectbox("Select an analysis option:", [
            "Density Plot",
            "Two-Sample Test",
        ])

        if analysis_option == "Density Plot":
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
            metric = st.selectbox("Select a metric for testing:", options=["vorp", "net", "bpm", "ORtg", "DRtg"])
            team1 = st.text_input("Enter the name of the first team:")
            team2 = st.text_input("Enter the name of the second team:")

            if st.button("Run Tests"):
                df1 = data[data['team'] == team1]
                df2 = data[data['team'] == team2]

                if not df1.empty and not df2.empty:
                    with st.spinner("Performing statistical tests..."):
                        results = two_sample(df1, df2, metric)
                    
                    st.write(f"Two-Sample T-Test Results for {metric}:")
                    st.json(results["t-test"])

                    st.write(f"Kolmogorov-Smirnov Test Results for {metric}:")
                    st.json(results["ks-test"])
                else:
                    st.error("One or both teams have no data.")
