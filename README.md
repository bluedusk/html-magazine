# HTML Magazine

Transform plain text, markdown, or HTML into stunning paginated magazine pages — with editorial voice rewriting, sourced photography, and print-quality typography. Share via Vercel, export to PDF.

**[Live Demo](https://samples-six-omega.vercel.app)** | Works with **Claude Code**, **Gemini CLI**, **GitHub Copilot**, and **OpenAI Codex**

## Install

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/bluedusk/html-magazine/main/remote-install.sh | bash
```

### Manual

```bash
git clone https://github.com/bluedusk/html-magazine.git
cd html-magazine
bash install.sh
```

### What the installer does

1. **Detects your agents** — scans for `claude`, `gemini`, `gh` (Copilot), `codex`
2. **Installs ui-ux-pro-max** (required dependency) for each detected agent:
   - Claude Code → `claude plugin install ui-ux-pro-max`
   - Gemini / Copilot / Codex → `npx uipro-cli init --ai <agent>`
3. **Installs html-magazine** for each detected agent:
   - Claude Code → plugin system
   - Gemini CLI → symlink to `~/.gemini/skills/`
   - Copilot → symlink to `.github/skills/` (project-level)
   - Codex → symlink to `~/.codex/skills/`
4. **Asks install scope** — user-level (all projects) or project-level (current project only)

### Requirements

- **Node.js** — needed for `npx uipro-cli` (non-Claude agents)
- **Git** — for cloning

### Agent-specific install

If you only want one agent:

```bash
# Claude Code only
claude plugin marketplace add bluedusk/html-magazine
claude plugin install html-magazine

# Gemini CLI only
ln -s /path/to/html-magazine ~/.gemini/skills/html-magazine

# Copilot only (project-level)
ln -s /path/to/html-magazine .github/skills/html-magazine

# Codex only
ln -s /path/to/html-magazine ~/.codex/skills/html-magazine
```

Don't forget to install ui-ux-pro-max separately for your agent.

---

## Usage

**Claude Code:**
```
/html-magazine
```

**Any agent — just ask naturally:**

> Turn this article into a magazine

> Make this look like a Vogue magazine page

> Convert this blog post to a National Geographic style magazine

---

## How It Works

1. **You provide content** — paste text, markdown, or point to a file
2. **Pick a style** — choose from 4 iconic magazine aesthetics
3. **Pick a rewrite level** — from minimal cleanup to full editorial transformation
4. **Get a magazine** — a single HTML file with paginated pages, page-flip navigation, and sourced images
5. **Share or export** — deploy to Vercel or export as PDF

## Styles

| Style | Inspired By | Visual Feel | Writing Voice |
|-------|-------------|-------------|---------------|
| **Editorial** | NYT Magazine / The Atlantic | Serif, dark covers, crimson accents | Measured, literary, scene-setting |
| **Tech Minimal** | Wired / MIT Technology Review | Bold sans, neon green, gradient rules | Sharp, data-forward, declarative |
| **Vibrant Lifestyle** | Vogue / GQ | Gold accents, wide margins, full-bleed photos | Sensory, confident, vivid |
| **Creator** | Dazed / i-D / The Face | Bold sans, one pop color, collage energy | Casual, authentic, internet-native |

## Rewrite Levels

| Level | What It Does |
|-------|-------------|
| **Minimal** | Keep original text. Add magazine structure (headline, kicker, pull quote). |
| **Light** | Tighten prose, improve flow. Preserve the author's voice. |
| **Moderate** | Rewrite for magazine quality. Apply the style's editorial voice. |
| **Full** | Complete transformation. A new piece of writing in the magazine's voice. |

## Features

- **Paginated layout** — fixed pages with page-flip navigation, not a scrollable web page
- **Single & spread modes** — toggle between one page and two-page spread (like an open magazine)
- **Editorial voice** — each style has a distinct writing personality that shapes the content
- **Image sourcing** — pulls real photos from Wikimedia Commons (no API key needed)
- **PDF export** — convert to PDF via `python3 scripts/export-pdf.py magazine.html`
- **Vercel deploy** — share your magazine with a public link
- **Self-contained** — single HTML file, works offline (except images)
- **Multi-agent** — works across Claude Code, Gemini, Copilot, and Codex

## Architecture

```
User provides content
        |
  html-magazine (editorial brain)
    1. Ask style + rewrite level
    2. Rewrite content with editorial voice
    3. Source images from Wikimedia Commons
    4. Build visual brief (colors, typography, layout elements)
        |
  ui-ux-pro-max (rendering engine)
    5. Generate paginated HTML with page-flip, spreads, print typography
        |
  Output: magazine.html
    6. Optional: deploy to Vercel or export to PDF
```

**html-magazine** handles style, editorial voice, content rewriting, and image sourcing.
**ui-ux-pro-max** handles all HTML, CSS, JS, and visual design quality.

## Optional Dependencies

| Dependency | For | Install |
|-----------|-----|---------|
| Playwright | PDF export | `pip install playwright && playwright install chromium` |
| Vercel CLI | Sharing via link | `npm i -g vercel` (or use `npx vercel deploy`) |

## License

MIT
