---
name: html-magazine
description: "Transforms plain text, markdown, or existing HTML into a beautifully styled self-contained HTML magazine page with a real paper-magazine feel — paginated with page-flip navigation, sourced photography, and print-inspired typography. Use whenever the user says 'turn this into a magazine', 'make this look like a magazine article', 'magazine layout', 'magazine format', or wants content presented as a physical-magazine-style HTML page. Also trigger when the user shares text or markdown and asks for polished publication-quality output, editorial-style layout, or print-quality design. Supports four styles: Editorial (NYT / The Atlantic), Tech Minimal (Wired / MIT Technology Review), Vibrant Lifestyle (Vogue / GQ), and Business (The Economist / Fortune)."
---

# HTML Magazine

Transforms content into a stunning, self-contained HTML magazine page. The result should feel like leafing through a real physical magazine — not reading a website.

This skill is the **editorial brain**. It handles style selection, editorial voice rewriting, image sourcing, and visual specification. It then passes a complete visual brief to the `ui-ux-pro-max` skill, which handles all HTML/CSS/JS rendering.

## Agent Compatibility

This skill uses `AskUserQuestion` for interactive prompts. If `AskUserQuestion` is not available, ask the same questions as plain text and wait for the user to respond.

---

## Workflow

### 1. Collect Content

If the user hasn't provided content, ask for it. Accept:
- **Plain text or markdown** — pasted or typed
- **A file path** — read the file
- **Existing HTML** — extract the text content

### 2. Ask Style

Present four options using `AskUserQuestion`:

1. **Editorial** — NYT / The Atlantic (refined serif, long-form gravitas)
2. **Tech Minimal** — Wired / MIT Technology Review (bold sans, data-forward, high contrast)
3. **Vibrant Lifestyle** — Vogue / GQ (expressive, fashion-forward, rich color)
4. **Business** — The Economist / Fortune (authoritative, institutional, signature red)

If the user already named a style, confirm and continue.

### 3. Ask Rewrite Level

Present four options using `AskUserQuestion`:

1. **Minimal** — Keep original text. Only add magazine elements (headline, kicker, byline, pull quote). Fix grammar.
2. **Light** — Tighten prose, improve flow, add structure. Preserve the author's voice.
3. **Moderate** — Rewrite for magazine quality. Apply the style's editorial voice. Core ideas remain.
4. **Full** — Complete editorial transformation. Fully adopt the style's voice. A new piece inspired by the input.

### 4. Read the Style Reference

Read the relevant reference file:
- `references/editorial.md` — NYT / The Atlantic
- `references/tech-minimal.md` — Wired / MIT Technology Review
- `references/vibrant-lifestyle.md` — Vogue / GQ
- `references/business.md` — The Economist / Fortune

Each file contains two sections:
- **Editorial Voice** — how the writing should sound at this magazine
- **Visual Elements** — colors, typography, layout elements, photography direction

### 5. Rewrite Content

Using the editorial voice section from the style reference, rewrite the content at the chosen level. Create these magazine elements:

- **Kicker** — short category label
- **Headline** — fits the style's tone (Vogue: dramatic, Economist: dry-witted, Wired: bold)
- **Deck** — one hooking sentence
- **Byline** — author name ("Staff Writer" if unknown)
- **Date** — today's date or inferred
- **Lede** — strong opening paragraph matching the style's approach
- **Body sections** — 2-4 named sections with subheadings
- **Pull quote(s)** — the most striking sentence(s)
- **Sidebar/callout** — optional, but required for Business style
- **Image captions** — evocative, matching the editorial voice

### 6. Source Images

Use the **Wikimedia Commons API** to find freely-licensed images. This is the only reliable automated method.

**Step 1 — Search:**
```
WebFetch: https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={terms}&srnamespace=6&srlimit=5&format=json
```
Use search terms from the style reference's Photography Direction section, combined with the article's topic.

**Step 2 — Get image URL:**
```
WebFetch: https://commons.wikimedia.org/w/api.php?action=query&titles={File:filename.jpg}&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1200&format=json
```
Use the `thumburl` (1200px) for the `<img>` src. Extract photographer from `extmetadata.Artist` for attribution.

Aim for **2-4 images**: 1 hero/cover + 1-3 body images.

If Wikimedia returns poor results, fall back to **CSS-only visuals** (gradients, geometric patterns, color blocks).

### 7. Pass to ui-ux-pro-max

Invoke the `ui-ux-pro-max` skill with a complete visual brief. The brief must include everything ui-ux-pro-max needs to generate the HTML — don't assume it knows what a "magazine" looks like.

Construct the brief by combining:
1. The **Visual Elements** section from the style reference (colors, typography, layout elements, photography direction)
2. The **rewritten content** with all magazine elements
3. The **sourced image URLs** with captions and attribution
4. The **rendering specifications** below

**Rendering specifications to include in the brief:**

```
FORMAT: Paper magazine — paginated with page-flip navigation, NOT a scrollable web page.

PAGE DIMENSIONS:
- Pages fill 92% of viewport height (92vh)
- Width derived from height via A4 ratio: calc(92vh / 1.414)
- Pages always horizontally centered on screen
- Dark surface/background behind the pages (color from style spec)
- Gutter shadows on inner edges to simulate binding
- Page numbers on every page

VIEW MODES:
- Single page view: one page centered. Default on viewports < 1100px.
- Two-page spread: two pages side by side like an open magazine. Default on viewports >= 1100px.
- Toggle button in top-right corner to switch modes. Persist choice in localStorage.
- Cover page always displays alone. Spread begins from page 2.
- In spread mode, left and right pages have mirrored gutter shadows (binding simulation).
- In spread mode, navigation advances by two pages.

NAVIGATION:
- Semi-transparent arrow buttons on left/right edges
- Keyboard: ArrowLeft, ArrowRight, Spacebar
- Touch: horizontal swipe support
- Page indicator at bottom center (e.g., "3 / 8" in single, "2–3 / 8" in spread)

PAGES TO GENERATE:
1. Cover — [style-specific cover description from reference]
2. Opening spread — lede with drop cap, byline, deck
3. Body pages — sections with images, pull quotes, sidebars
4. Closing page — final section, author credit, publication footer

IMAGE SOURCING:
- Use these Wikimedia Commons image URLs: [list URLs]
- Search for additional images if needed using Wikimedia Commons API:
  Search: https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={terms}&srnamespace=6&srlimit=5&format=json
  Get URL: https://commons.wikimedia.org/w/api.php?action=query&titles={File:name}&prop=imageinfo&iiprop=url&iiurlwidth=1200&format=json
- If images can't be sourced, use CSS-only visuals (gradients, patterns)

CONSTRAINTS:
- Single self-contained HTML file
- No external dependencies (no CDN fonts, no external CSS/JS)
- System font stacks only (Georgia, Helvetica Neue, Courier New families)
- Must work offline (except sourced image URLs)
- Responsive down to mobile
- Print support via @media print
```

### 8. Save & Present

Save the file to the current working directory as `magazine.html` (or `magazine-2.html` if it exists).

Tell the user:
- Which style was applied
- How many pages were generated
- Suggest opening in a browser

Then offer two optional next steps:

**Share via Vercel:**
> "Would you like to deploy this to Vercel so you can share it with a link?"

If yes, run:
```bash
npx vercel deploy magazine.html --yes
```
If the user isn't authenticated, guide them through `npx vercel login` first.

**Export to PDF:**
> "Would you like to export this as a PDF?"

If yes, run the export script:
```bash
python3 scripts/export-pdf.py magazine.html
```
This requires the `playwright` Python package. If not installed, guide the user to install it: `pip install playwright && playwright install chromium`.

---

## Quality Checklist

Before saving, verify:
- [ ] Pages fill the viewport height — not small floating cards
- [ ] Pages are horizontally centered in both single and spread modes
- [ ] View mode toggle works (single ↔ spread) with localStorage persistence
- [ ] Page-flip navigation works (arrows, keyboard, touch)
- [ ] Cover page has visual impact matching the chosen style
- [ ] Drop cap (or style-appropriate opening treatment) on first paragraph
- [ ] At least one pull quote present and visually distinct
- [ ] Page numbers on every page
- [ ] Images embedded with attribution (or CSS fallback)
- [ ] Editorial voice matches the chosen style and rewrite level
- [ ] File works offline (except image URLs)
