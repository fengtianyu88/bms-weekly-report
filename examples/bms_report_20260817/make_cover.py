# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = r"c:\Users\tiany\Documents\Trae solo my data\bms-weekly-20260817"
W, H = 1800, 766
FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"
CJK_SIZE = 160
DATE_SIZE = 111
LINE_GAP = 46
BLOCK_CENTER = 0.49
TOP = (8, 20, 46)
BOT = (22, 66, 150)

bg = Image.new("RGB", (W, H))
px = bg.load()
for y in range(H):
    t = y / (H - 1)
    t = t * t
    r = int(TOP[0] + (BOT[0] - TOP[0]) * t)
    g = int(TOP[1] + (BOT[1] - TOP[1]) * t)
    b = int(TOP[2] + (BOT[2] - TOP[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)

glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([W // 2 - 900, H // 2 - 500, W // 2 + 900, H // 2 + 500], fill=60)
glow = glow.filter(ImageFilter.GaussianBlur(200))
accent = Image.new("RGB", (W, H), (40, 110, 220))
bg = Image.composite(accent, bg, glow)

draw = ImageDraw.Draw(bg)
for i in range(6):
    y0 = H - 150 + i * 22
    draw.line([(0, y0), (W, y0)], fill=(60, 130, 220, 90), width=2)
for x0, y0, x1 in ((180, H - 60, 560), (720, H - 38, 1080), (1240, H - 82, 1620)):
    draw.line([(x0, y0), (x1, y0)], fill=(70, 140, 230), width=3)
    draw.ellipse([x1 + 6, y0 - 5, x1 + 16, y0 + 5], fill=(90, 160, 240))
    draw.ellipse([x0 - 10, y0 - 10, x0 + 10, y0 + 10], outline=(70, 140, 230), width=2)

font_cjk = ImageFont.truetype(FONT_PATH, CJK_SIZE)
box1 = draw.textbbox((0, 0), "BMS 算法追踪", font=font_cjk)
h1 = box1[3] - box1[1]

font_date = ImageFont.truetype(FONT_PATH, DATE_SIZE)
box2 = draw.textbbox((0, 0), "2026-08-17", font=font_date)
h2 = box2[3] - box2[1]

total = h1 + LINE_GAP + h2
y = int(H * BLOCK_CENTER) - total // 2
for t, f, b in (("BMS 算法追踪", font_cjk, box1), ("2026-08-17", font_date, box2)):
    h = b[3] - b[1]
    w = b[2] - b[0]
    draw.text(((W - w) // 2 - b[0], y - b[1]), t, font=f, fill=(255, 255, 255))
    y += h + LINE_GAP

bg.save(BASE + r"\cover_final.jpg", quality=92)
print(f"cjk h={h1}px ({CJK_SIZE}pt) / date h={h2}px ({DATE_SIZE}pt)")
print(f"widths: {(box1[2]-box1[0])/W:.0%} / {(box2[2]-box2[0])/W:.0%}")
