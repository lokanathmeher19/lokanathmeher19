from pathlib import Path
import json
import os
import sys
import requests


# ============================================================
# CONFIG
# ============================================================

USERNAME = "lokanathmeher19"

ROOT = Path(__file__).resolve().parent.parent

OUTPUT = ROOT / "data" / "contributions.json"

GITHUB_API = "https://api.github.com/graphql"


# ============================================================
# GRAPHQL QUERY
# ============================================================

QUERY = """
query($login: String!) {
  user(login: $login) {
    login

    contributionsCollection {
      contributionCalendar {
        totalContributions

        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""


# ============================================================
# MAIN
# ============================================================

def main():

    token = os.environ.get("GITHUB_TOKEN")

    if not token:

        print()
        print("ERROR: GITHUB_TOKEN is not set.")
        print()
        print("PowerShell:")
        print('$env:GITHUB_TOKEN="YOUR_GITHUB_TOKEN"')
        print()
        sys.exit(1)

    print()
    print("==========================================")
    print(" GitHub Contribution Fetcher")
    print("==========================================")
    print()

    print(f"Username: {USERNAME}")
    print("Fetching real GitHub contribution data...")
    print()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "query": QUERY,
        "variables": {
            "login": USERNAME
        }
    }

    response = requests.post(
        GITHUB_API,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:

        print(
            f"ERROR: GitHub API returned HTTP {response.status_code}"
        )

        print(response.text)

        sys.exit(1)

    result = response.json()

    if "errors" in result:

        print("ERROR: GitHub GraphQL API error:")

        for error in result["errors"]:
            print(
                error.get(
                    "message",
                    "Unknown error"
                )
            )

        sys.exit(1)

    user = result["data"]["user"]

    if user is None:

        print(
            f"ERROR: GitHub user '{USERNAME}' not found."
        )

        sys.exit(1)

    calendar = (
        user[
            "contributionsCollection"
        ][
            "contributionCalendar"
        ]
    )

    total = calendar["totalContributions"]

    # --------------------------------------------------------
    # Flatten GitHub calendar
    # --------------------------------------------------------

    contributions = []

    for week in calendar["weeks"]:

        for day in week["contributionDays"]:

            contributions.append(
                {
                    "date": day["date"],
                    "count": day["contributionCount"],
                    "level": day["contributionLevel"],
                }
            )

    # --------------------------------------------------------
    # Save data
    # --------------------------------------------------------

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_data = {
        "username": USERNAME,
        "total_contributions": total,
        "contributions": contributions
    }

    OUTPUT.write_text(
        json.dumps(
            output_data,
            indent=2
        ),
        encoding="utf-8"
    )

    print("SUCCESS!")
    print()
    print(f"Username: {USERNAME}")
    print(f"Real contributions: {total}")
    print(f"Days downloaded: {len(contributions)}")
    print()
    print(f"Saved to:")
    print(OUTPUT)
    print()


if __name__ == "__main__":
    main()