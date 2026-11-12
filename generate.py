
from pathlib import Path
import json
from xml.sax.saxutils import escape
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent

WIDTH = 600
HEIGHT = 65

def load_font(size, bold=False):
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )

    if Path(path).exists():
        return ImageFont.truetype(path, size)

    return ImageFont.load_default()


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

    label = cfg.get("label", "TERAZ")
    title = cfg.get("title", "Tytuł")
    subtitle = cfg.get("subtitle", "")

    right_line1 = cfg.get("status", "")
    right_line2 = cfg.get("right_line2", "")
    footer = cfg.get("footer", "TUXINFO • PERSONAL STATUS")

    # Podział kolumn
    split = 385
    left_x = 27
    right_x = 680

    elements = []

    # Lewy akcent
    elements.append(
        f'<rect x="12" y="12" width="4" height="51" '
        f'rx="2" fill="{accent}"/>'
    )

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

    # Pionowy separator
    elements.append(
        f'<rect x="{split}" y="12" width="1" height="51" '
        f'fill="{accent}" opacity="0.65"/>'
    )

    # Prawa kolumna
    elements.append(svg_text(
        right_x, 25, right_line1,
        10, footer_color, True, "end"
    ))

    elements.append(svg_text(
        right_x, 41, right_line2,
        10, footer_color, True, "end"
    ))

    elements.append(svg_text(
        right_x, 64, footer,
        10, footer_color, True, "end"
    ))

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

    <title>{escape(str(title))}</title>

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
