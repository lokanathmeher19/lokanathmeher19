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
STACK = "Python  •  C++  •  HTML  •  CSS  •  JavaScript  •  React  •  Node.js"
TOOLS = "Git  •  GitHub  •  VS Code  •  Linux"
DATABASE = "MySQL  •  MongoDB"
FOCUS = "Full-Stack Development  •  DevOps"



# ============================================================
# SVG SIZE
# ============================================================

# IMPORTANT:
# Make the card tall enough to visually match the ASCII image.

WIDTH = 650
HEIGHT = 600


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
>

<!-- ========================================================
     TERMINAL BODY
     ======================================================== -->

<rect
    x="2"
    y="2"
    width="646"
    height="596"
    rx="18"
    fill="#0d1117"
    stroke="#30363d"
    stroke-width="2"
/>


<!-- ========================================================
     TITLE BAR
     ======================================================== -->

<rect
    x="3"
    y="3"
    width="644"
    height="48"
    rx="17"
    fill="#161b22"
/>

<rect
    x="3"
    y="27"
    width="644"
    height="24"
    fill="#161b22"
/>


<!-- ========================================================
     TITLE BAR LINE
     ======================================================== -->

<line
    x1="3"
    y1="51"
    x2="647"
    y2="51"
    stroke="#30363d"
    stroke-width="1"
/>


<!-- ========================================================
     MAC BUTTONS
     ======================================================== -->

<circle
    cx="28"
    cy="27"
    r="6"
    fill="#ff5f56"
/>

<circle
    cx="50"
    cy="27"
    r="6"
    fill="#ffbd2e"
/>

<circle
    cx="72"
    cy="27"
    r="6"
    fill="#27c93f"
/>


<!-- ========================================================
     TERMINAL TITLE
     ======================================================== -->

<text
    x="325"
    y="31"
    text-anchor="middle"
    font-family="Consolas, Courier New, monospace"
    font-size="10"
    font-weight="600"
    fill="#8b949e"
>
lokanath@github: ~
</text>


<!-- ========================================================
     WHOAMI
     ======================================================== -->

<text
    x="32"
    y="92"
    font-family="Consolas, Courier New, monospace"
    font-size="16"
    font-weight="700"
    fill="#3fb950"
>
$ whoami
</text>


<!-- ========================================================
     NAME
     ======================================================== -->

<text
    x="32"
    y="134"
    font-family="Consolas, Courier New, monospace"
    font-size="28"
    font-weight="700"
    fill="#d8dee9"
>
{esc(NAME)}
</text>


<!-- ========================================================
     USERNAME
     ======================================================== -->

<text
    x="32"
    y="162"
    font-family="Consolas, Courier New, monospace"
    font-size="15"
    fill="#8b949e"
>
{esc(USERNAME)}
</text>


<!-- ========================================================
     MAIN SEPARATOR
     ======================================================== -->

<line
    x1="32"
    y1="188"
    x2="618"
    y2="188"
    stroke="#30363d"
    stroke-width="1"
/>


<!-- ========================================================
     ROLE
     ======================================================== -->

<text
    x="32"
    y="228"
    font-family="Consolas, Courier New, monospace"
    font-size="13"
    font-weight="700"
    fill="#58a6ff"
>
ROLE
</text>

<text
    x="130"
    y="228"
    font-family="Consolas, Courier New, monospace"
    font-size="12"
    fill="#d8dee9"
>
{esc(ROLE)}
</text>


<!-- ========================================================
     STACK
     ======================================================== -->

<text
    x="32"
    y="278"
    font-family="Consolas, Courier New, monospace"
    font-size="13"
    font-weight="700"
    fill="#bc8cff"
>
STACK
</text>

<text
    x="130"
    y="278"
    font-family="Consolas, Courier New, monospace"
    font-size="12"
    fill="#d8dee9"
>
{esc(STACK)}
</text>


<!-- ========================================================
     TOOLS
     ======================================================== -->

<text
    x="32"
    y="328"
    font-family="Consolas, Courier New, monospace"
    font-size="13"
    font-weight="700"
    fill="#3fb950"
>
TOOLS
</text>

<text
    x="130"
    y="328"
    font-family="Consolas, Courier New, monospace"
    font-size="12"
    fill="#d8dee9"
>
{esc(TOOLS)}
</text>


<!-- ========================================================
     DATABASE
     ======================================================== -->

<text
    x="32"
    y="378"
    font-family="Consolas, Courier New, monospace"
    font-size="13"
    font-weight="700"
    fill="#58a6ff"
>
DATABASE
</text>

<text
    x="130"
    y="378"
    font-family="Consolas, Courier New, monospace"
    font-size="12"
    fill="#d8dee9"
>
{esc(DATABASE)}
</text>


<!-- ========================================================
     FOCUS
     ======================================================== -->

<text
    x="32"
    y="428"
    font-family="Consolas, Courier New, monospace"
    font-size="13"
    font-weight="700"
    fill="#bc8cff"
>
FOCUS
</text>

<text
    x="130"
    y="428"
    font-family="Consolas, Courier New, monospace"
    font-size="12"
    fill="#d8dee9"
>
{esc(FOCUS)}
</text>


<!-- ========================================================
     FOOTER
     ======================================================== -->

<line
    x1="32"
    y1="510"
    x2="618"
    y2="510"
    stroke="#21262d"
    stroke-width="1"
/>

<text
    x="32"
    y="548"
    font-family="Consolas, Courier New, monospace"
    font-size="12"
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
print("==========================================")
print(" INFO CARD CREATED SUCCESSFULLY")
print("==========================================")
print()
print(f"Output: {OUTPUT}")
print(f"Canvas: {WIDTH} x {HEIGHT}")
print()