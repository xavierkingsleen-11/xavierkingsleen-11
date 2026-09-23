#!/usr/bin/env python3
"""
Reference-style GitHub profile builder.
Source data -> generated SVG/assets -> README.md.

This script is intentionally the source-of-truth entry point so the visual can
be regenerated instead of hand-editing a huge README.
"""
from pathlib import Path
print("Build pipeline: Python -> SVG/GIF assets -> README.md")
print("Main visual: assets/profile-dashboard.svg")
