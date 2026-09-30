#!/usr/bin/env python3
"""
Generates assets/threat-map.gif - the "GLOBAL THREAT MONITORING" panel.

* Land shape: REAL Natural Earth 1:110m land outlines (public domain), see
  scripts/data/land_110m_simplified.py, drawn as a dotted world map
  (equirectangular projection, cropped to -58..84 deg latitude).
* Animation (raster GIF, not SVG): scan sweep that lights up the dots it
  passes, blinking monitoring nodes, pulsing rings, subtle connection arcs
  with travelling packets, and a highlighted "home" node (Tamil Nadu).

VISUAL SIMULATION ONLY - node positions are major-city coordinates, the
arcs are decorative.  Nothing here is real threat intelligence.

Edit MONITORING_NODES / HOME_NODE below to move or add nodes.
"""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
from land_110m_simplified import LAND  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "threat-map.gif")

W, H = 1000, 400
SS = 2                       # supersampling factor for smooth dots/lines
LON_MIN, LON_MAX = -180.0, 180.0
LAT_MIN, LAT_MAX = -58.0, 84.0
DOT_STEP = 7                 # px between map dots (in final resolution)
N_FRAMES = 30
FRAME_MS = 100

BG = (5, 11, 8)
DOT_BASE = (24, 84, 52)
GREEN = (57, 255, 143)
CYAN = (93, 243, 255)

# (name, lat, lon)  - major cities used purely as monitoring-node positions
HOME_NODE = ("Tamil Nadu", 11.1, 78.7)
MONITORING_NODES = [
    ("San Francisco", 37.8, -122.4),
    ("New York", 40.7, -74.0),
    ("Sao Paulo", -23.5, -46.6),
    ("London", 51.5, -0.1),
    ("Frankfurt", 50.1, 8.7),
    ("Johannesburg", -26.2, 28.0),
    ("Dubai", 25.2, 55.3),
    ("Singapore", 1.35, 103.8),
    ("Tokyo", 35.7, 139.7),
    ("Sydney", -33.9, 151.2),
]


def project(lat, lon, scale=1):
    x = (lon - LON_MIN) / (LON_MAX - LON_MIN) * W * scale
    y = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H * scale
    return x, y


def land_mask():
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    for ring in LAND:
        pts = [project(lat, lon) for lon, lat in ring]
        d.polygon(pts, fill=255)
    return m


def land_dots(mask):
    dots = []
    for y in range(DOT_STEP // 2, H, DOT_STEP):
        off = (DOT_STEP // 2) if (y // DOT_STEP) % 2 else 0   # staggered grid
        for x in range(off + DOT_STEP // 2, W, DOT_STEP):
            if mask.getpixel((x, y)) > 127:
                dots.append((x, y))
    return dots


def arc_point(p0, p1, t, lift=0.22):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - abs(x1 - x0) * lift
    x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t ** 2 * x1
    y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t ** 2 * y1
    return x, y


def mix(c0, c1, a):
    a = max(0.0, min(1.0, a))
    return tuple(int(c0[i] + (c1[i] - c0[i]) * a) for i in range(3))


def render_frame(dots, k):
    ph = k / N_FRAMES
    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)

    sweep_x = ph * (W + 160) - 80           # scan line position (px)
    r_dot = 1.5 * SS

    # dotted land, brightened by the scan sweep
    for (x, y) in dots:
        dist = abs(x - sweep_x)
        boost = max(0.0, 1 - dist / 70.0)
        col = mix(DOT_BASE, CYAN, boost * 0.95)
        rr = r_dot * (1 + 0.5 * boost)
        d.ellipse([x * SS - rr, y * SS - rr, x * SS + rr, y * SS + rr], fill=col)

    # scan line (soft)
    for i, a in enumerate((0.10, 0.22, 0.10)):
        xx = (sweep_x + (i - 1) * 2) * SS
        d.line([(xx, 0), (xx, H * SS)], fill=mix(BG, CYAN, a), width=SS)

    home = project(HOME_NODE[1], HOME_NODE[2])
    pts = [project(lat, lon) for _, lat, lon in MONITORING_NODES]

    # restrained connection arcs to the home node + travelling packets
    for i, p in enumerate(pts):
        steps = 40
        prev = None
        for s in range(steps + 1):
            q = arc_point(p, home, s / steps)
            if prev is not None and s % 2 == 0:
                d.line([(prev[0] * SS, prev[1] * SS), (q[0] * SS, q[1] * SS)],
                       fill=mix(BG, GREEN, 0.32), width=SS)
            prev = q
        t = (ph * 1.0 + i * 0.137) % 1.0
        if i % 2 == 0:                              # only some arcs carry a packet
            qx, qy = arc_point(p, home, t)
            rr = 2.6 * SS
            d.ellipse([qx * SS - rr, qy * SS - rr, qx * SS + rr, qy * SS + rr],
                      fill=mix(BG, CYAN, 0.9))

    # monitoring nodes: blink + pulse ring
    for i, (x, y) in enumerate(pts):
        lp = (ph * 2 + i * 0.173) % 1.0
        blink = 0.55 + 0.45 * math.sin(2 * math.pi * (ph * 2 + i * 0.29))
        col = mix(BG, GREEN, 0.35 + 0.65 * blink)
        r = 3.2 * SS
        d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=col)
        pr = (4 + lp * 15) * SS
        d.ellipse([x * SS - pr, y * SS - pr, x * SS + pr, y * SS + pr],
                  outline=mix(BG, GREEN, (1 - lp) * 0.8), width=SS)

    # home node: selected / highlighted with concentric circles
    hx, hy = home
    lp = (ph * 2) % 1.0
    for rad, a in ((13, 0.9), (20, 0.5)):
        rr = rad * SS
        d.ellipse([hx * SS - rr, hy * SS - rr, hx * SS + rr, hy * SS + rr],
                  outline=mix(BG, CYAN, a), width=SS)
    pr = (8 + lp * 26) * SS
    d.ellipse([hx * SS - pr, hy * SS - pr, hx * SS + pr, hy * SS + pr],
              outline=mix(BG, CYAN, (1 - lp) * 0.9), width=SS)
    r = 4.2 * SS
    d.ellipse([hx * SS - r, hy * SS - r, hx * SS + r, hy * SS + r], fill=CYAN)

    return img.resize((W, H), Image.LANCZOS)


def main():
    dots = land_dots(land_mask())
    frames = [render_frame(dots, k) for k in range(N_FRAMES)]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=64, dither=Image.NONE) for f in frames]
    pal[0].save(OUT_PATH, save_all=True, append_images=pal[1:],
                duration=FRAME_MS, loop=0, optimize=False)
    print(f"Wrote {OUT_PATH}: {len(dots)} land dots, {N_FRAMES} frames, "
          f"{os.path.getsize(OUT_PATH)/1024:.0f} KB")


if __name__ == "__main__":
    main()
