#!/usr/bin/env python3
"""
Builds assets/hero-hacker.gif from a supplied source photo: dark-edge
blending into the SOC-black background, cyan/green grading, scanlines, and a
short (~0.3-0.6s) CCTV-style glitch interruption roughly every ~9 seconds.

Usage:
    python3 scripts/generate_hero.py /path/to/source-photo.jpg

Re-run this any time you want to swap the hero photo; nothing else in the
README needs to change (it just references assets/hero-hacker.gif).
"""
import os
import random
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "hero-hacker.gif")

TARGET_W, TARGET_H = 620, 420
BG = (4, 9, 7)

random.seed(7)


def prep_base(src_path):
    im = Image.open(src_path).convert("RGB")
    im = ImageOps.fit(im, (TARGET_W, TARGET_H), Image.LANCZOS)

    # Darken + push toward cyan/green (SOC grading)
    im = ImageEnhance.Brightness(im).enhance(0.62)
    im = ImageEnhance.Contrast(im).enhance(1.15)
    r, g, b = im.split()
    r = r.point(lambda v: int(v * 0.55))
    g = g.point(lambda v: min(255, int(v * 1.08)))
    b = b.point(lambda v: min(255, int(v * 1.12)))
    im = Image.merge("RGB", (r, g, b))

    # Vignette: fade edges to the page background so the rectangle disappears
    vignette = Image.new("L", (TARGET_W, TARGET_H), 0)
    vdraw = ImageDraw.Draw(vignette)
    max_r = int((TARGET_W ** 2 + TARGET_H ** 2) ** 0.5 / 2)
    cx, cy = TARGET_W // 2, TARGET_H // 2 + 20
    for radius in range(max_r, 0, -2):
        # opacity of the ORIGINAL image at this radius (255 = fully visible)
        frac = radius / max_r
        alpha = int(255 * max(0, 1 - frac ** 1.6))
        vdraw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius], fill=alpha
        )
    vignette = vignette.filter(ImageFilter.GaussianBlur(40))

    bg_layer = Image.new("RGB", (TARGET_W, TARGET_H), BG)
    blended = Image.composite(im, bg_layer, vignette)

    # Hard fade strips at the literal edges so no rectangle boundary reads
    edge_fade = Image.new("L", (TARGET_W, TARGET_H), 255)
    edraw = ImageDraw.Draw(edge_fade)
    fade_px = 70
    for i in range(fade_px):
        a = int(255 * (i / fade_px))
        edraw.line([(i, 0), (i, TARGET_H)], fill=a)
        edraw.line([(TARGET_W - 1 - i, 0), (TARGET_W - 1 - i, TARGET_H)], fill=a)
        edraw.line([(0, i), (TARGET_W, i)], fill=a)
        edraw.line([(0, TARGET_H - 1 - i), (TARGET_W, TARGET_H - 1 - i)], fill=a)
    edge_fade = edge_fade.filter(ImageFilter.GaussianBlur(20))
    blended = Image.composite(blended, bg_layer, edge_fade)

    # Subtle scanlines
    scan = Image.new("L", (TARGET_W, TARGET_H), 0)
    sdraw = ImageDraw.Draw(scan)
    for y in range(0, TARGET_H, 3):
        sdraw.line([(0, y), (TARGET_W, y)], fill=40)
    dark_overlay = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
    blended = Image.composite(dark_overlay, blended, scan)

    # Faint digital noise, always-on but restrained
    noise = Image.effect_noise((TARGET_W, TARGET_H), 22).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    blended = Image.blend(blended, noise_rgb, 0.03)

    return blended


def make_glitch_frame(base, intensity=1.0):
    frame = base.copy()
    w, h = frame.size

    # Horizontal displacement bands
    band_count = random.randint(4, 7)
    for _ in range(band_count):
        band_h = random.randint(6, 24)
        y = random.randint(0, h - band_h)
        shift = random.randint(-30, 30)
        box = (0, y, w, y + band_h)
        strip = frame.crop(box)
        shifted = Image.new("RGB", strip.size, BG)
        shifted.paste(strip, (shift, 0))
        frame.paste(shifted, box)

    # RGB channel split
    r, g, b = frame.split()
    off = int(6 * intensity)
    r = Image.new("L", r.size, 0)
    r.paste(frame.split()[0], (off, 0))
    b = Image.new("L", b.size, 0)
    b.paste(frame.split()[2], (-off, 0))
    frame = Image.merge("RGB", (r, g, b))

    # Bright flash scanline interruption + extra noise
    noise = Image.effect_noise((w, h), 55).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    frame = Image.blend(frame, noise_rgb, 0.18 * intensity)

    overlay = ImageDraw.Draw(frame)
    for _ in range(random.randint(2, 4)):
        y = random.randint(0, h - 1)
        overlay.line([(0, y), (w, y)], fill=(150, 255, 210), width=1)

    return frame


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src or not os.path.exists(src):
        print("Usage: generate_hero.py /path/to/source-photo.jpg", file=sys.stderr)
        sys.exit(1)

    base = prep_base(src)

    frames = [base]
    durations = [8500]  # ms: long clear hold (~8.5s) before the glitch

    for intensity in (0.6, 1.0, 0.7):
        frames.append(make_glitch_frame(base, intensity))
        durations.append(120)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    frames[0].save(
        OUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )
    print(f"Wrote {OUT_PATH} ({len(frames)} frames, ~{sum(durations)/1000:.1f}s cycle)")


if __name__ == "__main__":
    main()
