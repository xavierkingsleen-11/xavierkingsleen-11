# Xavier Kingsleen A — GitHub Profile Package

Repository name: `xavierkingsleen-11`

## Structure

```text
README.md
preview.html
requirements.txt
assets/
  hacker-source.jpg
  hacker-blended.png
  hacker-glitch.gif
  profile-dashboard.svg
  skills-radar.svg
scripts/
  generate_profile.py
  generate_glitch.py
.github/
  workflows/
    build-profile.yml
```

The main GitHub-facing visual is `assets/profile-dashboard.svg`. It is generated/source-controlled rather than a screenshot, following the reference approach of using Python/source assets to produce GitHub-compatible SVG output.

`preview.html` is only for local visual checking; GitHub itself renders `README.md`.

The hacker source image is blended into the dashboard and the separate glitch GIF is retained as an asset for future refinement.
