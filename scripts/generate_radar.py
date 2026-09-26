#!/usr/bin/env python3
"""
Generates assets/skills-radar.svg from config/skills.json.

Edit skill values in config/skills.json -> re-run this script (or let the
'update-assets' GitHub Action run it) -> the radar image updates.
Never hand-edit assets/skills-radar.svg directly; it is a build output.
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config", "skills.json")
OUT_PATH = os.path.join(ROOT, "assets", "skills-radar.svg")

BG = "#050b08"
GRID = "#123321"
NEON_GREEN = "#39ff8f"
CYAN = "#5df3ff"
DIM_TEXT = "#7fdba3"

W, H = 460, 420
CX, CY = W // 2, H // 2 + 10
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

    rings = []
    for frac in (0.25, 0.5, 0.75, 1.0):
        pts = [point(CX, CY, R * frac, i * step) for i in range(n)]
        pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        rings.append(
            f'<polygon points="{pts_str}" fill="none" stroke="{GRID}" stroke-width="1" />'
        )

    spokes = []
    labels = []
    for i, axis in enumerate(axes):
        x, y = point(CX, CY, R, i * step)
        spokes.append(
            f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1" />'
        )
        lx, ly = point(CX, CY, R + 34, i * step)
        anchor = "middle"
        if lx < CX - 15:
            anchor = "end"
        elif lx > CX + 15:
            anchor = "start"
        labels.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{DIM_TEXT}" font-family="Consolas, monospace" '
            f'font-size="12" text-anchor="{anchor}" dominant-baseline="middle">{axis["label"]}</text>'
        )

    data_pts = [
        point(CX, CY, R * (axis["value"] / 100), i * step) for i, axis in enumerate(axes)
    ]
    data_pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in data_pts)

    vertex_dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{CYAN}"/>' for x, y in data_pts
    )

    svg = f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}" rx="10"/>
  {''.join(rings)}
  {''.join(spokes)}
  <polygon points="{data_pts_str}" fill="{NEON_GREEN}" fill-opacity="0.18" stroke="{NEON_GREEN}"
           stroke-width="2" filter="url(#glow)">
    <animate attributeName="fill-opacity" values="0.12;0.24;0.12" dur="4s" repeatCount="indefinite"/>
  </polygon>
  {vertex_dots}
  {''.join(labels)}
</svg>
"""
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
