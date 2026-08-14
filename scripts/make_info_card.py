from pathlib import Path
import html


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"


# ============================================================
# YOUR INFORMATION
# ============================================================

NAME = "Lokanath Meher"
USERNAME = "@lokanathmeher19"

ROLE = "CSE Student  •  Full-Stack Developer  •  DevOps Enthusiast"
STACK = "Python  •  C++  •  JavaScript  •  React  •  Node.js"
TOOLS = "Git  •  GitHub  •  VS Code  •  Linux"
DATABASE = "MySQL  •  MongoDB"
FOCUS = "Full-Stack Development  •  DevOps"
LOCATION = "India"


# ============================================================
# SVG SIZE
# ============================================================

WIDTH = 650
HEIGHT = 430


# ============================================================
# HELPER
# ============================================================

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
    role="img"
    aria-label="Lokanath Meher profile information"
>

    <!-- =====================================================
         TERMINAL BODY
         ===================================================== -->

    <rect
        x="2"
        y="2"
        width="646"
        height="426"
        rx="16"
        fill="#0d1117"
        stroke="#30363d"
        stroke-width="2"
    />


    <!-- =====================================================
         TITLE BAR
         ===================================================== -->

    <rect
        x="3"
        y="3"
        width="644"
        height="43"
        rx="15"
        fill="#161b22"
    />

    <rect
        x="3"
        y="25"
        width="644"
        height="21"
        fill="#161b22"
    />


    <!-- Separator -->

    <line
        x1="3"
        y1="46"
        x2="647"
        y2="46"
        stroke="#30363d"
        stroke-width="1"
    />


    <!-- =====================================================
         MAC BUTTONS
         ===================================================== -->

    <circle
        cx="27"
        cy="24"
        r="6"
        fill="#ff5f56"
    />

    <circle
        cx="49"
        cy="24"
        r="6"
        fill="#ffbd2e"
    />

    <circle
        cx="71"
        cy="24"
        r="6"
        fill="#27c93f"
    />


    <!-- =====================================================
         TERMINAL TITLE
         ===================================================== -->

    <text
        x="325"
        y="28"
        text-anchor="middle"
        font-family="Consolas, Courier New, monospace"
        font-size="9"
        font-weight="600"
        fill="#8b949e"
    >
        lokanath@github: ~
    </text>


    <!-- =====================================================
         WHOAMI
         ===================================================== -->

    <text
        x="30"
        y="78"
        font-family="Consolas, Courier New, monospace"
        font-size="15"
        font-weight="700"
        fill="#3fb950"
    >
        $ whoami
    </text>


    <!-- =====================================================
         NAME
         ===================================================== -->

    <text
        x="30"
        y="113"
        font-family="Consolas, Courier New, monospace"
        font-size="25"
        font-weight="700"
        fill="#d8dee9"
    >
        {esc(NAME)}
    </text>


    <!-- =====================================================
         USERNAME
         ===================================================== -->

    <text
        x="30"
        y="139"
        font-family="Consolas, Courier New, monospace"
        font-size="14"
        fill="#8b949e"
    >
        {esc(USERNAME)}
    </text>


    <!-- =====================================================
         SEPARATOR
         ===================================================== -->

    <line
        x1="30"
        y1="160"
        x2="620"
        y2="160"
        stroke="#30363d"
        stroke-width="1"
    />


    <!-- =====================================================
         ROLE
         ===================================================== -->

    <text
        x="30"
        y="192"
        font-family="Consolas, Courier New, monospace"
        font-size="12"
        font-weight="700"
        fill="#58a6ff"
    >
        ROLE
    </text>

    <text
        x="125"
        y="192"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#d8dee9"
    >
        {esc(ROLE)}
    </text>


    <!-- =====================================================
         STACK
         ===================================================== -->

    <text
        x="30"
        y="226"
        font-family="Consolas, Courier New, monospace"
        font-size="12"
        font-weight="700"
        fill="#bc8cff"
    >
        STACK
    </text>

    <text
        x="125"
        y="226"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#d8dee9"
    >
        {esc(STACK)}
    </text>


    <!-- =====================================================
         TOOLS
         ===================================================== -->

    <text
        x="30"
        y="260"
        font-family="Consolas, Courier New, monospace"
        font-size="12"
        font-weight="700"
        fill="#3fb950"
    >
        TOOLS
    </text>

    <text
        x="125"
        y="260"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#d8dee9"
    >
        {esc(TOOLS)}
    </text>


    <!-- =====================================================
         DATABASE
         ===================================================== -->

    <text
        x="30"
        y="294"
        font-family="Consolas, Courier New, monospace"
        font-size="12"
        font-weight="700"
        fill="#58a6ff"
    >
        DATABASE
    </text>

    <text
        x="125"
        y="294"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#d8dee9"
    >
        {esc(DATABASE)}
    </text>


    <!-- =====================================================
         FOCUS
         ===================================================== -->

    <text
        x="30"
        y="328"
        font-family="Consolas, Courier New, monospace"
        font-size="12"
        font-weight="700"
        fill="#bc8cff"
    >
        FOCUS
    </text>

    <text
        x="125"
        y="328"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#d8dee9"
    >
        {esc(FOCUS)}
    </text>


    <!-- =====================================================
         LOCATION
         ===================================================== -->

    <text
        x="30"
        y="362"
        font-family="Consolas, Courier New, monospace"
        font-size="12"
        font-weight="700"
        fill="#d29922"
    >
        LOCATION
    </text>

    <text
        x="125"
        y="362"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#d8dee9"
    >
        {esc(LOCATION)}
    </text>


    <!-- =====================================================
         FOOTER
         ===================================================== -->

    <text
        x="30"
        y="398"
        font-family="Consolas, Courier New, monospace"
        font-size="11"
        fill="#8b949e"
    >
        $ Building  •  Learning  •  Exploring
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
print("================================")
print("INFO CARD CREATED SUCCESSFULLY")
print("================================")
print()
print(f"Output: {OUTPUT}")
print(f"Canvas: {WIDTH} x {HEIGHT}")
print()