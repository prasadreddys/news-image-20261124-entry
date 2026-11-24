#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a one-page newspaper front page.

Fixed text, colours and geometry. No network, no clock, no randomness,
so every run draws the same pixels. Run: python3 draw_image.py
Writes entry.png next to this file (1024x1024, PNG).
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

PAPER = (247, 242, 232)
NAVY = (16, 39, 63)
NAVY_LT = (28, 58, 88)
GOLD = (201, 162, 39)
GOLD_DK = (176, 138, 24)
RED = (176, 42, 42)
INK = (26, 26, 26)
MUTED = (85, 85, 85)
CARD = (255, 255, 255)
SEA = (46, 111, 148)
SEA_DK = (30, 82, 112)
GREEN = (34, 139, 76)
GREEN_DK = (24, 105, 56)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color=RED):
    f = font(SANS_B, 15)
    draw.text((x, y), label, font=f, fill=color)
    return y + 22


def headline(draw, x, y, text, size, width, fill=INK, leading=None):
    f = font(SERIF_B, size)
    lines = wrap(draw, text, f, width)
    return text_block(draw, (x, y), lines, f, fill, leading or size + 5), lines


def body(draw, x, y, text, size, width, leading=None):
    f = font(SANS, size)
    lines = wrap(draw, text, f, width)
    return text_block(draw, (x, y), lines, f, INK, leading or size + 6), lines


def mine(draw, cx, cy, r=13):
    """Spiked naval mine: dark ball with eight spikes."""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (1, -1), (-1, 1), (-1, -1)):
        draw.line([(cx, cy), (cx + dx * (r + 8), cy + dy * (r + 8))],
                  fill=(20, 20, 20), width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 30, 30),
                 outline=(0, 0, 0))
    draw.ellipse([cx - 5, cy - 6, cx + 2, cy + 1], fill=(90, 90, 90))


def tanker(draw, x, y, w, h, burning=False):
    """Simple oil tanker: dark hull, pale deck block, funnel."""
    draw.rectangle([x, y, x + w, y + h], fill=(40, 48, 56))
    draw.rectangle([x, y - 16, x + w // 3, y], fill=(220, 220, 210))
    draw.rectangle([x + w - 26, y - 26, x + w - 8, y], fill=(176, 42, 42))
    draw.line([(x, y + h), (x + w, y + h)], fill=(0, 0, 0), width=2)
    if burning:
        # Layered flames rising from the middle tanker's deck.
        deck_y = y
        for (fx, fw, fh, col) in ((0.50, 46, 58, (220, 60, 20)),
                                  (0.58, 34, 76, (245, 140, 20)),
                                  (0.47, 22, 44, (250, 205, 40))):
            px = x + w * fx
            draw.polygon([(px - fw // 2, deck_y),
                          (px - fw // 4, deck_y - fh // 2),
                          (px, deck_y - fh),
                          (px + fw // 4, deck_y - fh // 2),
                          (px + fw // 2, deck_y)], fill=col)


def lead_scene(draw, box):
    """Strait of Hormuz: shore, sea, three tankers, mines."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA)
    draw.rectangle([x0, y0, x1, y0 + 26], fill=(196, 164, 110))
    draw.text((x0 + 12, y0 + 4), "STRAIT OF HORMUZ",
              font=font(SANS_B, 14), fill=(90, 64, 20))
    for wy in (y0 + 70, y0 + 120, y0 + 170, y0 + 215):
        for wx in range(x0 + 10, x1 - 10, 46):
            draw.arc([wx, wy, wx + 34, wy + 12], 0, 180, fill=(200, 225, 240))
    tanker(draw, x0 + 22, y0 + 96, 120, 30)
    tanker(draw, x0 + 150, y0 + 108, 130, 32, burning=True)
    tanker(draw, x0 + 292, y0 + 96, 118, 30)
    mine(draw, x0 + 90, y0 + 205)
    mine(draw, x0 + 250, y0 + 218)
    mine(draw, x0 + 380, y0 + 200)
    draw.text((x0 + 12, y1 - 26), "IRAN SAYS 3 TANKERS HIT MINES — CLAIMS UNVERIFIED",
              font=font(SANS_B, 13), fill=(255, 255, 255))


def korea_scene(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(183, 222, 240))
    draw.polygon([(x0, y1), (x0 + 55, y0 + 42), (x0 + 130, y1)],
                 fill=(46, 139, 74))
    draw.polygon([(x0 + 40, y1), (x0 + 90, y0 + 66), (x0 + 150, y1)],
                 fill=(34, 110, 58))
    draw.text((x0 + 46, y1 - 22), "ULLEUNG", font=font(SANS_B, 13),
              fill=(255, 255, 255))
    draw.polygon([(x0 + 14, y0 + 30), (x0 + 62, y0 + 22),
                  (x0 + 92, y0 + 28), (x0 + 66, y0 + 36),
                  (x0 + 82, y0 + 48), (x0 + 58, y0 + 42),
                  (x0 + 26, y0 + 44), (x0 + 14, y0 + 38)],
                 fill=(40, 40, 40))
    draw.polygon([(x0 + 88, y0 + 26), (x0 + 104, y0 + 30),
                  (x0 + 88, y0 + 34)], fill=(40, 40, 40))
    cx, cy = x1 - 32, y0 + 30
    draw.polygon([(cx, cy - 24), (cx + 22, cy + 16), (cx - 22, cy + 16)],
                 fill=(245, 200, 20), outline=(150, 110, 0))
    draw.text((cx - 4, cy - 8), "!", font=font(SANS_B, 18), fill=(120, 60, 0))


def market_scene(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 245, 233))
    for gy in range(y0 + 24, y1 - 8, 26):
        draw.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(205, 225, 208))
    pts = [(x0 + 12, y1 - 26), (x0 + 48, y1 - 62), (x0 + 84, y1 - 50),
           (x0 + 118, y1 - 92), (x0 + 148, y1 - 108)]
    draw.line(pts, fill=GREEN_DK, width=5, joint="curve")
    draw.ellipse([pts[-1][0] - 6, pts[-1][1] - 6, pts[-1][0] + 6,
                  pts[-1][1] + 6], fill=GREEN)
    draw.text((x0 + 12, y0 + 8), "+4.7%", font=font(SANS_B, 26),
              fill=GREEN_DK)
    draw.text((x0 + 12, y0 + 42), "S&P 500", font=font(SANS_B, 14),
              fill=MUTED)


def estonia_scene(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(238, 238, 238))
    draw.rectangle([x0, y0, x1, y0 + 14], fill=(0, 114, 206))
    draw.rectangle([x0, y0 + 14, x1, y0 + 28], fill=(20, 20, 20))
    draw.rectangle([x0, y0 + 28, x1, y0 + 42], fill=(255, 255, 255))
    for gx in range(x0 + 22, x1 - 16, 18):
        draw.line([(gx, y0 + 56), (gx, y1 - 14)], fill=(90, 90, 90), width=5)
    draw.line([(x0 + 12, y0 + 56), (x1 - 12, y0 + 56)], fill=(60, 60, 60),
              width=5)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 12
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(200, 30, 30),
                 outline=(255, 255, 255), width=3)
    draw.line([(cx - 18, cy + 18), (cx + 18, cy - 18)], fill=(255, 255, 255),
              width=6)


def capitol_scene(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(226, 233, 240))
    cx = (x0 + x1) // 2
    draw.rectangle([x0 + 18, y1 - 34, x1 - 18, y1 - 14], fill=(210, 218, 228))
    for i in range(5):
        px = x0 + 30 + i * 26
        draw.rectangle([px, y1 - 62, px + 12, y1 - 34], fill=(255, 255, 255),
                       outline=(150, 160, 175))
    draw.rectangle([x0 + 22, y1 - 66, x1 - 22, y1 - 60], fill=(255, 255, 255),
                   outline=(150, 160, 175))
    draw.pieslice([cx - 40, y0 + 34, cx + 40, y0 + 114], 180, 360,
                  fill=(205, 214, 226), outline=(90, 105, 125))
    draw.rectangle([cx - 4, y0 + 18, cx + 4, y0 + 38], fill=(205, 214, 226),
                   outline=(90, 105, 125))
    draw.ellipse([cx - 6, y0 + 12, cx + 6, y0 + 24], fill=(205, 214, 226),
                 outline=(90, 105, 125))
    draw.rounded_rectangle([x0 + 8, y0 + 8, x0 + 86, y0 + 34], 6,
                           fill=NAVY)
    draw.text((x0 + 16, y0 + 13), "DEC 1", font=font(SANS_B, 16),
              fill=(255, 255, 255))


SCENES = {"korea": korea_scene, "market": market_scene,
          "estonia": estonia_scene, "capitol": capitol_scene}


def panel(draw, box, kicker_text, head, body_text, scene_key):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=(200, 195, 180), width=1)
    tx = x0 + 16
    y = kicker(draw, tx, y0 + 12, kicker_text)
    tw = 296
    y, _ = headline(draw, tx, y, head, 21, tw, leading=25)
    body(draw, tx, y + 4, body_text, 15, tw, leading=20)
    sx0 = x1 - 158
    draw.rectangle([sx0, y0 + 12, x1 - 12, y1 - 12], outline=(210, 205, 190))
    SCENES[scene_key](draw, (sx0, y0 + 12, x1 - 12, y1 - 12))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 112], fill=NAVY)
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF_B, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 12), title,
           font=tf, fill=(255, 255, 255))
    date = "TUESDAY  •  24 NOVEMBER 2026"
    df = font(SANS_B, 19)
    d.text(((W - d.textlength(date, font=df)) / 2, 76), date,
           font=df, fill=GOLD)
    d.rectangle([0, 112, W, 118], fill=GOLD)
    sub = "THE DAY'S WORLD NEWS — IN ONE IMAGE"
    sf = font(SANS, 15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 126), sub,
           font=sf, fill=MUTED)

    # Lead story
    lx0, ly0, lx1, ly1 = 24, 152, 1000, 452
    d.rectangle([lx0, ly0, lx1, ly1], fill=CARD,
                outline=(200, 195, 180), width=1)
    tx = lx0 + 20
    y = kicker(d, tx, ly0 + 14, "LEAD  —  IRAN  •  STRAIT OF HORMUZ")
    y, _ = headline(d, tx, y, "THREE TANKERS HIT MINES OFF HORMUZ",
                    33, 500, leading=38)
    body(d, tx, y + 8,
         "Iran's Revolutionary Guard says three oil tankers hit naval "
         "mines and caught fire — one off the south coast, two in the "
         "east — while under US air escort. The claims are unverified; "
         "US Central Command has not responded.",
         17, 500, leading=23)
    d.text((tx, ly1 - 34), "IRAN SAYS THE STRAIT IS CLOSED TO “VIOLATING” SHIPS",
           font=font(SANS_B, 13), fill=MUTED)
    lead_scene(d, (592, ly0 + 14, lx1 - 16, ly1 - 16))

    # Four panels, two by two
    gy, ph, pw = 464, 156, 476
    panel(d, (24, gy, 24 + pw, gy + ph), "KOREA  •  ULLEUNG ISLAND",
          "SHELTER ALERT ON ULLEUNG ISLAND",
          "Five Russian jets enter the defence zone; Seoul's 07:52 alert "
          "is lifted in minutes. No breach of airspace.", "korea")
    panel(d, (524, gy, 524 + pw, gy + ph), "MARKETS  •  WALL STREET",
          "WALL STREET ROARS BACK",
          "S&P 500 +4.7%, Nasdaq +6.5% as Nvidia brings back Jensen "
          "Huang; shares surge 31%.", "market")
    panel(d, (24, gy + ph + 12, 24 + pw, gy + 2 * ph + 12),
          "EUROPE  •  ESTONIA", "MOSCOW WARNS ESTONIA",
          "Russia accuses Tallinn of acts “on the verge of open war” as "
          "Estonia shuts its border from 1 Dec.", "estonia")
    panel(d, (524, gy + ph + 12, 524 + pw, gy + 2 * ph + 12),
          "USA  •  CONGRESS", "GOMEZ QUITS AFTER ETHICS FINDING",
          "Rep. Jimmy Gomez resigns from 1 Dec after the Ethics panel "
          "finds “substantial evidence” of sexual misconduct.", "capitol")

    # Also today
    ax0, ay0, ax1, ay1 = 24, 800, 1000, 964
    d.rectangle([ax0, ay0, ax1, ay1], fill=CARD,
                outline=(200, 195, 180), width=1)
    d.text((ax0 + 16, ay0 + 10), "ALSO TODAY",
           font=font(SANS_B, 17), fill=NAVY)
    d.line([(ax0 + 16, ay0 + 38), (ax1 - 16, ay0 + 38)], fill=GOLD, width=2)
    items = [
        "Zaporizhzhia — Russian strike kills 2, wounds 44.",
        "NATO vows to defend space after a report of a Russian "
        "nuclear-armed satellite.",
        "Solomon Islands tells China it will end its 2022 security pact.",
        "Reports say hacked Russian data puts war deaths near 500,000.",
        "Chess: Gukesh v Sindarov opens in Geneva — youngest title "
        "match ever, both 20.",
        "2031 Women's World Cup to US, Mexico, Costa Rica and Jamaica; "
        "UK gets 2035.",
    ]
    col_w, row_h = 472, 34
    for i, item in enumerate(items):
        cx = ax0 + 16 + (i % 2) * (col_w + 8)
        cy = ay0 + 48 + (i // 2) * row_h
        d.ellipse([cx, cy + 5, cx + 8, cy + 13], fill=GOLD_DK)
        lines = wrap(d, item, font(SANS, 14), col_w - 18)
        text_block(d, (cx + 16, cy), lines[:2], font(SANS, 14), INK, 17)

    # Footer
    foot = ("As reported on 24 Nov 2026  —  Reuters  •  AP  •  Yonhap  •  "
            "Al Jazeera  •  Japan Times  •  Wall Street Journal")
    ff = font(SANS, 14)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 974), foot,
           font=ff, fill=MUTED)
    d.text(((W - d.textlength("Drawn from live reporting. Claims marked unverified are unconfirmed.", font=font(SANS, 12))) / 2, 998),
           "Drawn from live reporting. Claims marked unverified are unconfirmed.",
           font=font(SANS, 12), fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
