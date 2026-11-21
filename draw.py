#!/usr/bin/env python3
"""The World Today, v9 - Saturday 21 November 2026.
One 1024x1024 front page, 43 dated stories, 13 illustrated cards.
Drawn with Pillow. No network, no randomness, no clock.
v9 keeps the restored first-v5 design and the v7/v8 fixes (list shifted left
so stories 14-28 never touch 29-43; hero cards 186px tall so no body text
touches the bottom border) and fixes the last complaint: the red banner
headline and the black source strip no longer sit inside the hero pictures,
so pictures 1-3 are 100% visible. The banner text now lives in the red tag
line under each picture, and only the small stat badge stays in the picture,
top right. The globe picture's thermometer moved down so the badge does not
cover it. Tag-line widths were measured after rendering: the longest one is
296px against 313px available, so none of them wraps."""
import os
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
PAPER = (247, 241, 222)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (16, 42, 90)
TEAL = (0, 110, 110)
CREAM = (255, 252, 240)
DIM = (60, 60, 60)
FONTDIR = "/usr/share/fonts/truetype/dejavu"

def f(name, size):
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)

F_TITLE = f("DejaVuSerif-Bold.ttf", 62)
F_SUB = f("DejaVuSerif.ttf", 17)
F_S = f("DejaVuSans.ttf", 11)
F_SB = f("DejaVuSans-Bold.ttf", 11)
F_BIG = f("DejaVuSerif-Bold.ttf", 26)
F_BIGS = f("DejaVuSans.ttf", 10)
F_H = f("DejaVuSerif-Bold.ttf", 15)
F_HS = f("DejaVuSerif-Bold.ttf", 12)
F_B = f("DejaVuSans.ttf", 11)
F_BS = f("DejaVuSans.ttf", 10)
F_TAG = f("DejaVuSans-Bold.ttf", 10)
F_LIST = f("DejaVuSans.ttf", 10)
F_BADGE = f("DejaVuSans-Bold.ttf", 11)
F_BANNER = f("DejaVuSans-Bold.ttf", 14)
F_CAP = f("DejaVuSans.ttf", 9)

def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def centred(d, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((PAGE - w) / 2, y), text, font=font, fill=fill)

def badge(d, x, y, text, fill=(255, 255, 255), ink=RED):
    w = d.textlength(text, font=F_BADGE) + 10
    d.rectangle([x, y, x + w, y + 16], fill=fill, outline=ink, width=1)
    d.text((x + 5, y + 2), text, font=F_BADGE, fill=ink)

# ---------- pictures ----------
def pic(d, kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    cx, cy = x + w // 2, y + h // 2
    if kind == "globe":
        d.ellipse([x + 12, y + 8, x + 62, y + h - 8], fill=(70, 140, 200))
        d.ellipse([x + 26, y + 16, x + 44, y + 34], fill=(90, 180, 90))
        d.ellipse([x + 36, y + 44, x + 56, y + 62], fill=(90, 180, 90))
        d.rectangle([x + w - 34, y + 44, x + w - 26, y + h - 10], fill=RED)
        d.ellipse([x + w - 36, y + 40, x + w - 24, y + 52], fill=RED)
    elif kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        for bx in (x + 14, x + 52, x + 90):
            d.rectangle([bx, y + h - 34, bx + 26, y + h - 8], fill=(60, 60, 80))
            for wy in range(y + h - 30, y + h - 10, 6):
                d.rectangle([bx + 4, wy, bx + 8, wy + 3], fill=(255, 220, 80))
                d.rectangle([bx + 16, wy, bx + 20, wy + 3], fill=(255, 220, 80))
        for sx, sy in ((x + 30, y + 14), (x + 70, y + 26), (x + 105, y + 10)):
            d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 200, 40))
            d.line([sx, sy, sx + 14, sy + 12], fill=(255, 200, 40), width=2)
    elif kind == "kyiv":
        d.rectangle([x, y, x + w, y + h], fill=(30, 30, 50))
        for bx in (x + 16, x + 58, x + 100):
            d.rectangle([bx, y + h - 40, bx + 28, y + h - 8], fill=(70, 70, 95))
            for wy in range(y + h - 36, y + h - 12, 6):
                d.rectangle([bx + 4, wy, bx + 9, wy + 3], fill=(255, 220, 80))
                d.rectangle([bx + 17, wy, bx + 22, wy + 3], fill=(255, 220, 80))
        d.polygon([(x + 118, y + 8), (x + 132, y + 26), (x + 104, y + 26)], fill=(255, 140, 40))
        d.polygon([(x + 126, y + 26), (x + 136, y + 40), (x + 116, y + 40)], fill=(255, 180, 60))
        d.ellipse([x + 18, y + 10, x + 30, y + 22], fill=(255, 220, 80))
    elif kind == "quake":
        d.rectangle([x, y, x + w, y + h], fill=(240, 220, 190))
        pts = [(x + 6, cy), (x + 26, cy - 6), (x + 40, cy + 18), (x + 52, cy - 26),
               (x + 64, cy + 22), (x + 78, cy - 8), (x + 96, cy + 4), (x + w - 6, cy - 10)]
        d.line(pts, fill=RED, width=3)
        d.polygon([(x + w - 44, y + h - 22), (x + w - 30, y + h - 44), (x + w - 16, y + h - 22)], fill=(120, 90, 60))
        d.polygon([(x + 8, y + h - 22), (x + 20, y + h - 40), (x + 32, y + h - 22)], fill=(140, 140, 140))
    elif kind == "plane":
        d.rectangle([x, y, x + w, y + h], fill=(200, 225, 240))
        d.ellipse([cx - 34, cy - 10, cx + 34, cy + 10], fill=(255, 255, 255), outline=INK, width=2)
        d.polygon([(cx + 20, cy - 8), (cx + 44, cy - 16), (cx + 40, cy - 2)], fill=(255, 255, 255), outline=INK)
        d.polygon([(cx - 6, cy + 8), (cx + 10, cy + 22), (cx + 16, cy + 8)], fill=(255, 255, 255), outline=INK)
        d.ellipse([x + 10, y + 8, x + 26, y + 24], fill=(255, 255, 255))
        d.ellipse([x + 34, y + 16, x + 52, y + 32], fill=(255, 255, 255))
    elif kind == "mercury":
        d.rectangle([x, y, x + w, y + h], fill=(30, 30, 50))
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(180, 170, 150))
        d.ellipse([cx - 12, cy - 8, cx - 2, cy + 2], fill=(140, 130, 110))
        d.ellipse([cx + 6, cy + 6, cx + 14, cy + 14], fill=(140, 130, 110))
        for sx, sy in ((x + 14, y + 12), (x + 100, y + 16), (x + 60, y + 70)):
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    elif kind == "nato":
        d.rectangle([x, y, x + w, y + h], fill=(20, 60, 120))
        for i in range(5):
            sx = x + 16 + i * 20
            d.ellipse([sx - 4, cy - 4, sx + 4, cy + 4], fill=(255, 220, 80))
        d.polygon([(cx, y + 12), (cx + 8, cy + 6), (cx - 8, cy + 6)], fill=(255, 255, 255))
    elif kind == "f1":
        d.rectangle([x, y, x + w, y + h], fill=(40, 40, 40))
        d.line([(x + 8, y + h - 16), (x + 40, y + 20), (x + 80, y + h - 24), (x + w - 8, y + 16)], fill=(255, 255, 255), width=3)
        d.rectangle([cx - 14, cy - 8, cx + 14, cy + 8], fill=RED)
        d.text((cx - 7, cy - 7), "F1", font=F_TAG, fill=(255, 255, 255))
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(30, 130, 60))
        d.rectangle([x + 10, y + h - 26, x + w - 10, y + h - 8], fill=(120, 200, 90))
        d.rectangle([cx - 4, y + 12, cx + 4, y + 40], fill=(200, 160, 90))
        d.ellipse([cx - 14, y + 36, cx + 14, y + h - 4], fill=(200, 160, 90))
        d.ellipse([x + w - 26, y + 12, x + w - 14, y + 24], fill=RED)
    elif kind == "boat":
        d.rectangle([x, y, x + w, y + h], fill=(180, 210, 235))
        d.line([(x + 8, cy + 18), (x + w - 8, cy + 18)], fill=(40, 90, 160), width=3)
        d.polygon([(cx - 30, cy + 18), (cx + 30, cy + 18), (cx + 20, cy + 34), (cx - 20, cy + 34)], fill=(150, 90, 40))
        d.line([(cx, cy - 22), (cx, cy + 18)], fill=INK, width=2)
        d.polygon([(cx + 2, cy - 22), (cx + 2, cy + 8), (cx + 20, cy + 8)], fill=(255, 255, 255), outline=INK)
    elif kind == "bitcoin":
        d.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
        chart = [(x + 8, y + 18), (x + 32, y + 34), (x + 52, y + 22), (x + 76, y + 44), (x + w - 8, y + 54)]
        d.line(chart, fill=RED, width=3)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 180, 40))
        d.text((cx - 6, cy - 9), "B", font=F_TAG, fill=(255, 255, 255))
    elif kind == "drone":
        d.rectangle([x, y, x + w, y + h], fill=(90, 140, 180))
        d.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], fill=(60, 60, 60))
        d.ellipse([cx - 30, cy - 16, cx - 10, cy - 10], fill=(200, 200, 200))
        d.ellipse([cx + 10, cy - 16, cx + 30, cy - 10], fill=(200, 200, 200))
        d.line([(cx, cy + 8), (cx, cy + 26)], fill=(60, 60, 60), width=2)
    elif kind == "ai":
        d.rectangle([x, y, x + w, y + h], fill=(220, 230, 250))
        d.rectangle([x + 16, y + 14, x + w - 16, y + h - 14], fill=(255, 255, 255), outline=NAVY, width=2)
        d.text((x + 24, y + 22), "AI", font=F_BIG, fill=NAVY)
        d.line([(x + 20, y + h - 24), (x + 44, y + h - 34), (x + 64, y + h - 28), (x + w - 20, y + h - 40)], fill=TEAL, width=2)

# n, tag, strip colour, picture, banner, badge, caption, headline, summary, status
HEROES = [
    dict(n=1, tag="ANTALYA, TURKIYE - CLIMATE", col=TEAL, kind="globe",
         banner="COP31: OVERTIME", stat="DAY 13 OF 12", cap="Talks ongoing · AFP",
         head="COP31 runs into overtime with no deal",
         body="Talks pass the Friday deadline; a third draft is due Saturday morning, still with no mention of fossil fuels. (AP, Al Jazeera)", st="OFFICIAL"),
    dict(n=2, tag="RIYADH - CONFLICT", col=NAVY, kind="missile",
         banner="RIYADH: 3 DOWNED", stat="3 INTERCEPTED", cap="Coalition says · Reuters",
         head="Coalition downs three missiles over Riyadh",
         body="Air defences destroy three ballistic missiles fired at the capital early Saturday, a third straight night of alerts. (Reuters)", st="OFFICIAL"),
    dict(n=3, tag="KYIV & KRYVYI RIH - WAR", col=RED, kind="kyiv",
         banner="UKRAINE: STRIKES", stat="42 HURT", cap="Officials · Kyiv Post",
         head="Russia hits Kyiv again as Kryvyi Rih counts its dead",
         body="Dawn missile hits set homes ablaze in Kyiv's Podil; a double-tap strike in Kryvyi Rih killed a boy and a medic, 42 hurt. (Kyiv Post)", st="REPORTED"),
]
SMALLS = [
    dict(n=4, tag="JUNIN, PERU", col=(140, 110, 20), kind="quake",
         stat="M6.7", head="Magnitude 6.7 earthquake shakes central Peru",
         body="The deep quake struck at 00:09 GMT near Junin, felt in Lima. No deaths reported. (USGS)", st="OFFICIAL"),
    dict(n=5, tag="DAVAO", col=(20, 60, 140), kind="plane",
         stat="146 SAFE", head="Jet lands safely after engine-fire alert",
         body="Air Niugini 767 diverts after midnight; all 146 aboard safe. (AP)", st="OFFICIAL"),
    dict(n=6, tag="MERCURY", col=(80, 80, 80), kind="mercury",
         stat="8 YEARS", head="BepiColombo reaches Mercury",
         body="Thrusters fire at 19:24 CET tonight after an 8-year voyage. (ESA)", st="OFFICIAL"),
    dict(n=7, tag="WARSAW", col=NAVY, kind="nato",
         stat="DAY AFTER", head="Rutte flies to Warsaw for NATO talks",
         body="NATO chief visits a day after the airspace incursion. (AP)", st="OFFICIAL"),
    dict(n=8, tag="LAS VEGAS", col=(40, 40, 40), kind="f1",
         stat="TONIGHT", head="Las Vegas GP qualifying today",
         body="Grid decided tonight under the lights; Russell fastest in final practice. (F1)", st="OFFICIAL"),
    dict(n=9, tag="WELLINGTON", col=(30, 120, 60), kind="cricket",
         stat="486-4", head="Rahul hits 136 as India fight back",
         body="India 466/4 lead NZ by 118 at stumps on day 3. (ESPNcricinfo)", st="OFFICIAL"),
    dict(n=10, tag="BAYELSA", col=(30, 120, 60), kind="boat",
         stat="AT LEAST 4", head="Nigeria funeral boat capsizes",
         body="At least four dead, two of them children, in Bayelsa. (Reuters)", st="OFFICIAL"),
    dict(n=11, tag="WORLD", col=(140, 110, 20), kind="bitcoin",
         stat="$58,983", head="Bitcoin trades below $59,000",
         body="Down 3.9% in 24 hours; ether $1,625. S&P in correction. (CoinGecko)", st="OFFICIAL"),
    dict(n=12, tag="HORMUZ", col=(110, 50, 140), kind="drone",
         stat="No. 58", head="Iran says it shot down a US MQ-9",
         body="The 58th claim, no US confirmation. (Al Jazeera)", st="CLAIM"),
    dict(n=13, tag="CANBERRA", col=TEAL, kind="ai",
         stat="11 DAYS", head="Australia and China agree to AI talks",
         body="Albanese ends an 11-day trip with a deal on AI. (ABC)", st="OFFICIAL"),
]
MORE = [
    "14 Kyiv: Zelensky warns Crimea bridge 'will not stay' (NBC)",
    "15 Copenhagen: Russian attack expelled over a plot (Al Jazeera)",
    "16 Antalya: EU warns COP31 risks a 'fossil summit' (AFP)",
    "17 Antalya: Panama threatens to block the climate text (Al Jazeera)",
    "18 Jakarta: PLN signs clean-power deals (Antara)",
    "19 Yemen: Houthis threaten Jeddah and Red Sea ports (Al Jazeera)",
    "20 Washington: Vance speaks on the Iran strikes (Reuters)",
    "21 Washington: Lawmaker threatens SpaceX funding (CNN)",
    "22 Texas: Execution of a man of 70 takes 63 minutes (ABC)",
    "23 Los Angeles: Jury convicts man of starting Palisades fire (ABC)",
    "24 Missouri: Judge approves $7.25bn Roundup settlement (AFP)",
    "25 Vancouver: Canada rests defence in youth climate trial (AFP)",
    "26 Pyongyang: Kim tours factories after no Trump meeting (AFP)",
    "27 Sejong: Freight train derails, no one hurt (Korea Herald)",
    "28 Taipei: Budget and cash payout are passed (Taipei Times)",
    "29 Bangkok: Six-point plan on arsenic in two rivers (The Nation)",
    "30 New Delhi: Pakistani minister joins SCO forum in India (Dawn)",
    "31 Myanmar: Rights groups urge sanctions after court ruling (AP)",
    "32 Eastern India: Rain alerts as Akvan's remnant passes (ETV)",
    "33 Port Louis: African ratings agency talks to 15 states (Al Jazeera)",
    "34 Melbourne: Cummins keeps the Australian captaincy (ABC)",
    "35 Turin: Medvedev meets Zverev in the semi-finals (ATP)",
    "36 Seoul: South Korea moves to impeach chief justice (Reuters)",
    "37 Kathmandu: Nepal PM Balendra Shah heads to India (PTI)",
    "38 Nairobi: Kenya begins onshore crude drilling in Turkana (Reuters)",
    "39 Dar es Salaam: Tanzania's Lissu convicted of sedition (AFP)",
    "40 Johannesburg: Nearly 600 women killed in 3 months (Reuters)",
    "41 Baghdad: Basra power-plant fire kills at least 4 (AP)",
    "42 Madrid: Spain heads to 29 Nov election (Reuters)",
    "43 Tallinn: Estonia closes Russia border crossings (AP)",
]

def hero_card(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=CREAM)
    pic(d, c["kind"], x + 1, y + 1, w - 2, 78)
    badge(d, x + w - 8 - (d.textlength(c["stat"], font=F_BADGE) + 10), y + 24, c["stat"])
    ty = y + 84
    d.text((x + 6, ty), f"{c['n']}  {c['tag']} — {c['banner']}", font=F_TAG, fill=RED)
    ty += 13
    for ln in wrap(d, c["head"], F_H, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=F_H, fill=INK)
        ty += 18
    for ln in wrap(d, c["body"], F_B, w - 12)[:3]:
        d.text((x + 6, ty), ln, font=F_B, fill=DIM)
        ty += 14

def small_card(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=CREAM)
    d.rectangle([x + 1, y + 1, x + w - 1, y + 15], fill=c["col"])
    d.text((x + 6, y + 3), f"{c['n']}  {c['tag']}", font=F_TAG, fill=(255, 255, 255))
    d.text((x + w - 6 - d.textlength(c["st"], font=F_TAG), y + 3), c["st"], font=F_TAG, fill=(255, 255, 255))
    pic(d, c["kind"], x + 1, y + 16, w - 2, 50)
    badge(d, x + w - 8 - (d.textlength(c["stat"], font=F_BADGE) + 10), y + 50, c["stat"])
    ty = y + 70
    for ln in wrap(d, c["head"], F_HS, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=F_HS, fill=INK)
        ty += 15
    for ln in wrap(d, c["body"], F_BS, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=F_BS, fill=DIM)
        ty += 12

def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=(200, 225, 240), outline=INK)
    sx, sy = mw / 300, mh / 150
    def X(px):
        return mx + px * sx
    def Y(py):
        return my + py * sy
    # Rough continents as polygons, in map-local coordinates.
    na = [(18, 22), (52, 14), (88, 20), (96, 38), (78, 52), (60, 44), (44, 58), (30, 66), (16, 44)]
    sa = [(52, 78), (76, 74), (92, 92), (82, 122), (64, 128), (50, 104)]
    eu = [(128, 26), (158, 16), (180, 24), (172, 44), (146, 50), (128, 40)]
    af = [(132, 56), (162, 52), (182, 66), (176, 96), (158, 118), (140, 96), (128, 76)]
    asia = [(184, 20), (230, 12), (268, 22), (276, 48), (252, 62), (220, 58), (196, 66), (182, 44)]
    au = [(236, 108), (268, 104), (282, 118), (262, 132), (238, 126)]
    for poly in (na, sa, eu, af, asia, au):
        d.polygon([(X(px), Y(py)) for px, py in poly], fill=(230, 215, 160), outline=(180, 160, 110))
    d.text((X(8), Y(4)), "PACIFIC", font=F_SB, fill=(60, 90, 140))
    d.text((X(118), Y(132)), "ATLANTIC", font=F_SB, fill=(60, 90, 140))
    pins = [(140, 34), (196, 52), (170, 60), (66, 88), (40, 30), (248, 30), (148, 44), (90, 46), (76, 96), (206, 78), (252, 44), (96, 108), (252, 116)]
    for i, (px, py) in enumerate(pins):
        d.ellipse([X(px) - 6, Y(py) - 6, X(px) + 6, Y(py) + 6], fill=RED, outline=(255, 255, 255))
        d.text((X(px) - 3, Y(py) - 5), str(i + 1), font=F_SB, fill=(255, 255, 255))

def build():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    d.text((16, 10), "THE WORLD IN ONE DAY", font=F_SB, fill=RED)
    right = "43 STORIES  •  6 REGIONS  •  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((PAGE - 16 - d.textlength(right, font=F_SB), 10), right, font=F_SB, fill=INK)
    d.line([(16, 30), (PAGE - 16, 30)], fill=INK, width=2)
    centred(d, 36, "Saturday 21 November 2026", F_TITLE)
    centred(d, 104, "COP31 runs into overtime  •  Riyadh downs three missiles  •  Kyiv hit again", F_SUB)
    d.line([(16, 128), (PAGE - 16, 128)], fill=INK, width=1)
    stats = [("13", "days COP31 has run in Antalya, still with no deal"),
             ("3", "ballistic missiles shot down over Riyadh before dawn"),
             ("42", "hurt in Kryvyi Rih, a boy and a medic killed"),
             ("6.7", "magnitude of the earthquake in Junin, central Peru"),
             ("146", "people safe after a jet's engine-fire alert"),
             ("136", "runs by KL Rahul that put India in charge")]
    x = 16
    col_w = (PAGE - 32) / 6
    for val, lab in stats:
        d.text((x + 4, 134), val, font=F_BIG, fill=RED)
        ty = 164
        for ln in wrap(d, lab, F_BIGS, col_w - 10)[:3]:
            d.text((x + 4, ty), ln, font=F_BIGS, fill=INK)
            ty += 11
        x += col_w
        if x < PAGE - 16:
            d.line([(x, 136), (x, 196)], fill=RED, width=1)
    parts = [("Europe 12", 12, (20, 60, 140)), ("Asia 10", 10, RED), ("Middle East 6", 6, (140, 110, 20)),
             ("Africa 4", 4, (30, 120, 60)), ("Americas 8", 8, (110, 50, 140)), ("Other 3", 3, TEAL)]
    x = 16
    for name, count, col in parts:
        seg = (PAGE - 32) * count / 43
        d.rectangle([x, 200, x + seg, 218], fill=col)
        d.text((x + 4, 203), name, font=F_SB, fill=(255, 255, 255))
        x += seg
    hw = (PAGE - 32 - 16) / 3
    for i, c in enumerate(HEROES):
        hero_card(d, 16 + i * (hw + 8), 226, hw, 186, c)
    sw = (PAGE - 32 - 32) / 5
    y = 420
    for r in range(2):
        for i in range(5):
            small_card(d, 16 + i * (sw + 8), y, sw, 138, SMALLS[r * 5 + i])
        y += 146
    y = 708
    d.text((16, y), "WHERE IT HAPPENED", font=F_SB, fill=RED)
    d.text((296, y), "ALSO ON SATURDAY 21 NOVEMBER 2026  —  30 MORE STORIES  •  43 IN ALL", font=F_SB, fill=RED)
    draw_map(d, 16, y + 18, 270, 135)
    d.text((16, y + 172), "Red numbers mark stories 1-13.", font=F_S, fill=(80, 80, 80))
    for i, s in enumerate(MORE):
        col = i // 15
        row = i % 15
        d.text((296 + col * 360, y + 18 + row * 11), s, font=F_LIST, fill=INK)
    by = 892
    d.rectangle([16, by, PAGE - 16, by + 76], outline=RED, width=2)
    d.text((24, by + 6), "DATE CHECK  ✓", font=F_SB, fill=RED)
    note = ("Every story here happened, or was first reported, on Saturday 21 November 2026. LEFT OUT — other days' news: "
            "Russian missiles land in Poland (Fri 20 Nov) • Kyiv bridges hit (Fri 20 Nov) • UK–EU deal (Fri 20 Nov) • "
            "ICJ Myanmar genocide ruling (Thu 19 Nov) • Cyclone Akvan's landfall (Fri 20 Nov) • Anthropic debut, shares jump 17% (Thu 19 Nov).")
    ty = by + 22
    for ln in wrap(d, note, F_BS, PAGE - 48):
        d.text((24, ty), ln, font=F_BS, fill=INK)
        ty += 13
    d.text((16, 978), "Every story here happened, or was first reported, on Saturday 21 November 2026. Officials' counts and claims are attributed.",
           font=F_S, fill=(80, 80, 80))
    d.text((16, 996), "Sources: Reuters, AP, AFP, BBC, Al Jazeera, USGS, ESA, CoinGecko, Kyiv Post  •  Pictures and map: original, drawn in code  •  21 November 2026",
           font=F_S, fill=(80, 80, 80))
    img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
    print("saved entry.png", img.size)

if __name__ == "__main__":
    build()
