from pathlib import Path
from datetime import datetime, timedelta
import json
import html
import math


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
# SVG CANVAS
# ============================================================

# IMPORTANT:
# The previous version was too narrow.
# This wider canvas prevents the right side from being cut off.

SVG_WIDTH = 1200
SVG_HEIGHT = 255


# ============================================================
# HEATMAP GRID
# ============================================================

CELL_SIZE = 16
CELL_GAP = 4

LEFT_MARGIN = 60
TOP_MARGIN = 72

DAY_ROWS = 7
MAX_WEEKS = 53


# ============================================================
# COLORS
# ============================================================

TEXT_COLOR = "#c9d1d9"
MUTED_COLOR = "#8b949e"

LEVEL_COLORS = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
]


# ============================================================
# FONT
# ============================================================

FONT_FAMILY = (
    '"Cascadia Code", '
    '"Cascadia Mono", '
    '"Consolas", '
    '"Courier New", '
    'monospace'
)


# ============================================================
# HELPERS
# ============================================================

def parse_date(value):

    return datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()


def sunday_start(date_value):

    days_from_sunday = (
        date_value.weekday() + 1
    ) % 7

    return date_value - timedelta(
        days=days_from_sunday
    )


def color_for_count(count):

    if count <= 0:
        return LEVEL_COLORS[0]

    if count <= 2:
        return LEVEL_COLORS[1]

    if count <= 5:
        return LEVEL_COLORS[2]

    if count <= 9:
        return LEVEL_COLORS[3]

    return LEVEL_COLORS[4]


def esc(value):

    return html.escape(
        str(value)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("==========================================")
    print(" GitHub Contribution Renderer")
    print("==========================================")
    print()

    # --------------------------------------------------------
    # Check data file
    # --------------------------------------------------------

    if not DATA_FILE.exists():

        print(
            "ERROR: contributions.json not found."
        )

        print()
        print(
            f"Expected:"
        )

        print(
            DATA_FILE
        )

        return

    # --------------------------------------------------------
    # Load JSON
    # --------------------------------------------------------

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    username = data.get(
        "username",
        USERNAME
    )

    total = int(
        data.get(
            "total_contributions",
            0
        )
    )

    contribution_list = data.get(
        "contributions",
        []
    )

    if not contribution_list:

        print(
            "ERROR: No contribution data found."
        )

        return

    # --------------------------------------------------------
    # Convert JSON to dictionary
    # --------------------------------------------------------

    contributions = {}

    for item in contribution_list:

        date_string = item.get(
            "date"
        )

        if not date_string:
            continue

        try:

            date_value = parse_date(
                date_string
            )

        except ValueError:

            continue

        count = int(
            item.get(
                "count",
                0
            )
        )

        contributions[
            date_value
        ] = count

    if not contributions:

        print(
            "ERROR: Contribution list is empty."
        )

        return

    # --------------------------------------------------------
    # Find complete date range
    # --------------------------------------------------------

    first_date = min(
        contributions.keys()
    )

    last_date = max(
        contributions.keys()
    )

    # Start on Sunday
    grid_start = sunday_start(
        first_date
    )

    # Move to the end of the final week
    grid_end = grid_start

    while grid_end < last_date:

        grid_end += timedelta(
            days=7
        )

    # Number of weeks
    total_days = (
        grid_end - grid_start
    ).days + 1

    weeks = math.ceil(
        total_days / 7
    )

    weeks = min(
        weeks,
        MAX_WEEKS
    )

    print(
        f"Loading real data for @{username}..."
    )

    print(
        f"Real contributions: {total}"
    )

    print(
        f"Grid: {weeks} weeks x 7 days"
    )

    # --------------------------------------------------------
    # Calculate grid size
    # --------------------------------------------------------

    grid_width = (
        weeks * CELL_SIZE
        + (weeks - 1) * CELL_GAP
    )

    grid_height = (
        DAY_ROWS * CELL_SIZE
        + (DAY_ROWS - 1) * CELL_GAP
    )

    RIGHT_MARGIN = 60

    required_width = (
        LEFT_MARGIN
        + grid_width
        + RIGHT_MARGIN
    )

    # Safety check
    final_width = max(
        SVG_WIDTH,
        required_width
    )

    # --------------------------------------------------------
    # Start SVG
    # --------------------------------------------------------

    svg = []

    svg.append(
        '<?xml version="1.0" encoding="UTF-8"?>'
    )

    svg.append(
        f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="100%"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {final_width} {SVG_HEIGHT}"
    preserveAspectRatio="xMidYMid meet"
    role="img"
    aria-label="GitHub contribution heatmap for {esc(username)}"
>
'''
    )

    # --------------------------------------------------------
    # Styles
    # --------------------------------------------------------

    svg.append(
        f'''
<style>

.title {{
    font-family: {FONT_FAMILY};
    font-size: 18px;
    font-weight: 700;
    fill: {TEXT_COLOR};
}}

.month {{
    font-family: {FONT_FAMILY};
    font-size: 12px;
    fill: {MUTED_COLOR};
}}

.day {{
    font-family: {FONT_FAMILY};
    font-size: 12px;
    fill: {MUTED_COLOR};
}}

.total {{
    font-family: {FONT_FAMILY};
    font-size: 16px;
    font-weight: 700;
    fill: {TEXT_COLOR};
}}

.legend {{
    font-family: {FONT_FAMILY};
    font-size: 11px;
    fill: {MUTED_COLOR};
}}

.cell {{
    rx: 3;
    ry: 3;
}}

</style>
'''
    )

    # ========================================================
    # TOP COMMAND
    # ========================================================

    svg.append(
        f'''
<text
    x="{final_width / 2:.2f}"
    y="28"
    text-anchor="middle"
    class="title"
>
    {esc(username)}@github ~ $ ./contributions.sh
</text>
'''
    )

    # ========================================================
    # MONTH LABELS
    # ========================================================

    previous_month = None

    for week in range(weeks):

        week_date = (
            grid_start
            + timedelta(
                days=week * 7
            )
        )

        month = week_date.month

        if month == previous_month:
            continue

        previous_month = month

        x = (
            LEFT_MARGIN
            + week
            * (CELL_SIZE + CELL_GAP)
        )

        svg.append(
            f'''
<text
    x="{x}"
    y="52"
    class="month"
>
    {week_date.strftime("%b")}
</text>
'''
        )

    # ========================================================
    # DAY LABELS
    # ========================================================

    day_labels = {
        1: "Mon",
        3: "Wed",
        5: "Fri"
    }

    for row, label in day_labels.items():

        y = (
            TOP_MARGIN
            + row
            * (CELL_SIZE + CELL_GAP)
            + 12
        )

        svg.append(
            f'''
<text
    x="8"
    y="{y}"
    class="day"
>
    {label}
</text>
'''
        )

    # ========================================================
    # ANIMATED HEATMAP
    #
    # Each row wipes from LEFT -> RIGHT.
    #
    # Row 0 starts first.
    # Row 1 starts slightly later.
    # Row 2 starts after that.
    # ...
    #
    # This produces the same terminal-style
    # progressive animation.
    # ========================================================

    for row in range(DAY_ROWS):

        row_y = (
            TOP_MARGIN
            + row
            * (CELL_SIZE + CELL_GAP)
        )

        clip_id = (
            f"heatmapRow{row}"
        )

        # ----------------------------------------------------
        # Clip path
        # ----------------------------------------------------

        svg.append(
            f'''
<clipPath id="{clip_id}">
    <rect
        x="{LEFT_MARGIN}"
        y="{row_y}"
        width="0"
        height="{CELL_SIZE}"
    >

        <animate
            attributeName="width"
            from="0"
            to="{grid_width}"
            begin="{row * 0.12:.2f}s"
            dur="1.10s"
            fill="freeze"
        />

    </rect>
</clipPath>
'''
        )

        # ----------------------------------------------------
        # Row group
        # ----------------------------------------------------

        svg.append(
            f'''
<g clip-path="url(#{clip_id})">
'''
        )

        # ----------------------------------------------------
        # Cells
        # ----------------------------------------------------

        for week in range(weeks):

            current_date = (
                grid_start
                + timedelta(
                    days=week * 7 + row
                )
            )

            count = contributions.get(
                current_date,
                0
            )

            # Outside actual data range
            if (
                current_date < first_date
                or current_date > last_date
            ):

                count = 0

            x = (
                LEFT_MARGIN
                + week
                * (CELL_SIZE + CELL_GAP)
            )

            color = color_for_count(
                count
            )

            svg.append(
                f'''
<rect
    x="{x}"
    y="{row_y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    class="cell"
    fill="{color}"
>
    <title>
        {current_date.isoformat()}: {count} contributions
    </title>
</rect>
'''
            )

        svg.append(
            "</g>"
        )

    # ========================================================
    # TOTAL CONTRIBUTIONS
    # ========================================================

    total_y = (
        TOP_MARGIN
        + grid_height
        + 38
    )

    svg.append(
        f'''
<text
    x="{LEFT_MARGIN}"
    y="{total_y}"
    class="total"
>
    {total} contributions in the last year
</text>
'''
    )

    # ========================================================
    # LEGEND
    # ========================================================

    legend_width = 170

    legend_x = (
        final_width
        - legend_width
    )

    svg.append(
        f'''
<text
    x="{legend_x - 25}"
    y="{total_y}"
    text-anchor="end"
    class="legend"
>
    Less
</text>
'''
    )

    for index, color in enumerate(
        LEVEL_COLORS
    ):

        x = (
            legend_x
            + index * 22
        )

        svg.append(
            f'''
<rect
    x="{x}"
    y="{total_y - 13}"
    width="16"
    height="16"
    rx="3"
    ry="3"
    fill="{color}"
/>
'''
        )

    svg.append(
        f'''
<text
    x="{legend_x + 5 * 22 + 8}"
    y="{total_y}"
    class="legend"
>
    More
</text>
'''
    )

    # ========================================================
    # CLOSE SVG
    # ========================================================

    svg.append(
        "</svg>"
    )

    # ========================================================
    # WRITE FILE
    # ========================================================

    OUTPUT_FILE.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print()
    print("==========================================")
    print(" SUCCESS")
    print("==========================================")
    print()
    print(
        f"Output: {OUTPUT_FILE}"
    )
    print(
        f"Username: {username}"
    )
    print(
        f"Contributions: {total}"
    )
    print(
        f"Weeks: {weeks}"
    )
    print()
    print("Background: TRANSPARENT")
    print("Border: NONE")
    print("Terminal frame: NONE")
    print("Animation: ROW-BY-ROW")
    print("Direction: LEFT -> RIGHT")
    print()
    print("All columns visible.")
    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()