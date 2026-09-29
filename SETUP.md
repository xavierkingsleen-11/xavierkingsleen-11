# Setup — Xavier Kingsleen A · SOC Profile

## 1. What to upload to GitHub

Create (or reuse) a repository named **exactly** `xavierkingsleen-11`
(your GitHub username) — that special name is what makes GitHub treat its
README as your profile page. Push the **contents** of this `profile/`
folder to that repo's `main` branch (not the `profile` folder itself —
`README.md` must sit at the repo root):

```
README.md
config/
templates/
scripts/
assets/
preview/
.github/workflows/
.gitignore
```

Command-line push (safest — avoids the web uploader silently skipping the
hidden `.github` folder):

```bash
cd profile
git init
git remote add origin https://github.com/xavierkingsleen-11/xavierkingsleen-11.git
git add .
git commit -m "Initial SOC profile"
git branch -M main
git push -u origin main
```

## 2. One-time repo settings

- **Settings → Actions → General → Workflow permissions** → set to
  **"Read and write permissions."** Both workflows commit back to the repo
  (`update-assets.yml`) or push a branch (`snake.yml`), which needs write
  access to the default `GITHUB_TOKEN`.
- No secret/token setup is required beyond that — both workflows use the
  automatic `secrets.GITHUB_TOKEN` GitHub injects into every run.

## 3. ACTION REQUIRED BEFORE YOU PUSH: Skills Radar values

`config/skills.json` currently holds a flat 50% on every radar axis, on
purpose — real skill-level values were never given to me, and I'm not going
to invent them and pass them off as an assessment of you. The generated
image stamps itself **"PLACEHOLDER VALUES"** in small orange text as long
as this is true.

Open `config/skills.json`, set your own numbers for the six axes (SOC/SIEM,
Windows/Linux, Threat Detection, Networking, AWS/Cloud Security,
Scripting/Tools), then change:

```json
"confirmed": false
```
to
```json
"confirmed": true
```

That removes the placeholder stamp. Re-run `python3 scripts/generate_radar.py`
(or just push — the Action does it for you).

## 4. What automatically updates, and how

| What | Source | Trigger |
|---|---|---|
| Skills radar (`assets/skills-radar.png`) | `config/skills.json` | `update-assets.yml`: every 6h, on push to `config/`/`templates/`/`scripts/`, or manual |
| Threat map (`assets/threat-map.gif`) | real Natural Earth land outlines (static file, see §7) | same workflow |
| Live GitHub stats (`assets/github-metrics.png`) | GitHub REST API (real numbers) | same workflow |
| `README.md` | all of `config/*.json` via the template | same workflow |
| Contribution graph (inline in README) | `github-readme-activity-graph` service, live | loads fresh every page view — no workflow needed |
| Contribution snake (`output` branch) | your real contribution calendar | `snake.yml`: daily 03:00 UTC, on push to `main`, or manual |

Both workflows are enabled the moment they're on `main` — nothing else to
switch on beyond the permission in step 2.

## 5. Where you edit things

| To change... | Edit this file |
|---|---|
| Name, role, terminal lines, tagline, About Me, global-monitoring labels, closing quote | `config/profile.json` |
| Skill category cards *and* the radar chart values | `config/skills.json` |
| Tools & Technologies (name + icon) | `config/tools.json` |
| Education entries | `config/education.json` |
| Current Focus bullets | `config/current_focus.json` |
| GitHub/LinkedIn/Portfolio/Email links | `config/social.json` |

## 6. Running things locally

```bash
cd profile
pip install -r scripts/requirements.txt

python3 scripts/generate_radar.py      # config/skills.json -> assets/skills-radar.png
python3 scripts/generate_map.py        # real land-outline data in scripts/data/ -> assets/threat-map.gif
python3 scripts/generate_metrics.py    # live GitHub API -> assets/github-metrics.png
python3 scripts/generate_readme.py     # all config/*.json -> README.md

# Browser preview (full CSS/JS effects GitHub can't run):
python3 -m http.server 8000
# then open http://localhost:8000/preview/index.html
```

### Changing the hero photo

```bash
python3 scripts/generate_hero.py /path/to/new-photo.jpg
```
The one asset not on a schedule — GitHub Actions can't reach a photo that
only lives on your machine.

## 7. Tools & Technologies — where each icon actually comes from

Every icon is a **real product/brand logo**, not a text placeholder. Two
sources, both listed transparently in `config/tools.json`:

- **Bundled locally as PNGs in `assets/icons/`** (Splunk, Windows, Linux,
  PowerShell, AWS, Git, GitHub, HTML5, CSS3, Wireshark, Kali Linux,
  VirusTotal) — rendered once from the Simple Icons / Font Awesome /
  Material Design Icons sets already vendored in this build environment,
  so they can never go down or get rate-limited.
- **Hosted, for the three logos not available in any offline set I had**
  (MITRE ATT&CK, Shodan, Nmap) — `https://github.com/mitre-attack.png`,
  the official MITRE ATT&CK GitHub org's own avatar; `https://github.com/nmap.png`,
  the official Nmap GitHub org's avatar (both served directly by
  GitHub's own CDN — as reliable as your profile picture is); and
  `cdn.jsdelivr.net/gh/selfhst/icons/.../shodan.png`, from the
  community-maintained `selfhst/icons` set built specifically to cover
  tools exactly like this one, served over jsDelivr's GitHub-backed CDN.

To swap any icon: change the `icon` value in `config/tools.json` to any
image URL, or drop a PNG in `assets/icons/` and point to it — no other file
needs to change.

## 8. Design notes worth knowing

- **No SVG anywhere.** `skills-radar.png`, `threat-map.gif`, and
  `github-metrics.png` are all raster PNG/GIF, not SVG.
- **The world map is real.** `scripts/data/land_110m_simplified.py` holds
  actual Natural Earth 1:110m public-domain land-outline coordinates
  (source noted in that file), not a decorative dot cloud — continents are
  geographically recognizable (see README for the credit).
- **Skills Radar values are placeholders until you set them** — see §3.
  They're profile self-assessment visuals either way, never certifications
  or test scores.
- **Both the Contribution Graph and Contribution Snake are kept** — the
  graph pulls your real calendar live from `github-readme-activity-graph`
  on every page view, the snake is regenerated daily from real contribution
  data by `snake.yml`. Neither is a fake/invented duplicate of the other;
  they show the same underlying real data two different ways (calendar vs.
  animated snake), which is why both are worth keeping rather than picking
  one.
- **No System Status panel.** It was in an earlier reference image but
  isn't part of the current 15-section spec, so it's been dropped rather
  than carried forward automatically.

## 9. What renders differently on GitHub vs. the local preview

- The **typing animation, cursor-blinks-only-after-typing, and CSS glitch
  flash** in `preview/index.html` are local-development-only — GitHub's
  markdown renderer doesn't execute JavaScript or custom CSS. On GitHub,
  the equivalent hero effect comes from `assets/hero-hacker.gif`, a real
  animated image (clear → ~0.3–0.5s CCTV-style glitch → clear, on an ~9s
  loop) that plays natively, no JS involved.
- The threat map's scan sweep, node pulses and packet-travel animation are
  baked into `threat-map.gif` as real frames, so they play identically on
  GitHub and in the preview.
- The preview's tool icons and layout are pulled live from the same
  `config/tools.json` / other config files via `fetch()`, so they always
  match what `generate_readme.py` would produce.

## 10. Validation performed / what to double-check yourself

Done in this build: JSON validity, YAML validity of both workflows,
end-to-end script run with no errors, filename/path consistency between
README and `assets/`, confirmed zero `.svg` files anywhere in the project,
confirmed every tool in `config/tools.json` resolves to either a local PNG
that exists on disk or a real hosted logo URL, and visual inspection of the
generated hero, map and radar frames.

Not possible to verify from here (no live GitHub/network access in this
sandboxed build environment) — please confirm once pushed:
- That the three hosted icon URLs (MITRE ATT&CK, Nmap, Shodan) load
  correctly on github.com — they were verified to be correct, real,
  currently-live URLs via web search, but couldn't be loaded pixel-by-pixel
  from inside this environment.
- That both Actions run successfully on first push (check the **Actions**
  tab) and that `assets/github-metrics.png` swaps from its placeholder to
  real numbers within the first run.
- Your real Skills Radar values are in and `confirmed: true` is set (§3).
- Email address is `xavier.cloudsec@gmail.com` in `config/social.json` —
  confirm that's the one you want live.
