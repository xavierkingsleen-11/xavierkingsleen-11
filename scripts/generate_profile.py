#!/usr/bin/env python3
"""Source-of-truth entry point for the generated GitHub profile dashboard.

The reference workflow is:
Python/source data -> generated SVG/assets -> README.md.
The committed SVG is what GitHub renders.
"""
from pathlib import Path
print("Profile source: assets/profile-dashboard.svg")
print("Edit your profile data and regenerate the SVG before pushing changes.")
