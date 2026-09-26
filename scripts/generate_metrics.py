#!/usr/bin/env python3
"""
Generates assets/github-metrics.svg with REAL data pulled from the GitHub API:
public repo count, total commits (via search API), stars received, followers,
following. No hardcoded/demo numbers are ever written here.

Run locally:
    GH_USERNAME=xavierkingsleen-11 GITHUB_TOKEN=<token or blank> python3 scripts/generate_metrics.py

In GitHub Actions, GITHUB_TOKEN is provided automatically by the runner
(secrets.GITHUB_TOKEN) - see .github/workflows/update-assets.yml.
The token only needs default read-only "public_repo"/read scope; no write
scope is required for the API calls themselves (the workflow's own commit
step is what needs contents:write, handled separately by the workflow).
"""
import json
import os
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "github-metrics.svg")
SOCIAL_PATH = os.path.join(ROOT, "config", "social.json")

API = "https://api.github.com"


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

    # Stars across all public repos (paginate)
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

    # Total commits authored by the user, via the Search API (best-effort;
    # search API is rate-limited and only indexes the default branch).
    commits = None
    try:
        data, _ = gh_get(
            f"{API}/search/commits",
            token,
            params={"q": f"author:{username}"},
        )
        commits = data.get("total_count")
    except Exception as e:  # search API can 422/403 without a token
        print(f"warning: commit search failed ({e}); leaving commits blank", file=sys.stderr)

    return {
        "repositories": public_repos,
        "commits": commits,
        "stars": stars,
        "followers": followers,
        "following": following,
    }


def render_svg(stats):
    fields = [
        ("Repositories", stats["repositories"]),
        ("Commits", stats["commits"] if stats["commits"] is not None else "\u2014"),
        ("Stars", stats["stars"]),
        ("Followers", stats["followers"]),
        ("Following", stats["following"]),
    ]
    w_each = 168
    W = w_each * len(fields)
    H = 96
    BG = "#050b08"
    BORDER = "#1c4a2e"
    NEON = "#39ff8f"
    LABEL = "#7fdba3"

    cells = []
    for i, (label, value) in enumerate(fields):
        x = i * w_each
        cells.append(f"""
    <rect x="{x+6}" y="6" width="{w_each-12}" height="{H-12}" rx="8" fill="none" stroke="{BORDER}" stroke-width="1.4"/>
    <text x="{x + w_each/2}" y="{H/2 - 6}" fill="{NEON}" font-family="Consolas, monospace" font-size="26" text-anchor="middle" font-weight="bold">{value}</text>
    <text x="{x + w_each/2}" y="{H/2 + 24}" fill="{LABEL}" font-family="Consolas, monospace" font-size="12" text-anchor="middle" letter-spacing="1">{label.upper()}</text>""")

    svg = f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {''.join(cells)}
</svg>
"""
    return svg


def render_pending_svg():
    W, H = 640, 96
    return f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="#050b08"/>
  <rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8" fill="none" stroke="#1c4a2e" stroke-width="1.4"/>
  <text x="{W/2}" y="{H/2+6}" fill="#7fdba3" font-family="Consolas, monospace" font-size="14" text-anchor="middle">
    LIVE METRICS PENDING - runs on first GitHub Actions execution
  </text>
</svg>
"""


def main():
    with open(SOCIAL_PATH) as f:
        social = json.load(f)
    username = os.environ.get("GH_USERNAME", social["github_username"])
    token = os.environ.get("GITHUB_TOKEN", "")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    try:
        stats = fetch_stats(username, token)
        svg = render_svg(stats)
        cache_path = os.path.join(ROOT, "assets", "github-metrics.json")
        with open(cache_path, "w") as f:
            json.dump({"fetched_at": int(time.time()), **stats}, f, indent=2)
        print(f"Wrote {OUT_PATH} with stats: {stats}")
    except Exception as e:
        # No network in this environment / rate-limited without a token -
        # ship a clearly-labeled placeholder instead of crashing the build.
        # GitHub Actions has real network + GITHUB_TOKEN, so it will
        # overwrite this with real numbers on first scheduled run.
        print(f"warning: could not reach GitHub API ({e}); writing placeholder", file=sys.stderr)
        svg = render_pending_svg()

    with open(OUT_PATH, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
