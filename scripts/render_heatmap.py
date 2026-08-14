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
# USER
# ============================================================

USERNAME = "lokanathmeher19"


# ============================================================
# SVG SETTINGS
# ============================================================

# Wide enough for the complete 53-week GitHub graph
SVG_WIDTH = 1200
SVG_HEIGHT = 330

LEFT = 55
TOP = 85

# Compact cells so every week is visible
CELL_SIZE = 16
CELL_GAP = 4

COLUMNS = 53
ROWS = 7

# Exact width of 53 columns
HEATMAP_WIDTH = (
    COLUMNS * CELL_SIZE
    + (COLUMNS - 1) * CELL_GAP
)

# Exact height of 7 rows
HEATMAP_HEIGHT = (
    ROWS * CELL_SIZE
    + (ROWS - 1) * CELL_GAP
)


# ============================================================
# COLORS
# ============================================================

TEXT_COLOR = "#8b949e"
TITLE_COLOR = "#c9d1d9"

LEVEL_COLORS = {
    "NONE": "#161b22",
    "FIRST_QUARTILE": "#0e4429",
    "SECOND_QUARTILE": "#006d32",
    "THIRD_QUARTILE": "#26a641",
    "FOURTH_QUARTILE": "#39d353",
}


# ============================================================
# ANIMATION
# ============================================================

# Complete animation repeats every 3 seconds
ANIMATION_CYCLE = 3.0

# Each row starts slightly after the previous row
ROW_DELAY = 0.08


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not DATA_FILE.exists():

        print("ERROR: contributions.json not found.")

        return None

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception as error:

        print(
            f"ERROR reading contributions.json: {error}"
        )

        return None

    return data


# ============================================================
# PARSE CONTRIBUTIONS
# ============================================================

def build_contribution_map(data):

    contribution_map = {}

    for item in data.get("contributions", []):

        date_string = item.get("date")

        if not date_string:
            continue

        try:

            date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            continue

        count = item.get("count", 0)

        try:

            count = int(count)

        except (ValueError, TypeError):

            count = 0

        level = item.get(
            "level",
            "NONE"
        )

        contribution_map[date] = {
            "count": count,
            "level": level
        }

    return contribution_map


# ============================================================
# COLOR
# ============================================================

def get_color(level, count):

    if level in LEVEL_COLORS:

        return LEVEL_COLORS[level]

    if count <= 0:

        return LEVEL_COLORS["NONE"]

    if count <= 3:

        return LEVEL_COLORS["FIRST_QUARTILE"]

    if count <= 6:

        return LEVEL_COLORS["SECOND_QUARTILE"]

    if count <= 9:

        return LEVEL_COLORS["THIRD_QUARTILE"]

    return LEVEL_COLORS["FOURTH_QUARTILE"]


# ============================================================
# FIND SUNDAY
# ============================================================

def sunday_on_or_before(date):

    days_since_sunday = (
        (date.weekday() + 1) % 7
    )

    return date - timedelta(
        days=days_since_sunday
    )


# ============================================================
# BUILD 53 × 7 GRID
# ============================================================

def build_grid(contribution_map):

    if not contribution_map:

        return [], None

    all_dates = sorted(
        contribution_map.keys()
    )

    first_date = all_dates[0]
    last_date = all_dates[-1]

    first_sunday = sunday_on_or_before(
        first_date
    )

    last_sunday = sunday_on_or_before(
        last_date
    )

    weeks = []

    current_sunday = first_sunday

    while (
        current_sunday <= last_sunday
        and len(weeks) < COLUMNS
    ):

        week = []

        for row in range(ROWS):

            date = (
                current_sunday
                + timedelta(days=row)
            )

            value = contribution_map.get(
                date,
                {
                    "count": 0,
                    "level": "NONE"
                }
            )

            week.append(
                {
                    "date": date,
                    "count": value["count"],
                    "level": value["level"]
                }
            )

        weeks.append(week)

        current_sunday += timedelta(
            days=7
        )

    # Make sure there are exactly 53 weeks
    while len(weeks) < COLUMNS:

        empty_week = []

        for row in range(ROWS):

            empty_week.append(
                {
                    "date": None,
                    "count": 0,
                    "level": "NONE"
                }
            )

        weeks.append(empty_week)

    return weeks[:COLUMNS], first_sunday


# ============================================================
# MONTH LABELS
# ============================================================

def build_month_labels(weeks):

    labels = []

    previous_month = None

    for column, week in enumerate(weeks):

        valid_dates = [
            item["date"]
            for item in week
            if item["date"] is not None
        ]

        if not valid_dates:
            continue

        date = valid_dates[0]

        month_key = (
            date.year,
            date.month
        )

        if month_key != previous_month:

            labels.append(
                {
                    "column": column,
                    "name": date.strftime("%b")
                }
            )

            previous_month = month_key

    return labels


# ============================================================
# SVG HEADER
# ============================================================

def svg_header(total_contributions):

    return f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
    preserveAspectRatio="xMidYMid meet"
    role="img"
    aria-label="GitHub contribution heatmap for {html.escape(USERNAME)}"
>

<style>

    .terminal {{
        font-family:
            "Cascadia Code",
            "Cascadia Mono",
            "Consolas",
            "Courier New",
            monospace;
    }}

    .command {{
        fill: {TITLE_COLOR};
        font-size: 18px;
        font-weight: 700;
    }}

    .month {{
        fill: {TEXT_COLOR};
        font-size: 12px;
        font-weight: 500;
    }}

    .weekday {{
        fill: {TEXT_COLOR};
        font-size: 12px;
        font-weight: 500;
    }}

    .total {{
        fill: {TITLE_COLOR};
        font-size: 17px;
        font-weight: 700;
    }}

    .legend {{
        fill: {TEXT_COLOR};
        font-size: 12px;
        font-weight: 500;
    }}

</style>


<!-- Terminal command -->

<text
    x="{SVG_WIDTH / 2}"
    y="35"
    text-anchor="middle"
    class="terminal command"
>
    {html.escape(USERNAME)}@github ~ $ ./contributions.sh
</text>

"""


# ============================================================
# MONTH LABELS
# ============================================================

def build_month_svg(weeks):

    parts = []

    labels = build_month_labels(
        weeks
    )

    for label in labels:

        x = (
            LEFT
            + label["column"]
            * (CELL_SIZE + CELL_GAP)
        )

        # Prevent last month label from going
        # outside the SVG.
        if x > SVG_WIDTH - 35:
            x = SVG_WIDTH - 35

        parts.append(
            f"""
<text
    x="{x}"
    y="63"
    class="terminal month"
>
    {html.escape(label["name"])}
</text>
"""
        )

    return "".join(parts)


# ============================================================
# WEEKDAY LABELS
# ============================================================

def build_weekday_svg():

    parts = []

    labels = {
        1: "Mon",
        3: "Wed",
        5: "Fri"
    }

    for row, label in labels.items():

        y = (
            TOP
            + row
            * (CELL_SIZE + CELL_GAP)
            + CELL_SIZE
            - 2
        )

        parts.append(
            f"""
<text
    x="0"
    y="{y}"
    class="terminal weekday"
>
    {label}
</text>
"""
        )

    return "".join(parts)


# ============================================================
# BUILD HEATMAP
# ============================================================

def build_heatmap_svg(weeks):

    parts = []

    for row in range(ROWS):

        clip_id = f"rowClip{row}"

        row_y = (
            TOP
            + row
            * (CELL_SIZE + CELL_GAP)
        )

        # Small delay for each row
        row_delay = row * ROW_DELAY

        parts.append(
            f"""
<clipPath id="{clip_id}">

    <rect
        x="{LEFT}"
        y="{row_y}"
        width="0"
        height="{CELL_SIZE + 2}"
    >

        <animate
            attributeName="width"
            values="0;{HEATMAP_WIDTH};{HEATMAP_WIDTH}"
            keyTimes="0;0.25;1"
            begin="{row_delay:.2f}s"
            dur="{ANIMATION_CYCLE:.2f}s"
            repeatCount="indefinite"
        />

    </rect>

</clipPath>
"""
        )

        parts.append(
            f"""
<g clip-path="url(#{clip_id})">
"""
        )

        for column in range(COLUMNS):

            item = weeks[column][row]

            count = item["count"]
            level = item["level"]

            color = get_color(
                level,
                count
            )

            x = (
                LEFT
                + column
                * (CELL_SIZE + CELL_GAP)
            )

            y = row_y

            date = item["date"]

            if date is None:

                date_text = ""

            else:

                date_text = (
                    f"{date.strftime('%Y-%m-%d')}"
                    f": {count} contributions"
                )

            safe_title = html.escape(
                date_text
            )

            parts.append(
                f"""
<rect
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="4"
    fill="{color}"
>
    <title>{safe_title}</title>
</rect>
"""
            )

        parts.append(
            """
</g>
"""
        )

    return "".join(parts)


# ============================================================
# TOTAL
# ============================================================

def build_total_svg(total):

    y = (
        TOP
        + HEATMAP_HEIGHT
        + 48
    )

    return f"""
<text
    x="{LEFT}"
    y="{y}"
    class="terminal total"
>
    {total:,} contributions in the last year
</text>
"""


# ============================================================
# LEGEND
# ============================================================

def build_legend_svg():

    y = (
        TOP
        + HEATMAP_HEIGHT
        + 43
    )

    start_x = SVG_WIDTH - 310

    parts = []

    parts.append(
        f"""
<text
    x="{start_x}"
    y="{y}"
    class="terminal legend"
>
    Less
</text>
"""
    )

    colors = [
        LEVEL_COLORS["NONE"],
        LEVEL_COLORS["FIRST_QUARTILE"],
        LEVEL_COLORS["SECOND_QUARTILE"],
        LEVEL_COLORS["THIRD_QUARTILE"],
        LEVEL_COLORS["FOURTH_QUARTILE"]
    ]

    for index, color in enumerate(colors):

        x = (
            start_x
            + 40
            + index * 25
        )

        parts.append(
            f"""
<rect
    x="{x}"
    y="{y - 13}"
    width="17"
    height="17"
    rx="4"
    fill="{color}"
/>
"""
        )

    parts.append(
        f"""
<text
    x="{start_x + 180}"
    y="{y}"
    class="terminal legend"
>
    More
</text>
"""
    )

    return "".join(parts)


# ============================================================
# FOOTER
# ============================================================

def build_footer():

    y = (
        TOP
        + HEATMAP_HEIGHT
        + 105
    )

    return f"""
<text
    x="{LEFT}"
    y="{y}"
    class="terminal legend"
>
    {html.escape(USERNAME)}@github ~ $
</text>
"""


# ============================================================
# GENERATE SVG
# ============================================================

def generate_svg(data):

    total = data.get(
        "total_contributions",
        0
    )

    contribution_map = (
        build_contribution_map(data)
    )

    weeks, first_sunday = build_grid(
        contribution_map
    )

    if not weeks:

        raise RuntimeError(
            "No contribution data found."
        )

    svg = []

    svg.append(
        svg_header(total)
    )

    svg.append(
        build_month_svg(weeks)
    )

    svg.append(
        build_weekday_svg()
    )

    svg.append(
        build_heatmap_svg(weeks)
    )

    svg.append(
        build_total_svg(total)
    )

    svg.append(
        build_legend_svg()
    )

    svg.append(
        build_footer()
    )

    svg.append(
        "\n</svg>\n"
    )

    return "".join(svg)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("==========================================")
    print(" GitHub Contribution Renderer")
    print("==========================================")
    print()

    print(
        f"Loading real data for @{USERNAME}..."
    )

    data = load_data()

    if data is None:
        return

    contribution_count = len(
        data.get(
            "contributions",
            []
        )
    )

    total = data.get(
        "total_contributions",
        0
    )

    print(
        f"Real contributions: {total}"
    )

    print(
        f"Days loaded: {contribution_count}"
    )

    try:

        svg = generate_svg(data)

    except Exception as error:

        print()
        print(
            f"ERROR: {error}"
        )

        return

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("SUCCESS!")
    print()
    print(
        f"Output: {OUTPUT_FILE}"
    )

    print(
        f"Canvas: {SVG_WIDTH} x {SVG_HEIGHT}"
    )

    print(
        f"Grid: {COLUMNS} weeks x {ROWS} days"
    )

    print(
        f"Heatmap width: {HEATMAP_WIDTH}px"
    )

    print(
        "Background: TRANSPARENT"
    )

    print(
        "Border: NONE"
    )

    print(
        "Data: REAL GITHUB DATA"
    )

    print(
        "Animation: REPEATING"
    )

    print(
        "Cycle: 3 seconds"
    )

    print(
        "Direction: LEFT → RIGHT"
    )

    print()


if __name__ == "__main__":

    main()