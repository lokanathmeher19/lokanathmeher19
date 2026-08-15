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
LOCATION = "India"


# ============================================================
# CARD SIZE
# ============================================================

WIDTH = 650
HEIGHT = 500


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
height="496"
rx="16"
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

<line
x1="3"
y1="46"
x2="647"
y2="46"
stroke="#30363d"
stroke-width="1"
/>


<!-- ========================================================
     MAC BUTTONS
     ======================================================== -->

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


<!-- ========================================================
     TERMINAL TITLE
     ======================================================== -->

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


<!-- ========================================================
     WHOAMI
     ======================================================== -->

<text
x="30"
y="82"
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
x="30"
y="120"
font-family="Consolas, Courier New, monospace"
font-size="30"
font-weight="700"
fill="#d8dee9"
>
{esc(NAME)}
</text>


<!-- ========================================================
     USERNAME
     ======================================================== -->

<text
x="30"
y="149"
font-family="Consolas, Courier New, monospace"
font-size="16"
fill="#8b949e"
>
{esc(USERNAME)}
</text>


<!-- ========================================================
     SEPARATOR
     ======================================================== -->

<line
x1="30"
y1="173"
x2="620"
y2="173"
stroke="#30363d"
stroke-width="1"
/>


<!-- ========================================================
     ROLE
     ======================================================== -->

<text
x="30"
y="211"
font-family="Consolas, Courier New, monospace"
font-size="14"
font-weight="700"
fill="#58a6ff"
>
ROLE
</text>

<text
x="125"
y="211"
font-family="Consolas, Courier New, monospace"
font-size="14"
fill="#d8dee9"
>
{esc(ROLE)}
</text>


<!-- ========================================================
     STACK
     ======================================================== -->

<text
x="30"
y="251"
font-family="Consolas, Courier New, monospace"
font-size="14"
font-weight="700"
fill="#bc8cff"
>
STACK
</text>

<text
x="125"
y="251"
font-family="Consolas, Courier New, monospace"
font-size="14"
fill="#d8dee9"
>
{esc(STACK)}
</text>


<!-- ========================================================
     TOOLS
     ======================================================== -->

<text
x="30"
y="291"
font-family="Consolas, Courier New, monospace"
font-size="14"
font-weight="700"
fill="#3fb950"
>
TOOLS
</text>

<text
x="125"
y="291"
font-family="Consolas, Courier New, monospace"
font-size="14"
fill="#d8dee9"
>
{esc(TOOLS)}
</text>


<!-- ========================================================
     DATABASE
     ======================================================== -->

<text
x="30"
y="331"
font-family="Consolas, Courier New, monospace"
font-size="14"
font-weight="700"
fill="#58a6ff"
>
DATABASE
</text>

<text
x="125"
y="331"
font-family="Consolas, Courier New, monospace"
font-size="14"
fill="#d8dee9"
>
{esc(DATABASE)}
</text>


<!-- ========================================================
     FOCUS
     ======================================================== -->

<text
x="30"
y="371"
font-family="Consolas, Courier New, monospace"
font-size="14"
font-weight="700"
fill="#bc8cff"
>
FOCUS
</text>

<text
x="125"
y="371"
font-family="Consolas, Courier New, monospace"
font-size="14"
fill="#d8dee9"
>
{esc(FOCUS)}
</text>


<!-- ========================================================
     LOCATION
     ======================================================== -->

<text
x="30"
y="411"
font-family="Consolas, Courier New, monospace"
font-size="14"
font-weight="700"
fill="#d29922"
>
LOCATION
</text>

<text
x="125"
y="411"
font-family="Consolas, Courier New, monospace"
font-size="14"
fill="#d8dee9"
>
{esc(LOCATION)}
</text>


<!-- ========================================================
     FOOTER
     ======================================================== -->

<text
x="30"
y="458"
font-family="Consolas, Courier New, monospace"
font-size="13"
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
print()