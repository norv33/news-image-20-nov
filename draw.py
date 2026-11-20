#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image (1024x1024 PNG).

Style: wire-desk poster -- white paper, thick black rules, red accent,
big coloured story numbers, a 2x3 grid of news cards, and a black
"by the numbers" strip. Original artwork drawn with PIL primitives.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

BLACK = (12, 12, 12)
WHITE = (255, 255, 255)
PAPER = (250, 248, 243)
RED = (200, 16, 46)
GREY = (90, 90, 90)
INK = (30, 30, 30)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("01", "POLITICS", (200, 16, 46),
     "TRUMP PUSHES IRAN WAR DECISION TO 2027",
     "The US president says there is no rush and he will "
     "\u201csee what happens\u201d after 1 January."),
    ("02", "EUROPE", (23, 84, 160),
     "EUROPE READY TO TALK TO RUSSIA ON UKRAINE",
     "European leaders say they are open to negotiations "
     "to end the war, after a summit in Berlin."),
    ("03", "WEATHER", (0, 122, 110),
     "CYCLONE AKVAN: 300,000 EVACUATED IN INDIA",
     "A severe storm bears down on the Odisha coast; "
     "423 rescue teams deployed as landfall nears."),
    ("04", "CULTURE", (122, 62, 160),
     "GTA 6 SALES PASS $1.8 BILLION",
     "Rockstar\u2019s blockbuster overtakes The Odyssey\u2019s "
     "global box-office run within days of launch."),
    ("05", "ART", (196, 106, 0),
     "VAN GOGH SELLS FOR A RECORD $190.4M",
     "A painting with a disputed Nazi-era past fetches "
     "a record price at auction."),
    ("06", "MIGRATION", (40, 90, 60),
     "DOZENS MISSING AS MIGRANT BOAT SINKS",
     "A boat carrying about 100 people capsizes off "
     "Senegal; four bodies recovered so far."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # ---- Masthead -------------------------------------------------
    title_f = font(SANS_BOLD, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 26), title, font=title_f, fill=BLACK)
    d.rectangle([mx, 102, W - mx, 110], fill=RED)
    date_f = font(SANS_BOLD, 42)
    date = "FRIDAY, 20 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 122), date, font=date_f, fill=RED)
    d.rectangle([mx, 178, W - mx, 182], fill=BLACK)

    # ---- Story grid: 2 cols x 3 rows ------------------------------
    gx, gy = mx, 198
    gw = (W - 2 * mx - 16) // 2          # 476
    gh = 216
    gap = 16
    tag_f = font(SANS_BOLD, 17)
    num_f = font(SANS_BOLD, 46)
    head_f = font(SANS_BOLD, 25)
    body_f = font(SANS, 19)

    for i, (num, tag, color, head, body) in enumerate(STORIES):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        d.rectangle([x, y, x + gw, y + gh], fill=WHITE,
                    outline=BLACK, width=3)
        # accent top bar
        d.rectangle([x + 3, y + 3, x + gw - 3, y + 11], fill=color)
        # tag
        d.text((x + 16, y + 22), tag, font=tag_f, fill=color)
        # big number, right of tag
        nw = d.textlength(num, font=num_f)
        d.text((x + gw - 16 - nw, y + 14), num, font=num_f, fill=color)
        # thin rule under tag row
        d.line([x + 16, y + 66, x + gw - 16, y + 66], fill=(200, 200, 200),
               width=2)
        # headline, wraps in remaining width
        text_w = gw - 32
        lines = wrap(d, head, head_f, text_w)[:2]
        hy = y + 78
        for ln in lines:
            d.text((x + 16, hy), ln, font=head_f, fill=INK)
            hy += 31
        # body
        blines = wrap(d, body, body_f, text_w)[:3]
        by = hy + 6
        for ln in blines:
            d.text((x + 16, by), ln, font=body_f, fill=(70, 70, 70))
            by += 25

    # ---- Also today ------------------------------------------------
    ay = gy + 3 * gh + 2 * gap + 12          # 890
    also_f = font(SANS, 16)
    also = ("ALSO TODAY:  India v New Zealand Test opens in Wellington  \u00b7  "
            "Haiti police kill 34 gang members in a Port-au-Prince raid")
    aw = d.textlength(also, font=also_f)
    assert aw <= W - 2 * mx, f"also-today line too wide: {aw}"
    d.text(((W - aw) / 2, ay), also, font=also_f, fill=GREY)

    # ---- By the numbers strip --------------------------------------
    sy = 928
    d.rectangle([0, sy, W, H], fill=BLACK)
    strip_f = font(SANS_BOLD, 20)
    strip = "BY THE NUMBERS"
    d.text((mx, sy + 12), strip, font=strip_f, fill=(255, 210, 60))
    facts_f = font(SANS, 19)
    facts = ("300,000 evacuated ahead of Cyclone Akvan   \u00b7   "
             "$1.8bn \u2014 GTA 6 sales   \u00b7   "
             "$190.4m \u2014 record Van Gogh   \u00b7   "
             "~100 aboard the Senegal boat   \u00b7   "
             "2027 \u2014 Trump\u2019s Iran decision")
    flines = wrap(d, facts, facts_f, W - 2 * mx)
    fy = sy + 42
    for ln in flines:
        d.text((mx, fy), ln, font=facts_f, fill=WHITE)
        fy += 25

    img.save(OUT, optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
