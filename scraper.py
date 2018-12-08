"""Scrapes reviews of Magic the Gathering cards by LSV on Channel Fireball."""

import csv
import requests
from bs4 import BeautifulSoup as bs

# mtg api: https://docs.magicthegathering.io/#api_v1cards_list


def get_web_content(set_, color):
    """Get html content of set review for a given set and color.

    Args:
        set_(str): The name of the specified set.
        color(str): The name of the specified color.

    Returns:
        str: The contents of the HTML doc as a string

    """
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/70.0.3538.110 '
                       'Safari/537.36')
    }
    base_url = "https://www.channelfireball.com/articles/{set}-limited-set-review-{color}/"  # noqa: E501
    full_url = base_url.format(set=set_, color=color)
    r = requests.get(url=full_url, headers=headers)

    return r.content.decode()


def get_set_info():
    """Return set info as a list of dictionaries."""
    return [
        {
            "name": "dominaria",
            "colors": [
                "white",
                "blue",
                "black",
                "red",
                "green",
                "gold-artifacts-and-lands",
            ],
            "ignore_list": set([
                "Ratings Scale",
                "Top 5 White Commons",
                "Top 5 Blue Commons",
                "Top 5 Black Commons",
                "Top 5 Red Commons",
                "Top 5 Green Commons",
            ]),
        },
        {
            "name": "guilds-of-ravnica",
            "colors": [
                "white",
                "blue",
                "black",
                "red",
                "green",
                "boros",
                "dimir",
                "golgari",
                "selesnya",
                "izzet",
                "artifacts-lands-and-guild-ranking",
            ],
            "ignore_list": set([
                "Ratings Scale",
                "Previous Guilds of Ravnica Set Reviews",
                "Top 3 White Commons",
                "Top 3 Blue Commons",
                "Top 3 Black Commons",
                "Top 3 Red Commons",
                "Top 3 Green Commons",
                "Guild Rankings",
                "Most Important Boros Common",
                "Most Important Dimir Common",
                "Most Important Golgari Common",
                "Most Important Selesnya Common",
                "Most Important Izzet Common",
                "Boros",
                "Dimir",
                "Golgari",
                "Selesnya",
                "Izzet",
            ]),
        },
        {
            "name": "core-set-2019",
            "colors": [
                "white",
                "blue",
                "black",
                "red",
                "green",
                "gold-artifacts-and-lands",
            ],
            "ignore_list": set([
                "Ratings Scale",
                "Top 5 White Commons",
                "Top 5 Blue Commons",
                "Top 5 Black Commons",
                "Top 5 Red Commons",
                "Top 5 Green Commons",
                "Multicolored",
                "Artifacts",
                "Lands",
            ])
        },
    ]


def write_csv(set_, colors, ignore_list):
    """Write card review values to CSV file.

    Args:
        set_(str): Name of the set.
        colors(list): List of colors in the set.
        ignore_list(list): Names to be ignored.

    Returns:
        None

    """
    file_path = f"C:\\Users\\Patrick\\Desktop\\{set_}.csv"
    with open(file_path, "w", encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([
            "Card Name",
            "Main Rating",
            "Sup. Rating",
            "Color",
            "Notes",
        ])

        for color in colors:
            parser = bs(get_web_content(set_, color), 'html.parser')
            for card in parser.find_all('h1', class_=""):
                if card.text not in ignore_list:
                    name = card.text
                    ph = card.findNext('p').text
                    rating = card.findNext('h3').text.replace("Limited: ", "")

                    csv_writer.writerow([name, rating, color, ph])


def main():
    """Execute main loop."""
    for item in get_set_info():
        write_csv(item["name"], item["colors"], item["ignore_list"])


if __name__ == "__main__":
    main()
