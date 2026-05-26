# -*- coding: utf-8 -*-
"""브랜드 자산 생성 — 파비콘·PWA 아이콘·OG 커버 (로즈골드)."""

import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

BG = (11, 11, 14)
G1 = (244, 210, 156)   # light gold
G2 = (233, 184, 167)   # rose
G3 = (154, 90, 60)     # deep copper

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def radial_disc(size, cx, cy, r):
    """로즈골드 라디얼 그라데이션 원 (specular + dark rim)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            if d <= r:
                t = d / r
                if t < 0.5: col = lerp(G1, G2, t / 0.5)
                else: col = lerp(G2, G3, (t - 0.5) / 0.5)
                # specular 하이라이트 (상단-좌측)
                sx, sy = cx - r * 0.35, cy - r * 0.4
                sd = math.hypot(x - sx, y - sy)
                hi = max(0, 1 - sd / (r * 0.75))
                col = lerp(col, (255, 255, 255), hi * 0.45)
                # dark rim
                if t > 0.9: col = lerp(col, (40, 24, 14), (t - 0.9) / 0.1)
                px[x, y] = col + (255,)
    return img

def _font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def _kfont(size, bold=True):
    p = ("/usr/share/fonts/truetype/nanum/NanumSquareB.ttf" if bold
         else "/usr/share/fonts/truetype/nanum/NanumSquareR.ttf")
    if os.path.exists(p):
        try: return ImageFont.truetype(p, size)
        except Exception: pass
    return _font(size)

def icon(size, maskable=False, mono="M"):
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    rad = int(size * 0.22)
    # rounded bg
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(bg).rounded_rectangle([0, 0, size - 1, size - 1], radius=rad, fill=BG + (255,))
    img = bg
    disc_r = int(size * (0.30 if maskable else 0.34))
    disc = radial_disc(size, size // 2, size // 2, disc_r)
    img.alpha_composite(disc)
    d = ImageDraw.Draw(img)
    f = _font(int(disc_r * 1.1))
    tb = d.textbbox((0, 0), mono, font=f)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    d.text((size // 2 - tw // 2 - tb[0], size // 2 - th // 2 - tb[1]), mono,
           font=f, fill=(26, 18, 8, 255))
    return img

def save(img, name): img.save(os.path.join(ROOT, name)); print("wrote", name)

# PWA / touch icons
save(icon(512), "icon-512.png")
save(icon(192), "icon-192.png")
save(icon(512, maskable=True), "icon-maskable-512.png")
save(icon(180), "apple-touch-icon.png")

# favicon.ico (멀티사이즈)
fav = icon(64)
fav.save(os.path.join(ROOT, "favicon.ico"),
         sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("wrote favicon.ico")

# logo.png (헤더/OG용 원본)
logo = icon(400)
logo.save(os.path.join(ASSETS, "logo.png")); print("wrote assets/logo.png")
for s in (320, 160, 80):
    icon(s).save(os.path.join(ASSETS, f"logo-{s}.png")); print(f"wrote assets/logo-{s}.png")

# og-cover.jpg 1200x630
W, H = 1200, 630
og = Image.new("RGB", (W, H), BG)
# subtle radial glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gp = glow.load()
for y in range(0, H, 2):
    for x in range(0, W, 2):
        d = math.hypot(x - W * 0.78, y - H * 0.15) / (W * 0.6)
        a = max(0, 1 - d)
        c = lerp(G1, G3, min(1, d)) + (int(70 * a),)
        for dy in range(2):
            for dx in range(2):
                if x + dx < W and y + dy < H: gp[x + dx, y + dy] = c
og = Image.alpha_composite(og.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(og)
disc = radial_disc(220, 110, 110, 96)
og.paste(disc, (96, 70), disc)
d.text((96, 300), "마사지고", font=_kfont(96), fill=(243, 243, 245))
d.text((98, 416), "출장마사지 · 서울·경기·인천·부산 전 권역", font=_kfont(33, bold=False), fill=(154, 154, 163))
d.text((98, 478), "예약 0508-202-4719 · 연중무휴", font=_kfont(34), fill=(214, 178, 116))
og.save(os.path.join(ASSETS, "og-cover.jpg"), quality=86, optimize=True)
print("wrote assets/og-cover.jpg")
