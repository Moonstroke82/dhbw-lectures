"""Combine preview PNGs of a deck into contact sheets for a quick visual check.

Usage: python tools/contact_sheet.py build/preview/<course>/<session>  -> sheet-1.png, sheet-2.png ...
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

d = Path(sys.argv[1])
files = sorted(d.glob("slide-*.png"))
cols, per, tw, th = 3, 12, 800, 450
for k in range(0, len(files), per):
    chunk = files[k:k + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), "white")
    for i, f in enumerate(chunk):
        im = Image.open(f).convert("RGB").resize((tw - 6, th - 6))
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x + 3, y + 3))
        ImageDraw.Draw(sheet).rectangle([x + 2, y + 2, x + tw - 3, y + th - 3], outline="#999")
    sheet.save(d / f"sheet-{k // per + 1}.png")
    print(d / f"sheet-{k // per + 1}.png")
