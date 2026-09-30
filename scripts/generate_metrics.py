#!/usr/bin/env python3
"""
Generates assets/github-metrics.png with REAL data pulled from the GitHub
API: public repo count, total commits (via search API), stars received,
followers, following. No hardcoded/demo numbers are ever written here.
PNG, not SVG - the profile intentionally avoids SVG as a generated asset.

Run locally:
    GH_USERNAME=xavierkingsleen-11 GITHUB_TOKEN=<token or blank> python3 scripts/generate_metrics.py

In GitHub Actions, GITHUB_TOKEN is provided automatically by the runner
(secrets.GITHUB_TOKEN) - see .github/workflows/update-assets.yml. No extra
token setup is required; a token only helps if you want higher Search-API
rate limits for the commit count.
"""
import json
import os
import sys
import time

import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "github-metrics.png")
SOCIAL_PATH = os.path.join(ROOT, "config", "social.json")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

API = "https://api.github.com"

BG = (5, 11, 8)
BORDER = (28, 74, 46)
NEON = (57, 255, 143)
LABEL = (127, 219, 163)


def gh_get(url, token, params=None):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    return r.json(), r.headers


def fetch_stats(username, token):
    user, _ = gh_get(f"{API}/users/{username}", token)
    followers = user.get("followers", 0)
    following = user.get("following", 0)
    public_repos = user.get("public_repos", 0)

    stars = 0
    page = 1
    while True:
        repos, _ = gh_get(
            f"{API}/users/{username}/repos",
            token,
            params={"per_page": 100, "page": page, "type": "owner"},
        )
        if not repos:
            break
        stars += sum(r.get("stargazers_count", 0) for r in repos)
        if len(repos) < 100:
            break
        page += 1

    commits = None
    try:
        data, _ = gh_get(f"{API}/search/commits", token, params={"q": f"author:{username}"})
        commits = data.get("total_count")
    except Exception as e:
        print(f"warning: commit search failed ({e}); leaving commits blank", file=sys.stderr)

    return {
        "repositories": public_repos,
        "commits": commits,
        "stars": stars,
        "followers": followers,
        "following": following,
    }


def render_png(fields, pending_text=None):
    SCALE = 3
    w_each, h = 170, 100
    W = w_each * max(len(fields), 4) if pending_text else w_each * len(fields)
    img = Image.new("RGB", (W * SCALE, h * SCALE), BG)
    draw = ImageDraw.Draw(img)
    font_val = ImageFont.truetype(FONT_BOLD_PATH, 26 * SCALE)
    font_label = ImageFont.truetype(FONT_PATH, 12 * SCALE)

    if pending_text:
        font_msg = ImageFont.truetype(FONT_PATH, 14 * SCALE)
        draw.rectangle([6 * SCALE, 6 * SCALE, W * SCALE - 6 * SCALE, h * SCALE - 6 * SCALE],
                       outline=BORDER, width=SCALE)
        bbox = draw.textbbox((0, 0), pending_text, font=font_msg)
        tw = bbox[2] - bbox[0]
        draw.text(((W * SCALE - tw) / 2, (h * SCALE) / 2 - 8 * SCALE), pending_text,
                   fill=LABEL, font=font_msg)
    else:
        for i, (label, value) in enumerate(fields):
            x0 = i * w_each * SCALE
            draw.rounded_rectangle(
                [x0 + 6 * SCALE, 6 * SCALE, x0 + (w_each - 6) * SCALE, (h - 6) * SCALE],
                radius=8 * SCALE, outline=BORDER, width=SCALE,
            )
            val_text = str(value)
            bbox = draw.textbbox((0, 0), val_text, font=font_val)
            tw = bbox[2] - bbox[0]
            draw.text((x0 + (w_each * SCALE - tw) / 2, 24 * SCALE), val_text,
                       fill=NEON, font=font_val)

            lbl_text = label.upper()
            bbox = draw.textbbox((0, 0), lbl_text, font=font_label)
            tw = bbox[2] - bbox[0]
            draw.text((x0 + (w_each * SCALE - tw) / 2, 66 * SCALE), lbl_text,
                       fill=LABEL, font=font_label)

    img = img.resize((W, h), Image.LANCZOS)
    return img


def main():
    with open(SOCIAL_PATH) as f:
        social = json.load(f)
    username = os.environ.get("GH_USERNAME", social["github_username"])
    token = os.environ.get("GITHUB_TOKEN", "")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    try:
        stats = fetch_stats(username, token)
        fields = [
            ("Repositories", stats["repositories"]),
            ("Commits", stats["commits"] if stats["commits"] is not None else "\u2014"),
            ("Stars", stats["stars"]),
            ("Followers", stats["followers"]),
            ("Following", stats["following"]),
        ]
        img = render_png(fields)
        cache_path = os.path.join(ROOT, "assets", "github-metrics.json")
        with open(cache_path, "w") as f:
            json.dump({"fetched_at": int(time.time()), **stats}, f, indent=2)
        print(f"Wrote {OUT_PATH} with stats: {stats}")
    except Exception as e:
        # No network in this dev environment, or rate-limited without a
        # token - ship a clearly-labeled placeholder instead of crashing.
        # GitHub Actions has real network + GITHUB_TOKEN, so this gets
        # overwritten with real numbers on the first scheduled run there.
        print(f"warning: could not reach GitHub API ({e}); writing placeholder", file=sys.stderr)
        img = render_png([], pending_text="LIVE METRICS PENDING - runs on first GitHub Actions execution")

    img.save(OUT_PATH)


if __name__ == "__main__":
    main()
