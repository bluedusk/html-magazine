# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

**html-magazine** is a Claude Code plugin (skill) that transforms plain text, markdown, or HTML into a self-contained paginated HTML magazine file with page-flip navigation, sourced photography, and print-quality typography.

## Architecture

The project uses a two-layer design:

1. **html-magazine** (`skills/html-magazine/SKILL.md`) — the editorial brain. Handles style selection, content rewriting, sub-style randomization, and passing a complete visual brief to the rendering layer.
2. **ui-ux-pro-max** (external plugin dependency) — the rendering engine. Receives the brief and generates all HTML/CSS/JS. html-magazine never prescribes colors, fonts, or layout details directly.

The skill does not write HTML itself — it always delegates rendering to `ui-ux-pro-max`.

## Slash commands

| Command | File | Purpose |
|---------|------|---------|
| `/html-magazine` | `commands/html-magazine.md` | Invoke the skill to transform content |

## Release process

See `RELEASING.md`. The only file that needs a version bump is `.claude-plugin/plugin.json`. Use `/release` to automate the full flow. Uses semantic versioning: patch for fixes/tweaks, minor for new features/styles, major for breaking changes to the skill interface.

## PDF export

```bash
python3 scripts/export-pdf.py magazine.html
# Optional flags: --output filename.pdf --width 210 --height 297
# Requires: pip install playwright pypdf && playwright install chromium
```

## Evals

Evaluation test cases are defined in `evals/evals.json`. Three scenarios cover Editorial (moderate rewrite), Vibrant Lifestyle (full rewrite), and Tech Minimal (light rewrite). Each case has 11–13 assertions checking HTML structure, CSS properties, navigation, and style-specific visual rules.

## Style system

Four main styles, each with 5 sub-styles in `references/substyles.md`. Sub-styles are always **randomly selected** — never asked of the user, never defaulting to the first option. Each style has a reference file:

- `references/editorial.md` — NYT / The Atlantic
- `references/tech-minimal.md` — Wired / MIT Technology Review
- `references/vibrant-lifestyle.md` — Vogue / GQ
- `references/creator.md` — Dazed / i-D / The Face

Reference files define editorial voice, visual tone, and media mood only — no specific colors or fonts. Visual decisions belong to ui-ux-pro-max.

## Samples site

Demo magazines live in `samples/` and are deployed to **https://samples-six-omega.vercel.app/**.

Vercel project: **bluedusks-projects/samples**

To rebuild the index and deploy:
```bash
python3 scripts/deploy-samples.py              # rebuild index.html + deploy
python3 scripts/deploy-samples.py --no-deploy   # rebuild only
python3 scripts/deploy-samples.py --deploy-only  # deploy without rebuilding
```

The index page (`samples/index.html`) is a hand-crafted magazine shelf gallery with GSAP animations and iframe cover previews. The deploy script can regenerate a simpler version, but the current hand-crafted version should be preserved — use `--deploy-only` to deploy without overwriting it.

## Output constraints

Every generated magazine must be:
- A single self-contained HTML file (no CDN, no external CSS/JS)
- Using system font stacks only (Georgia, Helvetica Neue, Courier New families)
- Pages at 92vh height, width via A4 ratio `calc(92vh / 1.414)`, horizontally centered
- Two-page spread mode default on viewports ≥ 1100px; single page below that
- Including a `Built with html-magazine` watermark linking to the GitHub repo
