#!/usr/bin/env python3
"""
Renders README.md from templates/readme_template.md.j2 using every file in
config/. This is the ONLY script that should touch README.md - never hand
edit the generated file for content that lives in config/, or your edits
will be overwritten next time this runs.

Run:
    python3 scripts/generate_readme.py
"""
import json
import os

from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT, "config")
TEMPLATE_DIR = os.path.join(ROOT, "templates")
OUT_PATH = os.path.join(ROOT, "README.md")


def load(name):
    with open(os.path.join(CONFIG_DIR, f"{name}.json")) as f:
        return json.load(f)


def main():
    context = {
        "profile": load("profile"),
        "skills": load("skills"),
        "tools": load("tools"),
        "education": load("education"),
        "current_focus": load("current_focus"),
        "social": load("social"),
    }

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("readme_template.md.j2")
    rendered = template.render(**context)

    with open(OUT_PATH, "w") as f:
        f.write(rendered)
    print(f"Wrote {OUT_PATH} ({len(rendered)} bytes)")


if __name__ == "__main__":
    main()
