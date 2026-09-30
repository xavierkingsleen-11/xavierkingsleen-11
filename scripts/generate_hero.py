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

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "hero-hacker.gif")

TARGET_W, TARGET_H = 900, 460
BG = (4, 9, 7)

random.seed(7)


def add_grid_texture(canvas, opacity=16):
    """Faint cyber-grid lines across the FULL canvas, so the padding around
    the photo is never flat/dead black - it reads as intentional background
    art, not empty space, no matter what color the surrounding page is."""
    w, h = canvas.size
    grid = Image.new("L", (w, h), 0)
    gdraw = ImageDraw.Draw(grid)
    step = 34
    for x in range(0, w, step):
        gdraw.line([(x, 0), (x, h)], fill=opacity)
    for y in range(0, h, step):
        gdraw.line([(0, y), (w, y)], fill=opacity)
    green_layer = Image.new("RGB", (w, h), (20, 60, 40))
    return Image.composite(green_layer, canvas, grid)


def prep_base(src_path):
    # Start from a full dark textured canvas (this is the "seam" the photo
    # will melt into - self-contained, not dependent on the page's own bg).
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), BG)
    canvas = add_grid_texture(canvas)

    im = Image.open(src_path).convert("RGB")
    # Photo occupies a smaller inner region, not the full bleed - this is
    # what leaves room for a wide, gradual fade on every side.
    photo_w, photo_h = int(TARGET_W * 0.62), int(TARGET_H * 0.86)
    im = ImageOps.fit(im, (photo_w, photo_h), Image.LANCZOS)

    # Darken hard + push toward cyan/green (SOC grading)
    im = ImageEnhance.Brightness(im).enhance(0.45)
    im = ImageEnhance.Contrast(im).enhance(1.2)
    r, g, b = im.split()
    r = r.point(lambda v: int(v * 0.5))
    g = g.point(lambda v: min(255, int(v * 1.05)))
    b = b.point(lambda v: min(255, int(v * 1.1)))
    im = Image.merge("RGB", (r, g, b))

    # Paste the graded photo onto its own transparent-mask layer sized to
    # the full canvas, offset slightly left (matches the approved concept).
    offset_x = int(TARGET_W * 0.03)
    offset_y = (TARGET_H - photo_h) // 2
    photo_layer = Image.new("RGB", (TARGET_W, TARGET_H), BG)
    photo_layer.paste(im, (offset_x, offset_y))

    # Strong radial vignette: only the centre ~35% of the photo stays at
    # full strength, everything past that melts toward the grid canvas.
    vignette = Image.new("L", (TARGET_W, TARGET_H), 0)
    vdraw = ImageDraw.Draw(vignette)
    cx, cy = offset_x + photo_w // 2, offset_y + photo_h // 2
    max_r = int(max(photo_w, photo_h) * 0.72)
    for radius in range(max_r, 0, -2):
        frac = radius / max_r
        alpha = int(255 * max(0, 1 - frac ** 1.3))
        vdraw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=alpha)
    vignette = vignette.filter(ImageFilter.GaussianBlur(65))

    # Rectangular feather over the photo's own bounds: guarantees the photo's
    # four edges reach 0% opacity, so no straight photo boundary can show.
    feather = Image.new("L", (TARGET_W, TARGET_H), 0)
    ImageDraw.Draw(feather).rectangle(
        [offset_x + 95, offset_y + 70, offset_x + photo_w - 95, offset_y + photo_h - 70],
        fill=255,
    )
    feather = feather.filter(ImageFilter.GaussianBlur(48))
    vignette = ImageChops.multiply(vignette, feather)

    blended = Image.composite(photo_layer, canvas, vignette)

    # Hard directional fades at the literal canvas edges too, so top/bottom/
    # left/right borders are always pure background - never a straight photo
    # edge, even where the vignette ellipse doesn't fully reach.
    edge_fade = Image.new("L", (TARGET_W, TARGET_H), 255)
    edraw = ImageDraw.Draw(edge_fade)
    fade_px = 130
    for i in range(fade_px):
        a = int(255 * (i / fade_px) ** 1.4)
        edraw.line([(i, 0), (i, TARGET_H)], fill=a)
        edraw.line([(TARGET_W - 1 - i, 0), (TARGET_W - 1 - i, TARGET_H)], fill=a)
        edraw.line([(0, i), (TARGET_W, i)], fill=a)
        edraw.line([(0, TARGET_H - 1 - i), (TARGET_W, TARGET_H - 1 - i)], fill=a)
    edge_fade = edge_fade.filter(ImageFilter.GaussianBlur(30))
    blended = Image.composite(blended, canvas, edge_fade)

    # Scanlines across the whole canvas (unifies photo + background texture)
    scan = Image.new("L", (TARGET_W, TARGET_H), 0)
    sdraw = ImageDraw.Draw(scan)
    for y in range(0, TARGET_H, 3):
        sdraw.line([(0, y), (TARGET_W, y)], fill=35)
    dark_overlay = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
    blended = Image.composite(dark_overlay, blended, scan)

    # Faint always-on digital noise ties photo grain to background grain
    noise = Image.effect_noise((TARGET_W, TARGET_H), 20).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    blended = Image.blend(blended, noise_rgb, 0.035)

    # Digital particles: sparse cyan/green motes drifting around the figure
    pd = ImageDraw.Draw(blended)
    rnd = random.Random(21)
    cx0 = offset_x + photo_w // 2
    for _ in range(190):
        x = int(rnd.gauss(cx0, photo_w * 0.42))
        y = int(rnd.gauss(TARGET_H * 0.5, TARGET_H * 0.30))
        if 0 <= x < TARGET_W and 0 <= y < TARGET_H:
            a = rnd.choice([0.25, 0.4, 0.6, 0.9])
            base = (93, 243, 255) if rnd.random() < 0.55 else (57, 255, 143)
            col = tuple(int(BG[c] + (base[c] - BG[c]) * a) for c in range(3))
            r = rnd.choice([0, 0, 1, 1, 2])
            pd.rectangle([x, y, x + r, y + r], fill=col)

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
    # Convert with Floyd-Steinberg dithering so the wide fade gradients don't
    # band under the GIF format's 256-colour palette limit.
    pal_frames = [
        f.convert("P", palette=Image.ADAPTIVE, colors=256, dither=Image.FLOYDSTEINBERG)
        for f in frames
    ]
    pal_frames[0].save(
        OUT_PATH,
        save_all=True,
        append_images=pal_frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )
    print(f"Wrote {OUT_PATH} ({len(frames)} frames, ~{sum(durations)/1000:.1f}s cycle)")


if __name__ == "__main__":
    main()
