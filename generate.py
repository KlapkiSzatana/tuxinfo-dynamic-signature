#!/usr/bin/env python3
"""Generate a clean, minimalist forum signature PNG from config.json."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 700, 150

def load_font(size, bold=False):
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

def fit_text(draw, text, font, max_width):
    text = str(text)
    while text and draw.textbbox((0, 0), text, font=font)[2] > max_width:
        text = text[:-2] + "…" if len(text) > 2 else text[:-1]
    return text

def main():
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    bg = config.get("background", "#f5f6f4")
    fg = config.get("foreground", "#202522")
    muted = config.get("muted", "#737b76")
    accent = config.get("accent", "#4f8a70")

    image = Image.new("RGB", (WIDTH, HEIGHT), bg)
    draw = ImageDraw.Draw(image)

    # Thin frame and restrained accent marker
    draw.rounded_rectangle((1, 1, WIDTH - 2, HEIGHT - 2), radius=16,
                           outline="#dfe3df", width=2)
    draw.rounded_rectangle((0, 0, 8, HEIGHT), radius=4, fill=accent)

    label_font = load_font(14, True)
    title_font = load_font( thirty := 30, True)
    subtitle_font = load_font(17)
    footer_font = load_font(11, True)
    status_font = load_font(13, True)

    left = 34
    label = fit_text(draw, config.get("label", "TERAZ"), label_font, 620)
    draw.text((left, 24), label, font=label_font, fill=accent)

    title = fit_text(draw, config.get("title", "Tytuł"), title_font, 620)
    draw.text((left, 49), title, font=title_font, fill=fg)

    subtitle = fit_text(draw, config.get("subtitle", ""), subtitle_font, 620)
    if subtitle:
        draw.text((left, 91), subtitle, font=subtitle_font, fill=muted)

    status = fit_text(draw, config.get("status", ""), status_font, 250)
    if status:
        status_box = draw.textbbox((0, 0), status, font=status_font)
        pill_w = status_box[2] + 24
        draw.rounded_rectangle((left, 119, left + pill_w, 141),
                               radius=11, fill="#e7eee9")
        draw.text((left + 12, 122), status, font=status_font, fill=accent)

    footer = fit_text(draw, config.get("footer", "TUXINFO"), footer_font, 240)
    footer_width = draw.textbbox((0, 0), footer, font=footer_font)[2]
    draw.text((WIDTH - footer_width - 25, 124), footer,
              font=footer_font, fill=muted)

    image.save(ROOT / "signature.png", format="PNG", optimize=True)
    link = str(config.get("link", "")).strip()
    (ROOT / "signature-link.txt").write_text(link + "\n", encoding="utf-8")
    print(f"Generated signature.png ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    main()
