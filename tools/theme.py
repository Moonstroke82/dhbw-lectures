"""Visual theme shared by the PPTX and HTML renderers.

Colours follow the DHBW corporate design (as used on dhbw.de: DHBW red
E2001A, DHBW grey 5C6971). The DHBW typeface (Generis) is licensed, so
the slides keep Calibri/Arial. When the official slide template is
supplied, change colours/fonts here and rebuild; slide sources do not change.
All sizes in points (1 in = 72 pt); slide is 16:9, 960 x 540 pt.
"""

import sys

SLIDE_W, SLIDE_H = 960, 540

COLORS = {
    "primary": "5C6971",   # DHBW grey: titles, headings, title/section slides
    "accent": "E2001A",    # DHBW red: rules, exercise badge, layer fills
    "optional": "2B2B2B",  # optional badge
    "text": "1E1E1E",
    "muted": "65737B",
    "light": "F2F3F4",     # card / code background
    "border": "D9DDDF",
    "white": "FFFFFF",
}

FONT = "Calibri"
FONT_MONO = "Consolas"
WEB_FONT = "Calibri, Carlito, 'Segoe UI', Arial, Helvetica, sans-serif"
WEB_FONT_MONO = "Consolas, Menlo, 'Courier New', monospace"

# Text is measured with Arial (wider than Calibri) so slides also fit
# in browsers that fall back to Arial/Helvetica (e.g. macOS without Office).
if sys.platform == "darwin":  # Menlo is wider than Consolas, so code still fits on Windows
    MEASURE_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
    MEASURE_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    MEASURE_MONO = "/System/Library/Fonts/Menlo.ttc"
else:
    MEASURE_REGULAR = "C:/Windows/Fonts/arial.ttf"
    MEASURE_BOLD = "C:/Windows/Fonts/arialbd.ttf"
    MEASURE_MONO = "C:/Windows/Fonts/consola.ttf"

# Regions (x, y, w, h)
TITLE = (43, 26, 874, 52)
RULE_Y = 84
BODY = (43, 100, 874, 392)
FOOTER_Y = 510

TITLE_SIZE = 28
BASE_SIZES = [24, 22, 20, 18, 16, 14]
REF_SIZES = [16, 14, 13, 12, 11]
MIN_SIZE = 11
SOURCE_SIZE = 10
FOOTER_SIZE = 9

LINE_HEIGHT = 1.2
ITEM_SPACING = 0.35
BLOCK_GAP = 0.7
BULLET_INDENT = 24
GAP = 14
TITLE_GAP = 4
BOX_PAD = 9
CELL_PAD = 4
CALLOUT_BAR = 5
LAYER_GAP = 4
SOURCE_GAP = 8
