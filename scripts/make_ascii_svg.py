from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import html


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "data" / "source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"


# ============================================================
# ASCII SETTINGS
# ============================================================

ASCII_WIDTH = 120
ASCII_HEIGHT = 78

RAMP = " .,:;irsXA253hMHGS#9B&@"


# ============================================================
# FINAL SVG SIZE
# ============================================================

SVG_WIDTH = 480
SVG_HEIGHT = 480


# ============================================================
# TERMINAL
# ============================================================

# IMPORTANT:
# The terminal occupies the COMPLETE SVG canvas.

CARD_X = 0
CARD_Y = 0

CARD_WIDTH = 480
CARD_HEIGHT = 480

CARD_RADIUS = 15

TITLE_HEIGHT = 36


# ============================================================
# COLORS
# ============================================================

BG = "#0d1117"
TITLE_BG = "#161b22"
BORDER = "#30363d"

TEXT = "#d8dee9"
MUTED = "#8b949e"


# ============================================================
# ASCII APPEARANCE
# ============================================================

FONT_SIZE = 4.2
CHAR_WIDTH = 3.5
LINE_HEIGHT = 4.8


# ============================================================
# IMAGE SETTINGS
# ============================================================

CONTRAST = 1.25


# ============================================================
# ESCAPE
# ============================================================

def esc(value):
    return html.escape(value)


# ============================================================
# MAIN
# ============================================================

def main():

    if not INPUT.exists():

        raise FileNotFoundError(
            f"Image not found: {INPUT}"
        )


    print()
    print("========================================")
    print("       ASCII SVG GENERATOR")
    print("========================================")
    print()


    # ========================================================
    # LOAD IMAGE
    # ========================================================

    image = Image.open(INPUT).convert("RGBA")

    alpha = image.getchannel("A")

    bbox = alpha.getbbox()


    if bbox is None:

        raise RuntimeError(
            "No visible subject found in image."
        )


    # Remove transparent padding
    image = image.crop(bbox)


    # ========================================================
    # GRAYSCALE
    # ========================================================

    rgb = image.convert("RGB")

    alpha = image.getchannel("A")

    gray = ImageOps.grayscale(rgb)


    # ========================================================
    # CONTRAST
    # ========================================================

    gray = ImageOps.autocontrast(
        gray
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
            radius=1,
            percent=150,
            threshold=2
        )
    )


    # ========================================================
    # RESIZE IMAGE
    # ========================================================

    target_height = ASCII_HEIGHT

    scale = (
        target_height
        / gray.height
    )

    target_width = int(
        gray.width
        * scale
        * 1.72
    )


    # Keep some horizontal margin
    target_width = min(
        target_width,
        ASCII_WIDTH - 10
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
    # ASCII CANVAS
    # ========================================================

    gray_canvas = Image.new(
        "L",
        (
            ASCII_WIDTH,
            ASCII_HEIGHT
        ),
        255
    )

    alpha_canvas = Image.new(
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

    x_offset = (
        ASCII_WIDTH
        - target_width
    ) // 2


    gray_canvas.paste(
        gray,
        (
            x_offset,
            0
        )
    )

    alpha_canvas.paste(
        alpha,
        (
            x_offset,
            0
        )
    )


    # ========================================================
    # GENERATE ASCII
    # ========================================================

    pixels = gray_canvas.load()
    alpha_pixels = alpha_canvas.load()

    rows = []


    for y in range(ASCII_HEIGHT):

        row = []

        for x in range(ASCII_WIDTH):

            a = alpha_pixels[x, y]


            if a < 15:

                row.append(" ")

                continue


            brightness = pixels[x, y]


            # Convert brightness to ASCII
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
    # FIND SUBJECT BOUNDING BOX
    # ========================================================

    left = ASCII_WIDTH
    right = 0
    top = ASCII_HEIGHT
    bottom = 0


    for y, row in enumerate(rows):

        for x, char in enumerate(row):

            if char != " ":

                left = min(left, x)
                right = max(right, x)

                top = min(top, y)
                bottom = max(bottom, y)


    if left > right:

        raise RuntimeError(
            "ASCII image is empty."
        )


    # ========================================================
    # CENTER SUBJECT HORIZONTALLY
    # ========================================================

    subject_width = (
        right - left + 1
    )


    desired_left = (
        ASCII_WIDTH
        - subject_width
    ) // 2


    shift = (
        desired_left - left
    )


    new_rows = []


    for row in rows:

        if shift > 0:

            row = (
                " " * shift
                + row[:ASCII_WIDTH - shift]
            )


        elif shift < 0:

            amount = abs(shift)

            row = (
                row[amount:]
                + " " * amount
            )


        new_rows.append(row)


    rows = new_rows


    # ========================================================
    # SVG ASCII DIMENSIONS
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
    # AVAILABLE AREA
    # ========================================================

    # Card content starts below title bar.
    # Keep equal padding around portrait.

    LEFT_PADDING = 18
    RIGHT_PADDING = 18

    TOP_PADDING = 12
    BOTTOM_PADDING = 24


    available_width = (
        CARD_WIDTH
        - LEFT_PADDING
        - RIGHT_PADDING
    )


    available_height = (
        CARD_HEIGHT
        - TITLE_HEIGHT
        - TOP_PADDING
        - BOTTOM_PADDING
    )


    # ========================================================
    # SCALE TO FIT
    # ========================================================

    scale_x = (
        available_width
        / portrait_width
    )

    scale_y = (
        available_height
        / portrait_height
    )


    scale = min(
        scale_x,
        scale_y
    )


    final_width = (
        portrait_width
        * scale
    )

    final_height = (
        portrait_height
        * scale
    )


    # ========================================================
    # CENTER PORTRAIT
    # ========================================================

    start_x = (
        CARD_X
        + (
            CARD_WIDTH
            - final_width
        ) / 2
    )


    content_top = (
        TITLE_HEIGHT
        + TOP_PADDING
    )


    start_y = (
        content_top
        + (
            available_height
            - final_height
        ) / 2
    )


    final_font_size = (
        FONT_SIZE
        * scale
    )


    final_line_height = (
        LINE_HEIGHT
        * scale
    )


    # ========================================================
    # ANIMATED ROWS
    # ========================================================

    animated_rows = []


    for index, row in enumerate(rows):

        y = (
            start_y
            + index
            * final_line_height
        )


        safe_row = esc(row)


        clip_id = (
            f"rowClip{index}"
        )


        delay = (
            index * 0.018
        )


        animated_rows.append(
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
                values="
                    0;
                    {final_width:.2f};
                    {final_width:.2f}
                "
                keyTimes="
                    0;
                    0.25;
                    1
                "
                begin="{delay:.3f}s"
                dur="3s"
                repeatCount="indefinite"
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
    # COMPLETE SVG
    # ========================================================

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
    preserveAspectRatio="xMidYMid meet"
>

<style>

.ascii {{
    font-family:
        "Courier New",
        Consolas,
        monospace;

    font-size:
        {final_font_size:.2f}px;

    font-weight:
        700;

    fill:
        {TEXT};

    white-space:
        pre;
}}

.prompt {{
    font-family:
        "Courier New",
        Consolas,
        monospace;

    font-size:
        6px;

    fill:
        {MUTED};
}}

</style>


<!-- ========================================================
     TERMINAL CARD
     ======================================================== -->

<rect
    x="1"
    y="1"
    width="478"
    height="478"
    rx="{CARD_RADIUS}"
    fill="{BG}"
    stroke="{BORDER}"
    stroke-width="2"
/>


<!-- ========================================================
     TITLE BAR
     ======================================================== -->

<path
    d="
        M 16 1
        H 464
        Q 479 1 479 16
        V 36
        H 1
        V 16
        Q 1 1 16 1
        Z
    "
    fill="{TITLE_BG}"
/>


<!-- ========================================================
     TITLE LINE
     ======================================================== -->

<line
    x1="1"
    y1="36"
    x2="479"
    y2="36"
    stroke="{BORDER}"
    stroke-width="1"
/>


<!-- ========================================================
     MAC BUTTONS
     ======================================================== -->

<circle
    cx="19"
    cy="19"
    r="4"
    fill="#ff5f56"
/>

<circle
    cx="35"
    cy="19"
    r="4"
    fill="#ffbd2e"
/>

<circle
    cx="51"
    cy="19"
    r="4"
    fill="#27c93f"
/>


<!-- ========================================================
     TERMINAL TITLE
     ======================================================== -->

<text
    x="240"
    y="22"
    text-anchor="middle"
    font-family="Consolas, 'Courier New', monospace"
    font-size="7"
    font-weight="600"
    fill="{MUTED}"
>
    lokanath@github: ~
</text>


<!-- ========================================================
     ASCII PORTRAIT
     ======================================================== -->

{''.join(animated_rows)}


<!-- ========================================================
     PROMPT
     ======================================================== -->

<text
    x="10"
    y="470"
    class="prompt"
>
    lokanathmeher19@github:~$ ./portrait.sh
</text>


</svg>
"""


    # ========================================================
    # SAVE
    # ========================================================

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )


    # ========================================================
    # RESULT
    # ========================================================

    print()
    print("========================================")
    print("       SUCCESS")
    print("========================================")
    print()

    print(
        f"Output: {OUTPUT}"
    )

    print(
        f"SVG: {SVG_WIDTH} x {SVG_HEIGHT}"
    )

    print(
        f"Terminal: {CARD_WIDTH} x {CARD_HEIGHT}"
    )

    print(
        f"Portrait: {final_width:.1f} x "
        f"{final_height:.1f}"
    )

    print(
        f"Scale: {scale:.3f}"
    )

    print()
    print("Terminal fills the SVG canvas.")
    print("No outer canvas padding.")
    print("Portrait is centered.")
    print("Animation repeats every 3 seconds.")
    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()