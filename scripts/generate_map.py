#!/usr/bin/env python3
"""
Generates assets/threat-map.svg: a dotted world-map silhouette with pulsing
monitoring nodes. Uses native SVG <animate>/<animateTransform> (SMIL) so the
pulse still plays on GitHub when the file is embedded via <img src=...svg>.

Node locations are illustrative "monitoring points", not real telemetry
(GitHub README cannot run arbitrary JS, so this stays a themed visual, not a
live feed). Edit NODES below to move them.
"""
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "threat-map.svg")

W, H = 640, 280
BG = "#050b08"
DOT = "#123321"
NEON_GREEN = "#39ff8f"
CYAN = "#5df3ff"

# Extremely simplified world "dot cloud" (illustrative, not geographically precise)
# Each entry: (x_fraction, y_fraction) landmass blobs, rendered as scattered dots.
LANDMASS_SEEDS = [
    (0.08, 0.30, 0.10, 0.16),  # N. America
    (0.16, 0.55, 0.06, 0.18),  # S. America
    (0.30, 0.85, 0.05, 0.06),  # small
    (0.44, 0.28, 0.09, 0.14),  # Europe
    (0.47, 0.45, 0.10, 0.22),  # Africa
    (0.58, 0.28, 0.16, 0.20),  # Asia
    (0.62, 0.50, 0.10, 0.10),  # S Asia
    (0.82, 0.62, 0.08, 0.10),  # Australia
]

NODES = [
    {"x": 0.62, "y": 0.34, "label": "monitoring"},   # South/East Asia region
    {"x": 0.47, "y": 0.30, "label": "monitoring"},   # Europe
    {"x": 0.14, "y": 0.32, "label": "monitoring"},   # N. America
    {"x": 0.84, "y": 0.66, "label": "monitoring"},   # Australia
    {"x": 0.50, "y": 0.50, "label": "alert", "color": "alert"},
]

random.seed(11)


def dots_for_seed(cx, cy, rw, rh, n):
    pts = []
    for _ in range(n):
        x = cx + random.uniform(-rw, rw)
        y = cy + random.uniform(-rh, rh)
        if random.random() < 0.65:
            pts.append((x * W, y * H))
    return pts


def main():
    dot_elems = []
    for (cx, cy, rw, rh) in LANDMASS_SEEDS:
        for x, y in dots_for_seed(cx, cy, rw, rh, 90):
            dot_elems.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.1" fill="{DOT}"/>')

    node_elems = []
    for i, n in enumerate(NODES):
        x, y = n["x"] * W, n["y"] * H
        color = CYAN if n.get("color") == "alert" else NEON_GREEN
        dur = 2.2 + (i % 3) * 0.4
        node_elems.append(f"""
  <circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{color}"/>
  <circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="none" stroke="{color}" stroke-width="1.4">
    <animate attributeName="r" values="3;16;3" dur="{dur}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.8;0;0.8" dur="{dur}s" repeatCount="indefinite"/>
  </circle>""")

    # A few restrained connection lines between nodes
    lines = []
    for i in range(len(NODES) - 1):
        a, b = NODES[i], NODES[i + 1]
        x1, y1 = a["x"] * W, a["y"] * H
        x2, y2 = b["x"] * W, b["y"] * H
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{NEON_GREEN}" stroke-width="0.6" stroke-dasharray="2 4" opacity="0.35"/>'
        )

    svg = f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {''.join(dot_elems)}
  {''.join(lines)}
  {''.join(node_elems)}
</svg>
"""
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
