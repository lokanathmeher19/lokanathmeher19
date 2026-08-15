from pathlib import Path
import html


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "wordmark.svg"


# ============================================================
# PROFILE
# ============================================================

USERNAME = "lokanathmeher19"
COMMAND = "./wordmark.sh"

SUBTITLE_1 = "CSE Student"
SUBTITLE_2 = "Full-Stack Developer"
SUBTITLE_3 = "DevOps Enthusiast"

WHOAMI = "lokanathmeher19"


# ============================================================
# SVG SIZE
# ============================================================

WIDTH = 900
HEIGHT = 220


# ============================================================
# COLORS
# ============================================================

WHITE = "#F0F6FC"
CYAN = "#58A6FF"
GREEN = "#3FB950"
PURPLE = "#BC8CFF"
ORANGE = "#F0883E"
GRAY = "#8B949E"


def esc(text):
    return html.escape(text)


# ============================================================
# SVG
# ============================================================

svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

    <!-- ================================================== -->
    <!-- TRANSPARENT BACKGROUND                             -->
    <!-- ================================================== -->

    <rect
        width="{WIDTH}"
        height="{HEIGHT}"
        fill="transparent"
    />


    <!-- ================================================== -->
    <!-- TERMINAL COMMAND                                   -->
    <!-- ================================================== -->

    <text
        x="450"
        y="40"
        text-anchor="middle"
        font-family="Consolas, 'Courier New', monospace"
        font-size="20"
        font-weight="700"
        fill="{WHITE}"
    >
        {esc(USERNAME)}@github ~
        <tspan fill="{CYAN}"> $ {esc(COMMAND)}</tspan>
    </text>


    <!-- ================================================== -->
    <!-- MAIN USERNAME                                      -->
    <!-- ================================================== -->

    <text
        x="450"
        y="105"
        text-anchor="middle"
        font-family="Consolas, 'Courier New', monospace"
        font-size="48"
        font-weight="700"
        fill="{WHITE}"
    >
        {esc(USERNAME)}
    </text>


    <!-- ================================================== -->
    <!-- BLINKING TERMINAL CURSOR                          -->
    <!-- ================================================== -->

    <rect
        x="705"
        y="72"
        width="4"
        height="38"
        rx="1"
        fill="{CYAN}"
    >

        <animate
            attributeName="opacity"
            values="1;1;0;0;1"
            keyTimes="0;0.45;0.5;0.95;1"
            dur="1.2s"
            repeatCount="indefinite"
        />

    </rect>


    <!-- ================================================== -->
    <!-- SUBTITLE                                           -->
    <!-- ================================================== -->

    <text
        x="450"
        y="145"
        text-anchor="middle"
        font-family="Consolas, 'Courier New', monospace"
        font-size="17"
        font-weight="500"
    >

        <tspan fill="{CYAN}">
            {esc(SUBTITLE_1)}
        </tspan>

        <tspan fill="{GRAY}">
            &#160; | &#160;
        </tspan>

        <tspan fill="{PURPLE}">
            {esc(SUBTITLE_2)}
        </tspan>

        <tspan fill="{GRAY}">
            &#160; | &#160;
        </tspan>

        <tspan fill="{ORANGE}">
            {esc(SUBTITLE_3)}
        </tspan>

    </text>


    <!-- ================================================== -->
    <!-- WHOAMI                                             -->
    <!-- ================================================== -->

    <text
        x="450"
        y="190"
        text-anchor="middle"
        font-family="Consolas, 'Courier New', monospace"
        font-size="16"
        font-weight="500"
    >

        <tspan fill="{GREEN}">$</tspan>

        <tspan fill="{GRAY}">
            &#160;whoami&#160;→&#160;
        </tspan>

        <tspan fill="{CYAN}">
            {esc(WHOAMI)}
        </tspan>

    </text>

</svg>
'''


# ============================================================
# WRITE FILE
# ============================================================

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)


print()
print("==========================================")
print(" WORDMARK CREATED SUCCESSFULLY")
print("==========================================")
print()
print(f"Output : {OUTPUT}")
print(f"Size   : {WIDTH} x {HEIGHT}")
print("Theme  : Terminal / Developer")
print("Colors : Cyan / Green / Purple / Orange")
print("Cursor : Blinking")
print()