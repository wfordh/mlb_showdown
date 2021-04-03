import argparse
import csv
from time import sleep

from tqdm import tqdm

from mlb_showdown_bot.showdown_player_card_generator import ShowdownPlayerCardGenerator
from mlb_showdown_bot.baseball_ref_scraper import BaseballReferenceScraper
from showdown_tools import hitter_fieldnames, pitcher_fieldnames

parser = argparse.ArgumentParser(description="Player season information")
parser.add_argument(
    "-f",
    "--file",
    required=False,
    help="File name with list of player name, season combos separated by newlines",
)
parser.add_argument("-c", "--context", required=True, help="Showdown context")


def main():
    args = parser.parse_args()
    command_args = dict(vars(args))
    infile_path = command_args.pop("file", None)
    context = command_args.pop("context", None)
    with open(infile_path, "r") as infile:
        player_data = [l.strip() for l in infile.readlines()]

    pitcher_list = list()
    hitter_list = list()
    bad_players = list()
    for player in tqdm(player_data):
        sleep(0.7)
        try:
            name, year = player.split(",")
            scraper = BaseballReferenceScraper(name=name, year=year)
            statline = scraper.player_statline()
            showdown = ShowdownPlayerCardGenerator(
                name=name, year=year, stats=statline, context=context
            )
            player_card = showdown.chart_ranges
            player_card["name"] = showdown.name
            player_card["points"] = showdown.points
            player_card["year"] = showdown.year
            player_card["icons"] = None if showdown.icons == [] else showdown.icons
            if showdown.is_pitcher:
                player_card["command"] = showdown.chart["command"]
                pitcher_list.append(player_card)
            else:
                player_card["on_base"] = showdown.chart["command"]
                hitter_list.append(player_card)
        except:
            bad_players.append(player)

    with open(f"data/pitcher_cards_{context}.csv", "a", encoding="utf-8-sig") as pitcher_file:
        writer = csv.DictWriter(pitcher_file, pitcher_fieldnames)
        writer.writeheader()
        for row in pitcher_list:
            writer.writerow(row)

    with open(f"data/hitter_cards_{context}.csv", "a", encoding="utf-8-sig") as hitter_file:
        writer = csv.DictWriter(hitter_file, hitter_fieldnames)
        writer.writeheader()
        for row in hitter_list:
            writer.writerow(row)

    print(bad_players)


if __name__ == "__main__":
    main()
