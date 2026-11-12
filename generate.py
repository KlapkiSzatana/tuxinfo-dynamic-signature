
from pathlib import Path
import json
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent

WIDTH = 600
HEIGHT = 65


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

    elements = []

    # Lewy akcent
    elements.append(
        f'<rect x="12" y="10" width="4" height="45" '
        f'rx="2" fill="{accent}"/>'
    )

    # Lewa kolumna
    elements.append(svg_text(
        27, 16, label, 10, accent, True
    ))

    elements.append(svg_text(
        27, 42, title, 22, fg, True
    ))

    elements.append(svg_text(
        27, 58, subtitle, 12, muted
    ))

    # Prawa kolumna
    elements.append(svg_text(
        588, 19, right_line1,
        10, fg, True, "end"
    ))

    elements.append(svg_text(
        588, 35, right_line2,
        10, muted, True, "end"
    ))

    elements.append(svg_text(
        588, 58, footer,
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
