from pathlib import Path
import json
from datetime import datetime, timedelta
import html


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "contributions.json"
OUTPUT_FILE = ROOT / "contrib-heatmap.svg"


# ============================================================
# SVG SETTINGS
# ============================================================

CELL_SIZE = 14
CELL_GAP = 4

CELL_RADIUS = 3

LEFT_LABEL = 38
TOP_LABEL = 32

BOTTOM_SPACE = 42

TEXT_COLOR = "#8b949e"
COUNT_COLOR = "#c9d1d9"

FONT = (
    "'Cascadia Code', "
    "'Cascadia Mono', "
    "'Consolas', "
    "'Courier New', "
    "monospace"
)


# GitHub-like contribution colors

COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not DATA_FILE.exists():

        print(
            f"ERROR: Contribution file not found:\n"
            f"{DATA_FILE}"
        )

        return None

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception as error:

        print("ERROR: Could not read contributions.json")
        print(error)

        return None

    contributions = data.get(
        "contributions",
        []
    )

    if not contributions:

        print("ERROR: No contribution data found.")

        return None

    return data


# ============================================================
# LEVEL CALCULATION
# ============================================================

def get_level(count, maximum):

    if count <= 0:
        return 0

    if maximum <= 0:
        return 0

    ratio = count / maximum

    if ratio <= 0.25:
        return 1

    if ratio <= 0.50:
        return 2

    if ratio <= 0.75:
        return 3

    return 4


# ============================================================
# BUILD WEEKS
# ============================================================

def build_calendar(contributions):

    days = []

    for item in contributions:

        try:

            date = datetime.strptime(
                item["date"],
                "%Y-%m-%d"
            ).date()

            count = int(
                item.get("count", 0)
            )

            days.append(
                {
                    "date": date,
                    "count": max(0, count)
                }
            )

        except Exception:
            continue

    if not days:
        return [], 0

    days.sort(
        key=lambda x: x["date"]
    )

    maximum = max(
        day["count"]
        for day in days
    )

    # --------------------------------------------------------
    # Start on Sunday.
    # --------------------------------------------------------

    first_date = days[0]["date"]

    start = (
        first_date
        - timedelta(
            days=(first_date.weekday() + 1) % 7
        )
    )

    # --------------------------------------------------------
    # End on Saturday.
    # --------------------------------------------------------

    last_date = days[-1]["date"]

    end = (
        last_date
        + timedelta(
            days=6 - (
                (last_date.weekday() + 1) % 7
            )
        )
    )

    # --------------------------------------------------------
    # Create dictionary.
    # --------------------------------------------------------

    lookup = {
        day["date"]: day["count"]
        for day in days
    }

    weeks = []

    current = start

    while current <= end:

        week = []

        for row in range(7):

            date = current + timedelta(
                days=row
            )

            count = lookup.get(
                date,
                0
            )

            week.append(
                {
                    "date": date,
                    "count": count
                }
            )

        weeks.append(week)

        current += timedelta(days=7)

    return weeks, maximum


# ============================================================
# MONTH LABELS
# ============================================================

def build_month_labels(
    weeks,
    x_start
):

    labels = []

    previous_month = None

    for index, week in enumerate(weeks):

        # Check the first day of each week.
        date = week[0]["date"]

        month = date.month

        if month != previous_month:

            labels.append(
                {
                    "name": date.strftime("%b"),
                    "x": x_start
                    + index
                    * (
                        CELL_SIZE
                        + CELL_GAP
                    )
                }
            )

            previous_month = month

    return labels


# ============================================================
# SVG
# ============================================================

def create_svg(
    data,
    weeks,
    maximum
):

    username = data.get(
        "username",
        "lokanathmeher19"
    )

    total = data.get(
        "total_contributions",
        0
    )

    columns = len(weeks)

    grid_width = (
        columns
        * (CELL_SIZE + CELL_GAP)
        - CELL_GAP
    )

    grid_height = (
        7
        * (CELL_SIZE + CELL_GAP)
        - CELL_GAP
    )

    width = (
        LEFT_LABEL
        + grid_width
        + 10
    )

    height = (
        TOP_LABEL
        + grid_height
        + BOTTOM_SPACE
    )

    x_start = LEFT_LABEL

    y_start = TOP_LABEL

    svg = []

    svg.append(
        '<?xml version="1.0" encoding="UTF-8"?>'
    )

    svg.append(
        f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}"
    role="img"
    aria-label="{html.escape(username)} GitHub contribution heatmap"
>
'''
    )

    # --------------------------------------------------------
    # CSS
    # --------------------------------------------------------

    svg.append(
        f'''
<style>

.month {{
    font-family: {FONT};
    font-size: 11px;
    fill: {TEXT_COLOR};
}}

.day {{
    font-family: {FONT};
    font-size: 11px;
    fill: {TEXT_COLOR};
}}

.count {{
    font-family: {FONT};
    font-size: 13px;
    font-weight: 700;
    fill: {COUNT_COLOR};
}}

.cell {{
    stroke: none;
}}

</style>
'''
    )

    # --------------------------------------------------------
    # Month labels
    # --------------------------------------------------------

    month_labels = build_month_labels(
        weeks,
        x_start
    )

    for month in month_labels:

        svg.append(
            f'''
<text
    x="{month["x"]}"
    y="14"
    class="month"
>
    {html.escape(month["name"])}
</text>
'''
        )

    # --------------------------------------------------------
    # Day labels
    # --------------------------------------------------------

    day_names = {
        1: "Mon",
        3: "Wed",
        5: "Fri"
    }

    for row, name in day_names.items():

        y = (
            y_start
            + row
            * (
                CELL_SIZE
                + CELL_GAP
            )
            + CELL_SIZE
            - 2
        )

        svg.append(
            f'''
<text
    x="0"
    y="{y}"
    class="day"
>
    {name}
</text>
'''
        )

    # --------------------------------------------------------
    # Contribution cells
    # --------------------------------------------------------

    for column, week in enumerate(weeks):

        x = (
            x_start
            + column
            * (
                CELL_SIZE
                + CELL_GAP
            )
        )

        for row, day in enumerate(week):

            y = (
                y_start
                + row
                * (
                    CELL_SIZE
                    + CELL_GAP
                )
            )

            count = day["count"]

            level = get_level(
                count,
                maximum
            )

            color = COLORS[level]

            date_text = day[
                "date"
            ].strftime(
                "%Y-%m-%d"
            )

            svg.append(
                f'''
<rect
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="{CELL_RADIUS}"
    fill="{color}"
    class="cell"
>
    <title>
        {html.escape(date_text)}: {count} contributions
    </title>
</rect>
'''
            )

    # --------------------------------------------------------
    # Total contributions
    # --------------------------------------------------------

    total_y = (
        y_start
        + grid_height
        + 30
    )

    svg.append(
        f'''
<text
    x="{x_start}"
    y="{total_y}"
    class="count"
>
    {total:,} contributions in the last year
</text>
'''
    )

    # --------------------------------------------------------
    # Close SVG
    # --------------------------------------------------------

    svg.append(
        "</svg>"
    )

    return "\n".join(svg)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("==========================================")
    print(" GitHub Contribution Renderer")
    print("==========================================")
    print()

    data = load_data()

    if data is None:
        return

    username = data.get(
        "username",
        "lokanathmeher19"
    )

    print(
        f"Loading real data for @{username}..."
    )

    weeks, maximum = build_calendar(
        data["contributions"]
    )

    if not weeks:

        print(
            "ERROR: Could not build contribution calendar."
        )

        return

    svg = create_svg(
        data,
        weeks,
        maximum
    )

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("SUCCESS!")
    print()
    print(
        f"Username: {username}"
    )

    print(
        f"Contributions: "
        f"{data.get('total_contributions', 0):,}"
    )

    print(
        f"Weeks rendered: {len(weeks)}"
    )

    print()
    print(
        f"Output:"
    )

    print(
        OUTPUT_FILE
    )

    print()
    print(
        "Background: TRANSPARENT"
    )

    print(
        "Border: NONE"
    )

    print(
        "Terminal frame: NONE"
    )

    print()


if __name__ == "__main__":
    main()