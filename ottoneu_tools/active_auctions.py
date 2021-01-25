# get date and league through argv or argparse
# get auctions started and players cut from that day
# get ottoneu data: last 10 auctions and maybe roster %
# using pybaseball, scrape statcast info
# v2: scrape RoS steamer / zips projections
# format data into email and send
import requests
from bs4 import BeautifulSoup
from pybaseball import statcast_batter, playerid_lookup, statcast_pitcher, cache

league_id = "953"  # put this in env
base_url = "https://ottoneu.fangraphs.com"
auction_url = f"{base_url}/{league_id}/transactions"
resp = requests.get(auction_url)
soup = BeautifulSoup(resp.content, "html.parser")
table = soup.find("table")
thead = [th.get_text() for th in table.find("thead").find_all("th")]
trows = [
    [td.get_text().strip() for td in tr.find_all("td")]
    for tr in table.find("tbody").find_all("tr")
]
# want row and link in one list? if so, prob don't want to use list comps

# filter for correct transaction type and only current transactions
#  get player name and take link to player page
# then use lookup to get player data
# append this link to the main url?
print([a["href"] for a in trows[0].find_all("a") if "playercard" in a["href"]])


# get names via lookup. use cache.enable() for pybaseball here?
# get statcast data for individual players or for league and then search for players?

# will need to clean names and remove jr, sr, etc
def get_ottoneu_avg_salary(player_id, lg_id=league_id):
    player_url = f"{base_url}/{lg_id}/playercard"
    player_resp = requests.get(player_url, params={"id": player_id})
    player_soup = BeautifulSoup(player_resp.content, "html.parser")
    salary_info = (
        player_soup.find("header", {"class": "page-header"})
        .find("div", {"class": "page-header__secondary"})
        .find_all("div")[1]
    )
    # all avg, all last 10, scoring specific all, scoring specific last 10
    # do find_all('em') to get those
    salary_info.find_all("a")
