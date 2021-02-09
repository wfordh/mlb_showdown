# get date and league through argv or argparse
# get auctions started and players cut from that day
# using pybaseball, scrape statcast info
# v2: scrape RoS steamer / zips projections
# format data into email and send
import requests
from bs4 import BeautifulSoup
from pybaseball import (
    statcast_batter_exitvelo_barrels,
    playerid_lookup,
    statcast_pitcher,
    cache,
)
from tqdm import tqdm
from auction_utils import clean_name, get_ottoneu_player_page, get_position_group


def main():
    league_id = "953"  # put this in env
    base_url = "https://ottoneu.fangraphs.com"
    current_year = 2020
    auction_url = f"{base_url}/{league_id}/transactions"
    # for testing
    auction_url = "https://ottoneu.fangraphs.com/953/transactions?filters%5B%5D=cut&filters%5B%5D=increase"
    resp = requests.get(auction_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    table = soup.find("table")
    thead = [th.get_text() for th in table.find("thead").find_all("th")]

    auction_players = list()
    for tr in tqdm(table.find("tbody").find_all("tr")):
        player_data = [td.get_text().strip() for td in tr.find_all("td")]
        player_page_url = [
            a["href"] for a in tr.find_all("a") if "playercard" in a["href"]
        ].pop()
        player_dict = dict(zip(thead, player_data))
        if player_dict["Transaction Type"] != "add":
            continue
        player_dict["ottoneu_id"] = player_page_url.rsplit("=")[1]
        player_salary_dict = get_ottoneu_player_page(
            player_dict["ottoneu_id"], league_id
        )
        player_dict.update(player_salary_dict)

        player_name = clean_name(player_dict["Player Name"])
        first_name, last_name = player_name.split(maxsplit=1)

        if player_dict["is_mlb"]:
            if "." in first_name:
                # lookup has "A.J." as "A. J." for some reason
                first_name = first_name.replace(".", ". ").strip()
            id_lookup = playerid_lookup(last_name, first_name)
            if id_lookup.shape[0] > 1:
                player_dict["mlbam_id"] = id_lookup.loc[
                    id_lookup.mlb_played_last == id_lookup.mlb_played_last.max()
                ].key_mlbam.values[0]
            else:
                player_dict["mlbam_id"] = id_lookup.key_mlbam.values[0]

        is_hitter, is_pitcher = get_position_group(player_dict["positions"])
        player_dict["is_hitter"] = is_hitter
        player_dict["is_pitcher"] = is_pitcher

        auction_players.append(player_dict)

    hitters = [player for player in auction_players if player["is_hitter"]]
    pitchers = [player for player in auction_players if player["is_pitcher"]]
    if hitters:
        # setting minBBE = 0 to avoid not getting someone
        # get rid of this indentation and just pull exit velo #s regardless?
        exit_velo_data = statcast_batter_exitvelo_barrels(current_year, minBBE=0)
        for player in hitters:
            if not player["is_mlb"]:
                # avoid index error for minor leaguers
                continue
            player_exit_velo = (
                exit_velo_data.loc[exit_velo_data.player_id == player["mlbam_id"]]
                .to_dict("records")
                .pop()
            )
            # add anything else?
            player["avg_exit_velo"] = player_exit_velo["avg_hit_speed"]
            player["max_exit_velo"] = player_exit_velo["max_hit_speed"]
            player["barrel_pa_rate"] = player_exit_velo["brl_pa"]
            player["barrel_bbe_rate"] = player_exit_velo["brl_percent"]

    if pitchers:
        # currently pybaseball only has individual pitcher data
        pass

    print(auction_players[0])

    # get names via lookup. use cache.enable() for pybaseball here?
    # get statcast data for individual players or for league and then search for players?



if __name__ == "__main__":
    main()
