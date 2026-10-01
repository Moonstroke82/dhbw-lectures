"""Visual theme shared by the PPTX and HTML renderers.

Placeholder look until the official slide template is supplied: change
colours/fonts here and rebuild; slide sources do not need to change.
All sizes in points (1 in = 72 pt); slide is 16:9, 960 x 540 pt.
"""

SLIDE_W, SLIDE_H = 960, 540

COLORS = {
    "primary": "1F3A5F",   # titles, headings
    "accent": "2A9D8F",    # rules, exercise badge, layer fills
    "optional": "E76F51",  # optional badge
    "text": "222222",
    "muted": "6B7280",
    "light": "F1F5F9",     # card / code background
    "border": "CBD5E1",
    "white": "FFFFFF",
}

FONT = "Calibri"
FONT_MONO = "Consolas"
WEB_FONT = "Calibri, Carlito, 'Segoe UI', Arial, Helvetica, sans-serif"
WEB_FONT_MONO = "Consolas, Menlo, 'Courier New', monospace"

# Text is measured with Arial (wider than Calibri) so slides also fit
# in browsers that fall back to Arial/Helvetica (e.g. macOS without Office).
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
