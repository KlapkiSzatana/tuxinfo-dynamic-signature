
from pathlib import Path
import json
from xml.sax.saxutils import escape
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent

HEIGHT = 75
MIN_WIDTH = 360

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def measure(text, font):
    return font.getlength(str(text))


def svg_text(x, y, text, size, color, bold=False, anchor="start"):
    if not text:
        return ""

    weight = "700" if bold else "400"

    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="DejaVu Sans, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" '
        f'fill="{color}" text-anchor="{anchor}">'
        f'{escape(str(text))}</text>'
    )



def main():
    cfg = json.loads(
        (ROOT / "config.json").read_text(encoding="utf-8")
    )

    fg = cfg.get("foreground", "#1D2933")
    muted = cfg.get("muted", "#788A98")
    accent = cfg.get("accent", "#55A9D8")
    footer_color = cfg.get("footer_color", "#1793D1")

    label = str(cfg.get("label", "TERAZ"))
    title = str(cfg.get("title", "Tytuł"))
    subtitle = str(cfg.get("subtitle", ""))

    right_line1 = str(cfg.get("status", "")).strip()
    right_line2 = str(cfg.get("right_line2", "")).strip()
    footer = str(cfg.get("footer", "TUXINFO • PERSONAL STATUS"))

    label_font = load_font(10, True)
    title_font = load_font(22, True)
    subtitle_font = load_font(12)
    right_font = load_font(10, True)
    footer_font = load_font(10, True)

    # Szerokość obliczana na podstawie treści
    left_width = max(
        measure(label, label_font),
        measure(title, title_font),
        measure(subtitle, subtitle_font),
        150
    )

    right_width = max(
        measure(right_line1, right_font),
        measure(right_line2, right_font),
        measure(footer, footer_font),
        120
    )

    # Minimalna szerokość i proporcje kolumn
    WIDTH = max(
        700,
        int((left_width + right_width + 100) / 0.95)
    )

    HEIGHT = 75
    split = int(WIDTH * 0.60)

    left_x = 27
    right_edge = WIDTH - 16

    # SVG
    elements = []

    # Lewa kolumna
    elements.append(svg_text(
        left_x, 18, label, 10, accent, True
    ))

    elements.append(svg_text(
        left_x, 47, title, 22, fg, True
    ))

    elements.append(svg_text(
        left_x, 64, subtitle, 12, muted
    ))

    # Piorun - duże, ukośne przecięcie
    # Rozciągnięte na niemal całą wysokość grafiki
    lightning = [
        (split - 5, 0),
        (split + 8, 0),
        (split - 1, 28),
        (split + 12, 28),
        (split - 9, 75),
        (split - 3, 42),
        (split - 15, 42)
    ]

    points = " ".join(
        f"{x},{y}" for x, y in lightning
    )

    elements.append(
        f'<polygon points="{points}" fill="{accent}"/>'
    )

    # Prawa kolumna
    elements.append(svg_text(
        right_edge, 25,
        right_line1, 10, footer_color, True, "end"
    ))

    elements.append(svg_text(
        right_edge, 41,
        right_line2, 10, footer_color, True, "end"
    ))

    elements.append(svg_text(
        right_edge, 64,
        footer, 10, footer_color, True, "end"
    ))

    # SVG rozciąga się na całą dostępną szerokość.
    # viewBox zachowuje proporcje i umożliwia skalowanie.
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="100%"
     height="75"
     viewBox="0 0 {WIDTH} {HEIGHT}"
     preserveAspectRatio="none">

    <title>{escape(title)}</title>

    {''.join(elements)}

</svg>
'''

    (ROOT / "signature.svg").write_text(
        svg,
        encoding="utf-8"
    )

    link = str(cfg.get("link", "")).strip()

    (ROOT / "signature-link.txt").write_text(
        link + "\n",
        encoding="utf-8"
    )

    print(f"Generated signature.svg ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
