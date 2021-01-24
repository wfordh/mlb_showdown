import argparse
import csv
from time import sleep

from tqdm import tqdm

from mlb_showdown_bot.showdown_player_card_generator import ShowdownPlayerCardGenerator
from mlb_showdown_bot.baseball_ref_scraper import BaseballReferenceScraper

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
    for player in tqdm(player_data):
        sleep(0.5)
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
        player_card["icons"] = showdown.icons
        if showdown.is_pitcher:
            pitcher_list.append(player_card)
        else:
            hitter_list.append(player_card)

    with open("pitcher_cards.csv", "w", encoding="utf-8-sig") as pitcher_file:
        pitcher_fieldnames = list(pitcher_list[0].keys())
        writer = csv.DictWriter(pitcher_file, pitcher_fieldnames)
        writer.writeheader()
        for row in pitcher_list:
            writer.writerow(row)

    with open("hitter_cards.csv", "w", encoding="utf-8-sig") as hitter_file:
        hitter_fieldnames = list(hitter_list[0].keys())
        writer = csv.DictWriter(hitter_file, hitter_fieldnames)
        writer.writeheader()
        for row in hitter_list:
            writer.writerow(row)


if __name__ == "__main__":
    main()
