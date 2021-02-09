import re
from time import sleep
import requests
from bs4 import BeautifulSoup

def get_ottoneu_player_page(player_id, lg_id):
    sleep(1.1)
    player_page_dict = dict()
    url = f"https://ottoneu.fangraphs.com/{lg_id}/playercard"
    r = requests.get(url, params={"id": player_id})
    soup = BeautifulSoup(r.content, "html.parser")
    header_data = soup.find("main").find("header", {"class": "page-header"})
    level_data = (
        header_data.find("div", {"class": "page-header__section--split"})
        .find("span", {"class": "strong tinytext"})
        .get_text()
    )
    if "(" in level_data or len(level_data.split()) == 2:
        player_page_dict["is_mlb"] = False
    else:
        player_page_dict["is_mlb"] = True
    # player_page_dict["is_mlb"] = False if "(" in level_data else True
    salary_data = header_data.find("div", {"class": "page-header__secondary"})
    player_page_dict["positions"] = (
        salary_data.find("div", {"class": "page-header__section--split"})
        .find("p")
        .get_text()
        .strip()
        .rsplit(maxsplit=1)[1]
    )
    salary_tags = [tag.get_text() for tag in salary_data.find_all("em")]
    salary_nums = [num.get_text() for num in salary_data.find_all("a")]

    for idx, (tag, num) in enumerate(zip(salary_tags, salary_nums)):
        if idx % 2 == 0:
            scoring_type = tag
            player_page_dict[tag] = num
        else:
            player_page_dict[f"{tag} - {scoring_type}"] = num
    return player_page_dict


def clean_name(player_name):
    name_suffixes = ("jr", "sr", "ii", "iii", "iv", "v")
    # might not want this at all for MLB names
    player_name = re.sub(r"(['])", "", player_name.lower())
    player_name = (
        player_name.rsplit(maxsplit=1)[0]
        if player_name.endswith(name_suffixes)
        else player_name
    )
    return player_name


def get_position_group(positions):
    # turn this into a dict?
    is_hitter = False
    is_pitcher = False
    if "/" in positions:
        if all(["P" in pos for pos in positions.split("/")]):
            is_pitcher = True
        elif any(["P" in pos for pos in positions.split("/")]):
            is_pitcher = True
            is_hitter = True
        else:
            is_hitter = True
    else:
        if "P" in positions:
            is_pitcher = True
        else:
            is_hitter = True
    return is_hitter, is_pitcher