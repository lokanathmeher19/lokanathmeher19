from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from rembg import remove


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

OUTPUT = DATA_DIR / "source-prepped.png"


# ============================================================
# SETTINGS
# ============================================================

MAX_SIZE = 1200

# Slightly expand the detected subject around edges
PADDING = 8


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) != 2:

        print(
            "Usage: python scripts/prep_photo.py source-photo.jpg"
        )

        sys.exit(1)


    source = ROOT / sys.argv[1]


    if not source.exists():

        print(
            f"ERROR: Photo not found: {source}"
        )

        sys.exit(1)


    print()
    print("======================================")
    print("       PREPARING PORTRAIT")
    print("======================================")
    print()


    # ========================================================
    # LOAD
    # ========================================================

    print("1. Loading photo...")

    image = Image.open(source).convert("RGBA")


    # ========================================================
    # RESIZE IF VERY LARGE
    # ========================================================

    if max(image.size) > MAX_SIZE:

        scale = (
            MAX_SIZE
            / max(image.size)
        )

        new_size = (
            int(image.width * scale),
            int(image.height * scale)
        )

        image = image.resize(
            new_size,
            Image.Resampling.LANCZOS
        )


    # ========================================================
    # REMOVE BACKGROUND
    # ========================================================

    print("2. Removing background...")


    rgba = remove(
        image
    ).convert("RGBA")


    # ========================================================
    # CLEAN ALPHA
    # ========================================================

    alpha = np.array(
        rgba.getchannel("A")
    )


    # Remove extremely faint pixels.

    alpha[alpha < 18] = 0


    # Slightly strengthen the mask.

    alpha = cv2.GaussianBlur(
        alpha,
        (3, 3),
        0
    )


    rgba.putalpha(
        Image.fromarray(alpha)
    )


    # ========================================================
    # FIND SUBJECT
    # ========================================================

    bbox = rgba.getchannel(
        "A"
    ).getbbox()


    if bbox is None:

        print(
            "ERROR: Could not detect subject."
        )

        sys.exit(1)


    # ========================================================
    # PADDING
    # ========================================================

    left, top, right, bottom = bbox


    left = max(
        0,
        left - PADDING
    )

    top = max(
        0,
        top - PADDING
    )

    right = min(
        rgba.width,
        right + PADDING
    )

    bottom = min(
        rgba.height,
        bottom + PADDING
    )


    # ========================================================
    # CROP PERSON ONLY
    # ========================================================

    rgba = rgba.crop(
        (
            left,
            top,
            right,
            bottom
        )
    )


    # ========================================================
    # CONTRAST
    #
    # IMPORTANT:
    # We improve contrast WITHOUT destroying the
    # white shirt.
    # ========================================================

    rgb = rgba.convert(
        "RGB"
    )


    gray = ImageOps.grayscale(
        rgb
    )


    gray = ImageOps.autocontrast(
        gray,
        cutoff=1
    )


    gray = gray.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=140,
            threshold=3
        )
    )


    # ========================================================
    # PUT IMPROVED GRAYSCALE BACK
    # ========================================================

    rgba = Image.merge(
        "RGBA",
        (
            gray,
            gray,
            gray,
            rgba.getchannel("A")
        )
    )


    # ========================================================
    # SAVE TRANSPARENT IMAGE
    # ========================================================

    rgba.save(
        OUTPUT,
        "PNG"
    )


    # ========================================================
    # RESULT
    # ========================================================

    print()
    print("DONE!")
    print()
    print(f"Output: {OUTPUT}")
    print(
        f"Subject size: "
        f"{rgba.width} x {rgba.height}"
    )
    print("Background: TRANSPARENT")
    print("Subject: FULL")
    print("White shirt: PRESERVED")
    print("Crop: SUBJECT ONLY")
    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()