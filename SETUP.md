# Setup — Xavier Kingsleen A · SOC Profile

## 1. What to upload to GitHub

Create (or reuse) a repository named **exactly** `xavierkingsleen-11`
(your GitHub username) — that special name is what makes GitHub treat its
README as your profile page. Push everything in this folder to that repo's
`main` branch:

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

## 2. One-time repo settings

- **Settings → Actions → General → Workflow permissions** → set to
  **"Read and write permissions."** Both workflows commit back to the repo
  (`update-assets.yml`) or push a branch (`snake.yml`), which needs write
  access to the default `GITHUB_TOKEN`.
- No secret/token setup is required beyond that. Both workflows use the
  automatic `secrets.GITHUB_TOKEN` GitHub injects into every run — nothing
  to create or paste in yourself. (If you ever want higher Search-API rate
  limits for commit counts, you could add a personal access token as a repo
  secret and reference it in `generate_metrics.py`, but it's optional.)

## 3. What automatically updates, and how

| What | Workflow | Trigger |
|---|---|---|
| Live GitHub stats card (`assets/github-metrics.svg`) | `update-assets.yml` | every 6 hours, or on push to `config/`/`templates/`/`scripts/`, or manual |
| Skills radar (`assets/skills-radar.svg`) | `update-assets.yml` | same as above (regenerated from `config/skills.json`) |
| Threat map (`assets/threat-map.svg`) | `update-assets.yml` | same as above |
| `README.md` | `update-assets.yml` | re-rendered from `templates/readme_template.md.j2` + all `config/*.json` every time the above runs |
| Contribution snake (`output` branch, referenced in README) | `snake.yml` | daily at 03:00 UTC, on push to `main`, or manual |

Both workflows are already enabled by default the moment they're on `main` —
you don't need to flip anything on beyond the permissions in step 2.

## 4. Where you edit things

Everything you listed as "must stay editable" lives in `config/*.json`.
Change a value, commit/push — `update-assets.yml` re-renders `README.md`
for you within minutes (or push it yourself to trigger immediately).

| To change... | Edit this file |
|---|---|
| Name, role, tagline, terminal lines, system status, About Me, global-monitoring labels, closing quote | `config/profile.json` |
| Skill category cards *and* the radar chart values | `config/skills.json` |
| Tools & technologies icons | `config/tools.json` |
| Education entries | `config/education.json` |
| Current Focus bullets | `config/current_focus.json` |
| GitHub/LinkedIn/Portfolio/Email links | `config/social.json` |

None of these require touching SVG markup, HTML, or the template by hand.

## 5. Running things locally

```bash
cd profile
pip install -r scripts/requirements.txt

python3 scripts/generate_radar.py      # config/skills.json      -> assets/skills-radar.svg
python3 scripts/generate_map.py        # (static, edit NODES in the script) -> assets/threat-map.svg
python3 scripts/generate_metrics.py    # live GitHub API          -> assets/github-metrics.svg
python3 scripts/generate_readme.py     # all config/*.json        -> README.md

# Browser preview (closer to the approved design than GitHub's renderer):
python3 -m http.server 8000
# then open http://localhost:8000/preview/index.html
```

`preview/index.html` fetches the same `config/*.json` files, so it must be
served over `http://`, not opened directly as a `file://` path (the browser
blocks `fetch()` of local files without a server).

### Changing the hero photo

```bash
python3 scripts/generate_hero.py /path/to/new-photo.jpg
```

This is the one asset not on a schedule — it only needs to be re-run when
you actually swap photos, since GitHub Actions can't reach a photo that
lives on your machine.

## 6. What will render differently on GitHub vs. the local preview

- The **typing animation, blinking cursor, and CSS glitch flash** in
  `preview/index.html` are for local development only — GitHub's markdown
  renderer does not execute JavaScript or custom CSS. On GitHub, the
  equivalent hero effect comes from `assets/hero-hacker.gif`, a real
  animated image (clear → ~0.3–0.5s CCTV-style glitch → clear, on an ~9s
  loop), which **does** play on GitHub.
- The skills radar and threat map are SVGs using native SVG `<animate>`
  (SMIL), not CSS/JS — these keep their subtle pulse/glow when GitHub loads
  them as `<img>`, unlike the JS-driven preview hover states.
- Hover states, hover-triggered transitions, and hover tooltips in the
  preview have no GitHub equivalent and simply won't be there on the
  profile page.

## 7. Validation performed / what to double-check yourself

Done in this build: JSON validity, YAML validity of both workflows,
end-to-end script run with no errors, filename case-consistency between
README and `assets/`, and a local visual proof (markdown-to-HTML render) of
the overall layout.

Not possible to verify from here (no live GitHub/network access in this
environment) — please confirm once pushed:
- The exact visual rendering of nested Markdown-inside-`<table><td>` blocks
  on github.com itself. This is a long-established, widely used GitHub
  README technique (blank line after the opening tag, blank line before the
  closing tag), but I could not load github.com to screenshot it directly —
  if any card looks off, the usual fix is making sure a blank line
  immediately follows every `<td>` and precedes every `</td>`.
- That both Actions run successfully on first push (check the **Actions**
  tab) and that `assets/github-metrics.svg` swaps from the "LIVE METRICS
  PENDING" placeholder to real numbers within the first scheduled run.
- Email address: pulled from your previous portfolio README
  (`xavierkingsleen@gmail.com`) since you didn't attach one for this
  request — confirm it's current in `config/social.json`.
