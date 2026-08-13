from pathlib import Path
from datetime import datetime
import json
import re

import requests
from bs4 import BeautifulSoup


# ============================================================
# SETTINGS
# ============================================================

USERNAME = "lokanathmeher19"

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

OUTPUT = DATA_DIR / "contributions.json"

URL = f"https://github.com/users/{USERNAME}/contributions"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


# ============================================================
# FETCH GITHUB PAGE
# ============================================================

def fetch_page():

    print()
    print("==============================================")
    print("FETCHING GITHUB CONTRIBUTIONS")
    print("==============================================")
    print()

    print(f"Username : {USERNAME}")
    print(f"URL      : {URL}")
    print()

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    print(
        f"HTTP     : {response.status_code}"
    )

    return response.text


# ============================================================
# PARSE CONTRIBUTION CELLS
# ============================================================

def parse_contributions(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    cells = soup.select(
        "td.ContributionCalendar-day"
    )

    print(
        f"Calendar cells found : {len(cells)}"
    )

    if not cells:

        # Newer GitHub markup can use
        # contribution calendar day elements.

        cells = soup.select(
            "[data-date][data-level]"
        )

        print(
            f"Fallback cells found : {len(cells)}"
        )

    contributions = []

    for cell in cells:

        date_text = cell.get(
            "data-date"
        )

        level_text = cell.get(
            "data-level"
        )

        if not date_text:
            continue

        # ----------------------------------------------------
        # Contribution count
        # ----------------------------------------------------

        count = 0

        text = cell.get_text(
            " ",
            strip=True
        )

        # Example:
        #
        # "5 contributions on March 20th."
        #
        # or
        #
        # "No contributions on March 20th."

        match = re.search(
            r"(\d[\d,]*)\s+contribution",
            text,
            re.IGNORECASE
        )

        if match:

            count = int(
                match.group(1)
                .replace(",", "")
            )

        # ----------------------------------------------------
        # Level
        # ----------------------------------------------------

        try:

            level = int(
                level_text
            )

        except (
            TypeError,
            ValueError
        ):

            level = 0

        contributions.append(
            {
                "date": date_text,
                "count": count,
                "level": level
            }
        )

    # --------------------------------------------------------
    # Remove duplicate dates
    # --------------------------------------------------------

    unique = {}

    for item in contributions:

        unique[
            item["date"]
        ] = item

    contributions = list(
        unique.values()
    )

    # --------------------------------------------------------
    # Sort by date
    # --------------------------------------------------------

    contributions.sort(
        key=lambda x: x["date"]
    )

    return contributions


# ============================================================
# TOTAL
# ============================================================

def calculate_total(contributions):

    return sum(
        item["count"]
        for item in contributions
    )


# ============================================================
# SAVE JSON
# ============================================================

def save_data(
    contributions,
    total
):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "username": USERNAME,
        "generated_at": datetime.utcnow().isoformat()
        + "Z",
        "total": total,
        "days": contributions
    }

    OUTPUT.write_text(
        json.dumps(
            data,
            indent=2
        ),
        encoding="utf-8"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        html = fetch_page()

        contributions = parse_contributions(
            html
        )

        if not contributions:

            print()
            print(
                "ERROR: No contribution cells found."
            )
            print(
                "GitHub may have changed its HTML."
            )
            return

        total = calculate_total(
            contributions
        )

        save_data(
            contributions,
            total
        )

        print()
        print("==============================================")
        print("SUCCESS")
        print("==============================================")
        print()
        print(
            f"Days found : {len(contributions)}"
        )
        print(
            f"Total      : {total}"
        )
        print(
            f"Output     : {OUTPUT}"
        )
        print()

        # Show latest 10 days

        print("Latest contribution data:")
        print("----------------------------------------------")

        for item in contributions[-10:]:

            print(
                f"{item['date']}  "
                f"count={item['count']}  "
                f"level={item['level']}"
            )

        print()

    except requests.RequestException as error:

        print()
        print("ERROR: GitHub request failed.")
        print(error)
        print()

    except Exception as error:

        print()
        print("ERROR:")
        print(error)
        print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()