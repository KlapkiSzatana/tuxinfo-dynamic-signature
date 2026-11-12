
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 700, 75

def load_font(size, bold=False):
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
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
    cfg = json.loads(
        (ROOT / "config.json").read_text(encoding="utf-8")
    )

    fg = cfg.get("foreground", "#202522")
    muted = cfg.get("muted", "#737b76")
    accent = cfg.get("accent", "#4f8a70")
    footer_color = cfg.get("footer_color", "#1793D1")

    # Przezroczyste tło
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    label_font = load_font(10, True)
    title_font = load_font(22, True)
    subtitle_font = load_font(12)
    #status_font = load_font(10, True)

    x = 12

    # Delikatny zielony akcent
    draw.rounded_rectangle(
        (x, 12, x + 4, 63),
        radius=2,
        fill=accent
    )
    x += 15

    label = fit_text(
        draw, cfg.get("label", "TERAZ"), label_font, 640
    )
    draw.text((x, 10), label, font=label_font, fill=accent)

    title = fit_text(
        draw, cfg.get("title", "Tytuł"), title_font, 640
    )
    draw.text((x, 25), title, font=title_font, fill=fg)

    subtitle = fit_text(
        draw, cfg.get("subtitle", ""), subtitle_font, 640
    )
    if subtitle:
        draw.text((x, 53), subtitle, font=subtitle_font, fill=muted)

    #status = str(cfg.get("status", "")).strip()

    #if status:
        #status_width = draw.textbbox(
            #(0, 0), status, font=status_font
        #)[2]

        #pill_x = WIDTH - status_width - 32

        #draw.rounded_rectangle(
            #(pill_x, 28, WIDTH - 12, 48),
            #radius=10,
            #fill=(231, 238, 233, 230)
        #)

        #draw.text(
            #(pill_x + 10, 33),
            #status,
            #font=status_font,
            #fill=accent
        #)

    footer = fit_text(
        draw,
        cfg.get("footer", "TUXINFO • PERSONAL STATUS"),
        load_font(10, True),
        250
    )
    
    footer_width = draw.textbbox(
        (0, 0), footer, font=load_font(10, True)
    )[2]
    
    draw.text(
        (WIDTH - footer_width - 12, 55),
        footer,
        font=load_font(10, True),
        fill=footer_color
    )

    image.save(
        ROOT / "signature.png",
        format="PNG",
        optimize=True
    )

    link = str(cfg.get("link", "")).strip()

    (ROOT / "signature-link.txt").write_text(
        link + "\n",
        encoding="utf-8"
    )

    print(f"Generated transparent signature.png ({WIDTH}x{HEIGHT})")

if __name__ == "__main__":
    main()
