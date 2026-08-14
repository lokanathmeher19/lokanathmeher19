from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import html


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

INPUT = DATA_DIR / "source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"


# ============================================================
# ASCII SETTINGS
# ============================================================

ASCII_WIDTH = 120
ASCII_HEIGHT = 78

RAMP = " .,:;irsXA253hMHGS#9B&@"

ALPHA_THRESHOLD = 15


# ============================================================
# SVG / TERMINAL SIZE
# ============================================================

# FINAL SVG SIZE
SVG_WIDTH = 480
SVG_HEIGHT = 480

# Terminal window
WINDOW_X = 8
WINDOW_Y = 8

WINDOW_WIDTH = 464
WINDOW_HEIGHT = 464

WINDOW_RADIUS = 15

# Smaller title bar
TITLE_BAR_HEIGHT = 36


# ============================================================
# COLORS
# ============================================================

BACKGROUND = "#0d1117"
TITLE_BACKGROUND = "#161b22"
BORDER = "#30363d"

TEXT_COLOR = "#d8dee9"
MUTED_COLOR = "#8b949e"


# ============================================================
# ASCII FONT / SPACING
# ============================================================

# These values make the complete ASCII portrait fit
# comfortably inside the smaller 480x480 SVG.

FONT_SIZE = 4.2
CHAR_WIDTH = 3.5
LINE_HEIGHT = 4.8


# ============================================================
# IMAGE QUALITY
# ============================================================

CONTRAST = 1.25


# ============================================================
# MAIN
# ============================================================

def main():

    if not INPUT.exists():

        print(
            f"ERROR: Image not found: {INPUT}"
        )

        return


    print()
    print("========================================")
    print("       CREATING ASCII PORTRAIT")
    print("========================================")
    print()

    print(f"Input : {INPUT}")
    print(f"Output: {OUTPUT}")
    print()


    # ========================================================
    # LOAD IMAGE
    # ========================================================

    image = Image.open(INPUT).convert("RGBA")

    alpha = image.getchannel("A")

    bbox = alpha.getbbox()


    if bbox is None:

        print(
            "ERROR: No subject detected."
        )

        return


    # Crop transparent area around subject
    image = image.crop(bbox)

    print(
        f"Source: {image.width} x {image.height}"
    )


    # ========================================================
    # RGB + ALPHA
    # ========================================================

    rgb = image.convert("RGB")

    alpha = image.getchannel("A")


    # ========================================================
    # GRAYSCALE
    # ========================================================

    gray = ImageOps.grayscale(rgb)


    # ========================================================
    # CONTRAST
    # ========================================================

    gray = ImageOps.autocontrast(
        gray,
        cutoff=0
    )

    gray = ImageEnhance.Contrast(
        gray
    ).enhance(
        CONTRAST
    )


    # ========================================================
    # SHARPEN
    # ========================================================

    gray = gray.filter(
        ImageFilter.UnsharpMask(
            radius=1.1,
            percent=150,
            threshold=2
        )
    )


    # ========================================================
    # RESIZE
    # ========================================================

    source_width = gray.width
    source_height = gray.height

    target_height = ASCII_HEIGHT

    scale = (
        target_height
        / source_height
    )

    target_width = int(
        source_width
        * scale
        * 1.72
    )

    max_width = ASCII_WIDTH - 6

    target_width = min(
        target_width,
        max_width
    )


    gray = gray.resize(
        (
            target_width,
            target_height
        ),
        Image.Resampling.LANCZOS
    )

    alpha = alpha.resize(
        (
            target_width,
            target_height
        ),
        Image.Resampling.LANCZOS
    )


    # ========================================================
    # CREATE ASCII CANVAS
    # ========================================================

    canvas_gray = Image.new(
        "L",
        (
            ASCII_WIDTH,
            ASCII_HEIGHT
        ),
        255
    )

    canvas_alpha = Image.new(
        "L",
        (
            ASCII_WIDTH,
            ASCII_HEIGHT
        ),
        0
    )


    # ========================================================
    # CENTER IMAGE
    # ========================================================

    offset_x = (
        ASCII_WIDTH
        - target_width
    ) // 2

    offset_y = 0


    canvas_gray.paste(
        gray,
        (
            offset_x,
            offset_y
        )
    )

    canvas_alpha.paste(
        alpha,
        (
            offset_x,
            offset_y
        )
    )


    # ========================================================
    # CONVERT TO ASCII
    # ========================================================

    gray_pixels = canvas_gray.load()
    alpha_pixels = canvas_alpha.load()

    rows = []


    for y in range(ASCII_HEIGHT):

        row = []

        for x in range(ASCII_WIDTH):

            a = alpha_pixels[x, y]


            # Transparent area
            if a < ALPHA_THRESHOLD:

                row.append(" ")

                continue


            brightness = gray_pixels[x, y]


            # Soft edges
            if a < 220:

                brightness = (
                    brightness
                    * (a / 255)
                    +
                    255
                    * (1 - a / 255)
                )


            # Contrast curve
            normalized = (
                brightness / 255.0
            )

            normalized = (
                normalized - 0.5
            ) * 1.28 + 0.5

            normalized = max(
                0.0,
                min(
                    1.0,
                    normalized
                )
            )

            brightness = (
                normalized * 255
            )


            index = int(
                brightness
                / 256
                * len(RAMP)
            )

            index = max(
                0,
                min(
                    len(RAMP) - 1,
                    index
                )
            )


            row.append(
                RAMP[index]
            )


        rows.append(
            "".join(row)
        )


    # ========================================================
    # FIND ACTUAL VISIBLE SUBJECT
    # ========================================================

    visible_columns = []


    for x in range(ASCII_WIDTH):

        found = False

        for y in range(ASCII_HEIGHT):

            if rows[y][x] != " ":

                found = True
                break


        if found:

            visible_columns.append(x)


    if not visible_columns:

        print(
            "ERROR: ASCII subject is empty."
        )

        return


    # ========================================================
    # SUBJECT BOUNDING BOX
    # ========================================================

    subject_left = min(
        visible_columns
    )

    subject_right = max(
        visible_columns
    )

    subject_width = (
        subject_right
        - subject_left
        + 1
    )


    # ========================================================
    # CENTER ACTUAL SUBJECT
    # ========================================================

    desired_left = (
        ASCII_WIDTH
        - subject_width
    ) // 2

    shift_x = (
        desired_left
        - subject_left
    )


    centered_rows = []


    for row in rows:

        if shift_x > 0:

            row = (
                " " * shift_x
                + row[
                    :ASCII_WIDTH - shift_x
                ]
            )


        elif shift_x < 0:

            amount = abs(shift_x)

            row = (
                row[amount:]
                + " " * amount
            )


        centered_rows.append(
            row
        )


    rows = centered_rows


    # ========================================================
    # FINAL SUBJECT CHECK
    # ========================================================

    visible_columns = []


    for x in range(ASCII_WIDTH):

        for y in range(ASCII_HEIGHT):

            if rows[y][x] != " ":

                visible_columns.append(x)
                break


    final_left = min(
        visible_columns
    )

    final_right = max(
        visible_columns
    )

    final_center = (
        final_left
        + final_right
    ) / 2

    canvas_center = (
        ASCII_WIDTH - 1
    ) / 2


    print(
        f"Subject columns: "
        f"{final_left} - {final_right}"
    )

    print(
        f"Subject center: "
        f"{final_center:.1f}"
    )

    print(
        f"Canvas center: "
        f"{canvas_center:.1f}"
    )


    # ========================================================
    # SVG PORTRAIT SIZE
    # ========================================================

    portrait_width = (
        ASCII_WIDTH
        * CHAR_WIDTH
    )

    portrait_height = (
        ASCII_HEIGHT
        * LINE_HEIGHT
    )


    # ========================================================
    # AVAILABLE TERMINAL AREA
    # ========================================================

    # Extra top margin below title bar
    CONTENT_TOP_MARGIN = 18

    # Extra bottom margin above prompt
    CONTENT_BOTTOM_MARGIN = 32


    content_top = (
        TITLE_BAR_HEIGHT
        + CONTENT_TOP_MARGIN
    )

    content_bottom = (
        WINDOW_HEIGHT
        - CONTENT_BOTTOM_MARGIN
    )

    content_height = (
        content_bottom
        - content_top
    )


    # ========================================================
    # SAFETY SCALE
    #
    # This guarantees that the ASCII portrait NEVER
    # goes outside the terminal window.
    # ========================================================

    available_width = (
        WINDOW_WIDTH - 30
    )

    available_height = content_height


    scale_x = (
        available_width
        / portrait_width
    )

    scale_y = (
        available_height
        / portrait_height
    )

    fit_scale = min(
        1.0,
        scale_x,
        scale_y
    )


    final_portrait_width = (
        portrait_width
        * fit_scale
    )

    final_portrait_height = (
        portrait_height
        * fit_scale
    )


    # ========================================================
    # CENTER ASCII INSIDE TERMINAL
    # ========================================================

    start_x = (
        WINDOW_X
        + (
            WINDOW_WIDTH
            - final_portrait_width
        ) / 2
    )


    start_y = (
        WINDOW_Y
        + content_top
        + (
            content_height
            - final_portrait_height
        ) / 2
    )


    # Scaled font and line height
    final_font_size = (
        FONT_SIZE
        * fit_scale
    )

    final_line_height = (
        LINE_HEIGHT
        * fit_scale
    )


    print()
    print(
        f"SVG size: "
        f"{SVG_WIDTH} x {SVG_HEIGHT}"
    )

    print(
        f"Terminal: "
        f"{WINDOW_WIDTH} x {WINDOW_HEIGHT}"
    )

    print(
        f"Portrait: "
        f"{final_portrait_width:.1f} x "
        f"{final_portrait_height:.1f}"
    )

    print(
        f"Scale: "
        f"{fit_scale:.3f}"
    )


    # ========================================================
    # ROW ANIMATION
    # ========================================================

    svg_rows = []


    for row_number, row in enumerate(rows):

        safe_row = html.escape(row)

        y = (
            start_y
            + row_number
            * final_line_height
        )


        clip_id = (
            f"asciiRow{row_number}"
        )


        delay = (
            row_number
            * 0.018
        )


        svg_rows.append(
            f"""
    <clipPath id="{clip_id}">
        <rect
            x="{start_x:.2f}"
            y="{y - final_font_size:.2f}"
            width="0"
            height="{final_line_height + 2:.2f}"
        >
            <animate
                attributeName="width"
                from="0"
                to="{final_portrait_width:.2f}"
                begin="{delay:.3f}s"
                dur="0.42s"
                fill="freeze"
            />
        </rect>
    </clipPath>

    <text
        x="{start_x:.2f}"
        y="{y:.2f}"
        class="ascii"
        clip-path="url(#{clip_id})"
    >{safe_row}</text>
"""
        )


    # ========================================================
    # SVG
    # ========================================================

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
>

<!-- ========================================================
     MAC TERMINAL
     ======================================================== -->

<rect
    x="{WINDOW_X}"
    y="{WINDOW_Y}"
    width="{WINDOW_WIDTH}"
    height="{WINDOW_HEIGHT}"
    rx="{WINDOW_RADIUS}"
    fill="{BACKGROUND}"
    stroke="{BORDER}"
    stroke-width="2"
/>


<!-- ========================================================
     TITLE BAR
     ======================================================== -->

<path
    d="
        M {WINDOW_X + WINDOW_RADIUS}
          {WINDOW_Y}

        H {WINDOW_X + WINDOW_WIDTH - WINDOW_RADIUS}

        Q {WINDOW_X + WINDOW_WIDTH}
          {WINDOW_Y}

          {WINDOW_X + WINDOW_WIDTH}
          {WINDOW_Y + WINDOW_RADIUS}

        V {WINDOW_Y + TITLE_BAR_HEIGHT}

        H {WINDOW_X}

        V {WINDOW_Y + WINDOW_RADIUS}

        Q {WINDOW_X}
          {WINDOW_Y}

          {WINDOW_X + WINDOW_RADIUS}
          {WINDOW_Y}

        Z
    "
    fill="{TITLE_BACKGROUND}"
/>


<!-- TITLE BORDER -->

<line
    x1="{WINDOW_X}"
    y1="{WINDOW_Y + TITLE_BAR_HEIGHT}"
    x2="{WINDOW_X + WINDOW_WIDTH}"
    y2="{WINDOW_Y + TITLE_BAR_HEIGHT}"
    stroke="{BORDER}"
    stroke-width="1"
/>


<!-- ========================================================
     MAC BUTTONS
     ======================================================== -->

<circle
    cx="{WINDOW_X + 20}"
    cy="{WINDOW_Y + 18}"
    r="4"
    fill="#ff5f56"
/>

<circle
    cx="{WINDOW_X + 37}"
    cy="{WINDOW_Y + 18}"
    r="4"
    fill="#ffbd2e"
/>

<circle
    cx="{WINDOW_X + 54}"
    cy="{WINDOW_Y + 18}"
    r="4"
    fill="#27c93f"
/>


<!-- ========================================================
     TERMINAL TITLE
     ======================================================== -->

<text
    x="{WINDOW_X + WINDOW_WIDTH / 2}"
    y="{WINDOW_Y + 22}"
    font-family="Consolas, 'Courier New', monospace"
    font-size="7px"
    font-weight="600"
    fill="{MUTED_COLOR}"
    text-anchor="middle"
>
    lokanath@github: ~
</text>


<!-- ========================================================
     STYLE
     ======================================================== -->

<style>

.ascii {{
    font-family:
        "Courier New",
        "Consolas",
        monospace;

    font-size:
        {final_font_size:.2f}px;

    font-weight:
        700;

    fill:
        {TEXT_COLOR};

    white-space:
        pre;
}}


.prompt {{
    font-family:
        "Courier New",
        "Consolas",
        monospace;

    font-size:
        6px;

    fill:
        {MUTED_COLOR};
}}

</style>


<!-- ========================================================
     ASCII PORTRAIT
     ======================================================== -->

{''.join(svg_rows)}


<!-- ========================================================
     TERMINAL PROMPT
     ======================================================== -->

<text
    x="{WINDOW_X + 12}"
    y="{WINDOW_Y + WINDOW_HEIGHT - 10}"
    class="prompt"
>
    lokanathmeher19@github:~$ ./portrait.sh
</text>


</svg>
"""


    # ========================================================
    # WRITE FILE
    # ========================================================

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print()
    print("========================================")
    print("       ASCII SVG CREATED")
    print("========================================")
    print()

    print(
        f"Output: {OUTPUT}"
    )

    print(
        f"Canvas: {SVG_WIDTH} x {SVG_HEIGHT}"
    )

    print(
        "Subject: CENTERED"
    )

    print(
        "Portrait: FITTED INSIDE TERMINAL"
    )

    print(
        "Background: DARK TERMINAL"
    )

    print(
        "Terminal: MAC STYLE"
    )

    print(
        "Animation: ROW-BY-ROW"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()