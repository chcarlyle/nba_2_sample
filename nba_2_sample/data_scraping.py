import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# Function to scrape NBA game IDs and metadata
def scrape_nba_ids(year: int, month: str):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTP errors if any
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    rows = soup.select("table#schedule > tbody > tr")
    for row in rows:
        if row.get("class") and "thead" in row.get("class"):  # Skip non-game rows
            continue
        
        game = {
            "month": month,
            "date_game": row.select_one("th[data-stat='date_game']").get_text(strip=True) if row.select_one("th[data-stat='date_game']") else None,
            "id": row.select_one("th[data-stat='date_game']").get("csk") if row.select_one("th[data-stat='date_game']") else None,
            "visitor_team": row.select_one("td[data-stat='visitor_team_name']").get("csk") if row.select_one("td[data-stat='visitor_team_name']") else None,
            "visitor_points": row.select_one("td[data-stat='visitor_pts']").get_text(strip=True) if row.select_one("td[data-stat='visitor_pts']") else None,
            "home_team": row.select_one("td[data-stat='home_team_name']").get("csk") if row.select_one("td[data-stat='home_team_name']") else None,
            "home_points": row.select_one("td[data-stat='home_pts']").get_text(strip=True) if row.select_one("td[data-stat='home_pts']") else None,
        }
        games.append(game)
        time.sleep(2)

    return pd.DataFrame(games)


# Function to scrape advanced box scores for a game
def scrape_advanced(game_id: str, home_team: str, visitor_team: str):
    url = f"https://www.basketball-reference.com/boxscores/{game_id}.html"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTP errors if any
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

    soup = BeautifulSoup(response.text, "html.parser")

    home_abbr = home_team[:3]
    visitor_abbr = visitor_team[:3]

    boxes = []

    # Scrape home team stats
    rowsh = soup.select(f"table#box-{home_abbr}-game-advanced > tbody > tr")
    for row in rowsh:
        if row.get("class") and "thead" in row.get("class"):  # Skip non-player rows
            continue
        
        boxh = {
            "team": home_abbr,
            "player": row.select_one("th[data-stat='player']").get("data-append-csv") if row.select_one("th[data-stat='player']") else None,
            "mp": row.select_one("td[data-stat='mp']").get("csk") if row.select_one("td[data-stat='mp']") else None,
            "ORtg": row.select_one("td[data-stat='off_rtg']").get_text(strip=True) if row.select_one("td[data-stat='off_rtg']") else None,
            "DRtg": row.select_one("td[data-stat='def_rtg']").get_text(strip=True) if row.select_one("td[data-stat='def_rtg']") else None,
            "bpm": row.select_one("td[data-stat='bpm']").get_text(strip=True) if row.select_one("td[data-stat='bpm']") else None,
        }
        boxes.append(boxh)

    # Scrape visitor team stats
    rowsv = soup.select(f"table#box-{visitor_abbr}-game-advanced > tbody > tr")
    for row in rowsv:
        if row.get("class") and "thead" in row.get("class"):  # Skip non-player rows
            continue
        
        boxv = {
            "team": visitor_abbr,
            "player": row.select_one("th[data-stat='player']").get("data-append-csv") if row.select_one("th[data-stat='player']") else None,
            "mp": row.select_one("td[data-stat='mp']").get("csk") if row.select_one("td[data-stat='mp']") else None,
            "ORtg": row.select_one("td[data-stat='off_rtg']").get_text(strip=True) if row.select_one("td[data-stat='off_rtg']") else None,
            "DRtg": row.select_one("td[data-stat='def_rtg']").get_text(strip=True) if row.select_one("td[data-stat='def_rtg']") else None,
            "bpm": row.select_one("td[data-stat='bpm']").get_text(strip=True) if row.select_one("td[data-stat='bpm']") else None,
        }
        boxes.append(boxv)

    return pd.DataFrame(boxes)

def scrape_month(df_games):
    all_box_scores = []

    for _, game in df_games.iterrows():
        game_id = game.get("id")
        home_team = game.get("home_team")
        visitor_team = game.get("visitor_team")

        if not game_id or not home_team or not visitor_team:
            print(f"Skipping game with missing data: {game}")
            continue

        print(f"Scraping game {game_id} ({home_team} vs {visitor_team})...")
        box_scores = scrape_advanced(game_id, home_team, visitor_team)
        
        if not box_scores.empty:
            box_scores["game_id"] = game_id  # Add game ID for tracking
            all_box_scores.append(box_scores)

        time.sleep(2)  # Respectful scraping delay

    # Combine all box scores into a single DataFrame
    if all_box_scores:
        return pd.concat(all_box_scores, ignore_index=True)
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data was scraped


# Main function
def main():
    year = 2024
    month = "october"
    game_data = scrape_nba_ids(year, month)
    print(game_data)

    if not game_data.empty:
        advanced_stats = scrape_month(game_data)
        print(advanced_stats)


if __name__ == "__main__":
    main()