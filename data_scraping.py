import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Example function to scrape NBA game data
def scrape_nba_data(year: int, month: str):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    games = []
    rows = soup.select("table#schedule > tbody > tr")
    for row in rows:
        game = {
            "date_game": row.select_one("th[data-stat='date_game']").get_text() if row.select_one("th[data-stat='date_game']") else None,
            "vname": row.select_one("td[data-stat='visitor_team_name']").get_text() if row.select_one("td[data-stat='visitor_team_name']") else None,
            "vpts": row.select_one("td[data-stat='visitor_pts']").get_text() if row.select_one("td[data-stat='visitor_pts']") else None,
            "hname": row.select_one("td[data-stat='home_team_name']").get_text() if row.select_one("td[data-stat='home_team_name']") else None,
            "hpts": row.select_one("td[data-stat='home_pts']").get_text() if row.select_one("td[data-stat='home_pts']") else None
        }
        games.append(game)

    return pd.DataFrame(games)

# Main function to run as CLI
def main():
    year = 2024
    month = "october"
    data = scrape_nba_data(year, month)
    print(data)

    # Save or process the data further
    # data.to_csv(f"nba_{year}_{month}.csv", index=False)

if __name__ == "__main__":
    main()
