from pathlib import Path
from datetime import datetime
import json
import html


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "contributions.json"
OUTPUT_FILE = ROOT / "contrib-heatmap.svg"


# ============================================================
# SVG SIZE
# ============================================================

SVG_WIDTH = 860
SVG_HEIGHT = 220


# ============================================================
# HEATMAP SETTINGS
# ============================================================

WEEKS = 53
DAYS = 7

CELL_SIZE = 14
CELL_GAP = 3

GRID_WIDTH = WEEKS * (CELL_SIZE + CELL_GAP) - CELL_GAP
GRID_HEIGHT = DAYS * (CELL_SIZE + CELL_GAP) - CELL_GAP


# ============================================================
# COLORS
# ============================================================

# GitHub-like contribution colors
PALETTE = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
]


TEXT_COLOR = "#c9d1d9"
MUTED_COLOR = "#8b949e"

TERMINAL_BG = "#0d1117"


# ============================================================
# POSITIONING
# ============================================================

LABEL_WIDTH = 32

GRID_X = 32 + LABEL_WIDTH
GRID_Y = 72

HEADER_Y = 38

MONTH_Y = 58

FOOTER_Y = 207


# ============================================================
# ANIMATION
# ============================================================

# Smaller = faster
ANIMATION_DELAY = 0.003

# Duration of each square animation
ANIMATION_DURATION = 0.08


# ============================================================
# HELPERS
# ============================================================

def safe_int(value):
    try:
        return int(value)
    except Exception:
        return 0


def get_level(count):
    """
    Convert contribution count into GitHub-style level.
    """

    count = safe_int(count)

    if count <= 0:
        return 0

    if count <= 2:
        return 1

    if count <= 5:
        return 2

    if count <= 10:
        return 3

    return 4


def load_contributions():
    """
    Load contribution data.

    Expected format:

    {
        "days": [
            {
                "date": "2026-08-13",
                "count": 5
            }
        ]
    }

    Also supports a plain list.
    """

    if not DATA_FILE.exists():
        print(f"ERROR: Data file not found:")
        print(DATA_FILE)
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except Exception as error:
        print("ERROR: Could not read contributions.json")
        print(error)
        return []

    if isinstance(data, dict):
        days = data.get("days", [])

        if not days:
            days = data.get("contributions", [])

    elif isinstance(data, list):
        days = data

    else:
        days = []

    return days


# ============================================================
# BUILD CONTRIBUTION MAP
# ============================================================

def build_contribution_map(days):

    contribution_map = {}

    for item in days:

        if not isinstance(item, dict):
            continue

        date_value = (
            item.get("date")
            or item.get("day")
        )

        count = (
            item.get("count")
            if "count" in item
            else item.get("contributions", 0)
        )

        if not date_value:
            continue

        try:
            date_value = str(date_value)

            # Validate date
            datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )

        except Exception:
            continue

        contribution_map[date_value] = safe_int(count)

    return contribution_map


# ============================================================
# GET LAST 53 WEEKS
# ============================================================

def build_grid(contribution_map):

    today = datetime.now().date()

    # Find Sunday of current week
    sunday = today

    while sunday.weekday() != 6:
        from datetime import timedelta
        sunday -= timedelta(days=1)

    from datetime import timedelta

    # Start 52 weeks before current week
    start_date = sunday - timedelta(
        weeks=WEEKS - 1
    )

    grid = []

    for week in range(WEEKS):

        column = []

        for day in range(DAYS):

            current_date = (
                start_date
                + timedelta(
                    weeks=week,
                    days=day
                )
            )

            date_string = current_date.isoformat()

            count = contribution_map.get(
                date_string,
                0
            )

            column.append(
                {
                    "date": date_string,
                    "count": count,
                    "level": get_level(count)
                }
            )

        grid.append(column)

    return grid


# ============================================================
# MONTH LABELS
# ============================================================

def build_month_labels(grid):

    labels = []

    last_month = None

    for week_index, column in enumerate(grid):

        if not column:
            continue

        date_string = column[0]["date"]

        try:
            date_obj = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            )

        except Exception:
            continue

        month = date_obj.strftime("%b")

        if month != last_month:

            labels.append(
                (
                    week_index,
                    month
                )
            )

            last_month = month

    return labels


# ============================================================
# MAIN SVG
# ============================================================

def create_svg():

    days = load_contributions()

    contribution_map = build_contribution_map(
        days
    )

    grid = build_grid(
        contribution_map
    )

    month_labels = build_month_labels(
        grid
    )

    # --------------------------------------------------------
    # TOTAL CONTRIBUTIONS
    # --------------------------------------------------------

    total_contributions = sum(
        item["count"]
        for column in grid
        for item in column
    )

    # --------------------------------------------------------
    # SVG ELEMENTS
    # --------------------------------------------------------

    svg_elements = []

    # ========================================================
    # TERMINAL HEADER
    # ========================================================

    command = "avi@github ~ $ ./contributions.sh"

    svg_elements.append(
        f"""
<text
    x="{SVG_WIDTH / 2}"
    y="{HEADER_Y}"
    text-anchor="middle"
    class="command"
>
    {html.escape(command)}
</text>
"""
    )

    # ========================================================
    # MONTH LABELS
    # ========================================================

    for week_index, month in month_labels:

        x = (
            GRID_X
            + week_index * (
                CELL_SIZE + CELL_GAP
            )
        )

        svg_elements.append(
            f"""
<text
    x="{x}"
    y="{MONTH_Y}"
    class="month"
>
    {html.escape(month)}
</text>
"""
        )

    # ========================================================
    # DAY LABELS
    # ========================================================

    day_labels = {
        0: "Mon",
        2: "Wed",
        4: "Fri",
    }

    for day_index, label in day_labels.items():

        y = (
            GRID_Y
            + day_index * (
                CELL_SIZE + CELL_GAP
            )
            + CELL_SIZE - 2
        )

        svg_elements.append(
            f"""
<text
    x="0"
    y="{y}"
    class="day"
>
    {label}
</text>
"""
        )

    # ========================================================
    # CONTRIBUTION CELLS
    # ========================================================

    animation_index = 0

    for week_index, column in enumerate(grid):

        for day_index, item in enumerate(column):

            x = (
                GRID_X
                + week_index * (
                    CELL_SIZE + CELL_GAP
                )
            )

            y = (
                GRID_Y
                + day_index * (
                    CELL_SIZE + CELL_GAP
                )
            )

            level = item["level"]

            fill = PALETTE[level]

            date_string = item["date"]
            count = item["count"]

            tooltip = (
                f"{count} contribution"
                if count == 1
                else f"{count} contributions"
            )

            tooltip += f" on {date_string}"

            # -----------------------------------------------
            # Animation
            # -----------------------------------------------

            delay = (
                animation_index
                * ANIMATION_DELAY
            )

            animation_index += 1

            cell_id = (
                f"cell-{week_index}-{day_index}"
            )

            svg_elements.append(
                f"""
<rect
    id="{cell_id}"
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="3"
    ry="3"
    fill="{fill}"
    opacity="0"
>
    <title>
        {html.escape(tooltip)}
    </title>

    <animate
        attributeName="opacity"
        from="0"
        to="1"
        begin="{delay:.3f}s"
        dur="{ANIMATION_DURATION}s"
        fill="freeze"
    />

</rect>
"""
            )

    # ========================================================
    # FOOTER
    # ========================================================

    footer = (
        f"{total_contributions:,} "
        "contributions in the last year"
    )

    svg_elements.append(
        f"""
<text
    x="{GRID_X}"
    y="{FOOTER_Y}"
    class="footer"
>
    {html.escape(footer)}
</text>
"""
    )

    # ========================================================
    # LEGEND
    # ========================================================

    legend_y = FOOTER_Y - 7

    legend_start_x = SVG_WIDTH - 145

    svg_elements.append(
        f"""
<text
    x="{legend_start_x - 35}"
    y="{legend_y}"
    class="legend-text"
>
    Less
</text>
"""
    )

    for index in range(5):

        x = (
            legend_start_x
            + index * (
                CELL_SIZE + 3
            )
        )

        svg_elements.append(
            f"""
<rect
    x="{x}"
    y="{legend_y - 11}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="3"
    ry="3"
    fill="{PALETTE[index]}"
/>
"""
        )

    svg_elements.append(
        f"""
<text
    x="{legend_start_x + 5 * 17}"
    y="{legend_y}"
    class="legend-text"
>
    More
</text>
"""
    )

    # ========================================================
    # FINAL SVG
    # ========================================================

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
>

<style>

.command {{
    font-family:
        "SFMono-Regular",
        "Cascadia Code",
        "Consolas",
        monospace;

    font-size: 16px;

    font-weight: 700;

    fill: {TEXT_COLOR};
}}

.month {{
    font-family:
        "SFMono-Regular",
        "Cascadia Code",
        "Consolas",
        monospace;

    font-size: 12px;

    fill: {MUTED_COLOR};
}}

.day {{
    font-family:
        "SFMono-Regular",
        "Cascadia Code",
        "Consolas",
        monospace;

    font-size: 11px;

    fill: {MUTED_COLOR};
}}

.footer {{
    font-family:
        "SFMono-Regular",
        "Cascadia Code",
        "Consolas",
        monospace;

    font-size: 13px;

    font-weight: 700;

    fill: {TEXT_COLOR};
}}

.legend-text {{
    font-family:
        "SFMono-Regular",
        "Cascadia Code",
        "Consolas",
        monospace;

    font-size: 10px;

    fill: {MUTED_COLOR};
}}

rect {{
    shape-rendering: geometricPrecision;
}}

</style>

{''.join(svg_elements)}

</svg>
"""

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("=" * 40)
    print("CONTRIBUTION HEATMAP CREATED")
    print("=" * 40)
    print()
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total: {total_contributions:,}")
    print(f"Grid: {WEEKS} weeks x {DAYS} days")
    print("Data: REAL GitHub contributions")
    print("Animation: FAST")
    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    create_svg()