#!/usr/bin/env python3

# stdlib
import re
import json
import time
import string
from collections import defaultdict

# 3rd party
import requests
from bs4 import BeautifulSoup

# Wikipedia URL to scrape data from
URL = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"

# Get the last 26 uppercase letters
LETTERS = string.ascii_letters[26:]

# Number of IATA Codes fetched
iata_codes = 0
# JSON Results object
json_results = defaultdict(dict)


def get_page(letter):
    return requests.get(f"{URL}_{letter}")


def replace_refs(strings):
    """Replaces [1] or [2] or any bracket[digit] combinations for either
    a list or strings or single string."""
    results = []
    if isinstance(strings, list):
        for i in range(len(strings)):
            strings[i] = re.sub("\[\d\]", "", strings[i])
        # Strip '[digit]' characters and return list of strings.
        return strings
    elif isinstance(strings, str):
        return re.sub("\[\d\]", "", string)


def append_data(row):
    """
    IATA | ICAO | Airport Name | Location Served | Time (UTC) | DST
    ['AZZ', 'FNAM', 'Ambriz Airport', 'Ambriz, Angola', 'UTC+01:00', '']
    """
    # Headers (DST shows when Daylight Savings Time begins and ends.
    headers = ["IATA", "ICAO", "Airport Name", "Location Served", "Time (UTC)", "DST"]

    # Replace any wikipedia string references in values '[\d]'
    row = replace_refs(row)
    # Use IATA code as the key
    key = row[0]
    if (key.startswith("-") and key.endswith("-")) or key == "IATA":
        # Certain rows will have an identifier like '-AB-' to indicate IATA codes
        # that begin with 'AB', for example. Additionally, ignore IATA header.
        return False
    else:
        # Save to JSON results object to write to file later.
        for h, r in zip(headers, row):
            json_results[key][h] = r
        return True


# Generation start time
start = time.time()
for letter in LETTERS:
    print(f"Generating IATA Data for codes that begin with '{letter}'")
    page = get_page(letter)
    # If page didnt return a successful status code, continue to next letter
    if not page.ok:
        continue
    soup = BeautifulSoup(page.text, "html.parser")

    # Search String - find the table object within the page, limit to all 'tr's
    table = soup.find("table", {"class": "wikitable"}).find("tbody").find_all("tr")

    for row in table:
        # We're removing first and last element (empty string) from a split string at '|'
        # after replacing all instances of '\n' with '|' in order to ascii-ify the table
        # EXAMPLE: Text of row after .strip()
        # '|AZZ|FNAM|Ambriz Airport|Ambriz, Angola|UTC+01:00||'
        row_data = [r for r in row.text.replace("\n", "|").strip().split("|")[1:-1]]
        if append_data(row_data):
            # Iterate list of generated IATA codes
            iata_codes += 1


print(f"Generated data about {iata_codes} IATA Codes in {time.time() - start}s")
# Write to iata file
with open("../iata.json", "w") as json_file:
    print(json.dumps(json_results), file=json_file)
