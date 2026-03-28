# HTML Magazine

A Claude Code plugin that transforms plain text, markdown, or HTML into stunning paginated magazine pages — with editorial voice rewriting, sourced photography, and print-quality typography.

## Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/bluedusk/html-magazine/main/remote-install.sh | bash
```

## Manual Install

```bash
git clone https://github.com/bluedusk/html-magazine.git
cd html-magazine
bash install.sh
```

## Usage

```
/html-magazine
```

Or just ask naturally:

> Turn this article into a magazine

> Make this look like a Vogue magazine page

## How It Works

1. **You provide content** — paste text, markdown, or point to a file
2. **Pick a style** — choose from 4 iconic magazine aesthetics
3. **Pick a rewrite level** — from minimal cleanup to full editorial transformation
4. **Get a magazine** — a single HTML file with paginated pages, page-flip navigation, and sourced images

## Styles

| Style | Inspired By | Feel |
|-------|-------------|------|
| **Editorial** | NYT Magazine / The Atlantic | Refined serif, long-form gravitas, dark moody covers |
| **Tech Minimal** | Wired / MIT Technology Review | Bold sans, neon accents, data-forward, high contrast |
| **Vibrant Lifestyle** | Vogue / GQ | Elegant serif, gold accents, fashion-forward, luxurious white space |
| **Business** | The Economist / Fortune | Two-column, signature red, authoritative, information-dense |

## Rewrite Levels

| Level | What It Does |
|-------|-------------|
| **Minimal** | Keep original text. Add magazine elements (headline, kicker, pull quote). |
| **Light** | Tighten prose, improve flow. Preserve the author's voice. |
| **Moderate** | Rewrite for magazine quality. Apply the style's editorial voice. |
| **Full** | Complete transformation. A new piece of writing in the magazine's voice. |

## Features

- **Paginated layout** — fixed pages with page-flip navigation, not a scrollable web page
- **Single & spread modes** — toggle between one page and two-page spread (like an open magazine)
- **Editorial voice** — each style has a distinct writing personality
- **Image sourcing** — pulls real photos from Wikimedia Commons (no API key needed)
- **PDF export** — convert to PDF via `python3 scripts/export-pdf.py magazine.html`
- **Vercel deploy** — share your magazine with a public link
- **Self-contained** — single HTML file, works offline (except images)

## Architecture

html-magazine is the **editorial brain**. It handles:
- Style selection and editorial voice matching
- Content rewriting at the chosen level
- Image sourcing from Wikimedia Commons
- Translating magazine concepts into concrete visual specifications

It delegates **HTML rendering** to the [ui-ux-pro-max](https://github.com/Industry-Pro-Max/ui-ux-pro-max-skill) plugin, which handles all CSS, layout, and visual design quality.

## Dependencies

- **Claude Code** — required
- **ui-ux-pro-max** — auto-installed by the install script

## Optional Dependencies

- **Playwright** — for PDF export (`pip install playwright && playwright install chromium`)
- **Vercel CLI** — for sharing (`npx vercel deploy`)

## License

MIT
