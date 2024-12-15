# NBA Player Performance Analysis

This repository contains Python scripts for scraping, cleaning, and analyzing NBA player performance data, focusing on advanced metrics like Box Plus-Minus (BPM), Offensive Rating (ORtg), and Defensive Rating (DRtg). The workflow enables you to compare regular-season and postseason performances and generate insights using statistical and visual methods.

## Repository Contents

### 1. Scripts

#### `data_scraping.py`
- **Purpose:** Scrape NBA game metadata and advanced box scores from Basketball Reference.
- **Key Functions:**
  - `scrape_nba_ids(year, month)`: Scrapes NBA game IDs, teams, scores, and dates for a specified year and month.
  - `scrape_advanced(game_id, home_team, visitor_team)`: Extracts advanced stats (e.g., BPM, ORtg, DRtg) for a single game.
  - `scrape_month(df_games)`: Scrapes advanced stats for all games in a DataFrame of game metadata.
- **Source:** Data is scraped from **https://www.basketball-reference.com/**

#### `data_cleaning.py`
- **Purpose:** Clean and preprocess scraped data for analysis.
- **Key Functions:**
  - `clean_data(df)`: Cleans raw data, converts columns to appropriate types, and handles missing values.
  - `generate_vorp(df)`: Calculates Value Over Replacement Player (VORP) for each player.
  - `generate_net(df)`: Calculates Net Rating (ORtg - DRtg) for players.
  - `compile_yearly_data(year, directory)`: Compiles data from monthly CSV files into a single DataFrame for a given year.
  - `subsetplayer(df, player)`: Filters data for a specific player.
  - `subsetdates(df, date1, date2)`: Filters data within a specified date range.

#### `analysis.py`
- **Purpose:** Analyze cleaned NBA performance data using statistical tests and visualization.
- **Key Functions:**
  - `average_vorp_by_team(df)`: Calculates average VORP for each team.
  - `player_average(df, player, metric)`: Computes the average of a specified metric for a given player.
  - `two_sample(df1, df2, metric)`: Performs a t-test and Kolmogorov-Smirnov test on a given metric between two datasets.
  - `plot_density(df, metric)`: Generates a density plot for a specified metric.

#### `app.py`
- **Purpose:** Provide a user interface to use the functions included in the other modules and view data frames easily

#### `Documentation`
- Documentation is hosted on github pages **https://chcarlyle.github.io/nba_2_sample/**
---

### 2. Example Workflow

1. **Scraping Data:**
   - Use `scrape_nba_ids` to gather game metadata for a specific month and year.
   - Pass the resulting DataFrame to `scrape_month` to collect advanced box scores.

2. **Cleaning Data:**
   - Use `clean_data` to preprocess the scraped data.
   - Generate derived metrics like VORP and Net Rating with `generate_vorp` and `generate_net`.

3. **Analyzing Data:**
   - Compare player or team performance using statistical tests with `two_sample`.
   - Visualize data distributions using `plot_density`.

---
### Installation

To install package, run:

```bash
pip install git+https://github.com/chcarlyle/nba_2_sample


### Requirements

- Python 3.8 or higher
- Required libraries:
  - `pandas`
  - `requests`
  - `bs4` (BeautifulSoup)
  - `scipy`
  - `matplotlib`
  - `seaborn`

To install dependencies, run:

```bash
pip install pandas requests beautifulsoup4 scipy matplotlib seaborn
