import os
import json
import requests
from datetime import datetime, timedelta, timezone


USERNAME = "lokanathmeher19"

TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not set")


API_URL = "https://api.github.com/graphql"


QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    login

    contributionsCollection(from: $from, to: $to) {
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


def fetch_contributions():

    print("=" * 50)
    print(" GitHub Contribution Fetcher")
    print("=" * 50)

    print()
    print(f"Username: {USERNAME}")
    print("Fetching REAL GitHub contribution data...")
    print()

    today = datetime.now(timezone.utc)

    start = today - timedelta(days=370)

    variables = {
        "login": USERNAME,
        "from": start.isoformat(),
        "to": today.isoformat(),
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        API_URL,
        json={
            "query": QUERY,
            "variables": variables,
        },
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        print("GitHub GraphQL error:")
        print(json.dumps(result["errors"], indent=2))
        raise RuntimeError("GitHub API request failed")

    user = result["data"]["user"]

    if user is None:
        raise RuntimeError(
            f"GitHub user '{USERNAME}' not found"
        )

    calendar = (
        user["contributionsCollection"]
        ["contributionCalendar"]
    )

    contributions = []

    for week in calendar["weeks"]:

        for day in week["contributionDays"]:

            contributions.append({
                "date": day["date"],
                "count": day["contributionCount"],
                "level": day["contributionLevel"],
            })

    data = {
        "username": USERNAME,
        "total_contributions":
            calendar["totalContributions"],
        "updated_at":
            datetime.now(timezone.utc).isoformat(),
        "contributions": contributions,
    }

    os.makedirs("data", exist_ok=True)

    output_file = "data/contributions.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2
        )

    print("SUCCESS!")
    print()
    print(f"Username: {USERNAME}")
    print(
        f"Real contributions: "
        f"{calendar['totalContributions']}"
    )
    print(
        f"Days downloaded: "
        f"{len(contributions)}"
    )
    print()
    print("Saved to:")
    print(os.path.abspath(output_file))


if __name__ == "__main__":
    fetch_contributions()