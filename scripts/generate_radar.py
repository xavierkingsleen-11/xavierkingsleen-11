#!/usr/bin/env python3
"""
Generates assets/skills-radar.png from config/skills.json.

PNG, not SVG - the profile intentionally avoids SVG as a generated visual
asset. Edit skill values in config/skills.json, re-run this script (or let
update-assets.yml run it), and the radar image updates. Never hand-edit
assets/skills-radar.png; it is a build output.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config", "skills.json")
OUT_PATH = os.path.join(ROOT, "assets", "skills-radar.png")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

SCALE = 3  # supersample then downscale for clean anti-aliased lines/text
BG = (5, 11, 8)
GRID = (18, 51, 33)
NEON_GREEN = (57, 255, 143)
CYAN = (93, 243, 255)
DIM_TEXT = (127, 219, 163)

W, H = 700, 480
CX, CY = W // 2, H // 2 + 6
R = 140


def point(cx, cy, r, angle_deg):
    a = math.radians(angle_deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def main():
    with open(CONFIG_PATH) as f:
        skills = json.load(f)
    axes = skills["radar"]["axes"]
    n = len(axes)
    step = 360 / n

    w, h = W * SCALE, H * SCALE
    cx, cy, r = CX * SCALE, CY * SCALE, R * SCALE

    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 13 * SCALE)

    # Grid rings
    for frac in (0.25, 0.5, 0.75, 1.0):
        pts = [point(cx, cy, r * frac, i * step) for i in range(n)]
        draw.polygon(pts, outline=GRID, width=max(1, SCALE // 2))

    # Spokes
    for i in range(n):
        x, y = point(cx, cy, r, i * step)
        draw.line([(cx, cy), (x, y)], fill=GRID, width=max(1, SCALE // 2))

    # Data polygon (soft glow via blurred duplicate underneath)
    data_pts = [point(cx, cy, r * (axes[i]["value"] / 100), i * step) for i in range(n)]

    glow_layer = Image.new("RGB", (w, h), BG)
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.polygon(data_pts, outline=NEON_GREEN, width=SCALE * 2)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8 * SCALE // 3))
    img = Image.blend(img, glow_layer, 0.5)
    draw = ImageDraw.Draw(img)

    # Filled polygon (semi-transparent look via blend onto bg)
    fill_layer = Image.new("RGB", (w, h), BG)
    fill_draw = ImageDraw.Draw(fill_layer)
    fill_draw.polygon(data_pts, fill=NEON_GREEN)
    img = Image.blend(img, fill_layer, 0.16)
    draw = ImageDraw.Draw(img)

    draw.polygon(data_pts, outline=NEON_GREEN, width=SCALE)
    for x, y in data_pts:
        rad = 4 * SCALE
        draw.ellipse([x - rad, y - rad, x + rad, y + rad], fill=CYAN)

    # Labels
    for i, axis in enumerate(axes):
        x, y = point(cx, cy, r + 40 * SCALE, i * step)
        text = axis["label"]
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if x < cx - 15 * SCALE:
            x -= tw
        elif abs(x - cx) <= 15 * SCALE:
            x -= tw / 2
        y -= th / 2
        draw.text((x, y), text, fill=DIM_TEXT, font=font)

    if not skills["radar"].get("confirmed", False):
        stamp_font = ImageFont.truetype(FONT_PATH, 12 * SCALE)
        msg = "PLACEHOLDER VALUES - set real values in config/skills.json"
        bb = draw.textbbox((0, 0), msg, font=stamp_font)
        draw.text(((w - (bb[2] - bb[0])) / 2, h - 26 * SCALE), msg,
                  fill=(255, 190, 90), font=stamp_font)

    img = img.resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
