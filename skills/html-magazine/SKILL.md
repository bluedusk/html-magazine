---
name: html-magazine
description: "Transforms plain text, markdown, existing HTML, or images into a beautifully styled self-contained HTML magazine page with a real paper-magazine feel — paginated with page-flip navigation, sourced photography, and print-inspired typography. Use whenever the user says 'turn this into a magazine', 'make this look like a magazine article', 'magazine layout', 'magazine format', or wants content presented as a physical-magazine-style HTML page. Also trigger when the user shares text, markdown, or an image and asks for polished publication-quality output, editorial-style layout, or print-quality design. Supports four styles: Editorial (NYT / The Atlantic), Tech Minimal (Wired / MIT Technology Review), Vibrant Lifestyle (Vogue / GQ), and Business (The Economist / Fortune)."
---

# HTML Magazine

Transforms content into a stunning, self-contained HTML magazine page. The result should feel like leafing through a real physical magazine — not reading a website.

This skill is the **editorial brain**. It handles style selection, editorial voice rewriting, image sourcing, and visual specification. It then passes a complete visual brief to the `ui-ux-pro-max` skill, which handles all HTML/CSS/JS rendering.

## Agent Compatibility

This skill works across multiple AI coding agents:

- **Claude Code** — full support, uses `AskUserQuestion` for prompts, `ui-ux-pro-max` plugin for rendering
- **Gemini CLI** — uses `activate_skill` for skill loading, plain text prompts for user interaction
- **GitHub Copilot** — plain text prompts, follows skill instructions directly
- **OpenAI Codex** — plain text prompts, follows skill instructions directly

If `AskUserQuestion` is not available, ask the same questions as plain text in the conversation and wait for the user to respond before proceeding. If `ui-ux-pro-max` is not available, generate the HTML directly using the visual element specifications from the style references.

---

## Workflow

### 1. Collect Content

If the user hasn't provided content, ask for it and **wait for their response before proceeding to Step 2**. Do not ask about style or rewrite level until content has been received. Accept:
- **Plain text or markdown** — pasted or typed
- **A file path** — read the file
- **Existing HTML** — extract the text content
- **An image** — file path or pasted image; use vision to read it, then extract all visible text and describe any visual context (charts, photos, diagrams) as prose. Treat the extracted content as the input text for the magazine.

### 2. Ask Style

Present four options using `AskUserQuestion`:

1. **Editorial** — NYT / The Atlantic (refined, literary, immersive)
2. **Tech** — Wired / MIT Technology Review (sharp, data-forward, futuristic)
3. **Fashion** — Vogue / GQ (luxurious, sensory, photo-forward)
4. **Creator** — Dazed / i-D / The Face (bold, authentic, youth culture)

If the user already named a style, confirm and continue.

### 3. Ask Rewrite Level

Present four options using `AskUserQuestion`:

1. **Minimal** — Keep original text. Only add magazine elements (headline, kicker, byline, pull quote). Fix grammar.
2. **Light** — Tighten prose, improve flow, add structure. Preserve the author's voice.
3. **Moderate** — Rewrite for magazine quality. Apply the style's editorial voice. Core ideas remain.
4. **Full** — Complete editorial transformation. Fully adopt the style's voice. A new piece inspired by the input.

### 3b. Ask Media Preference

Present three options using `AskUserQuestion`:

1. **Images** — Source and embed photographs that match the content and style
2. **Images + Video** — Source photographs and background video loops for key pages
3. **None** — Pure CSS/SVG decorative design (geometric patterns, gradients, abstract shapes — no external media)

### 4. Read the Style Reference

Read the relevant reference file:
- `references/editorial.md` — NYT / The Atlantic
- `references/tech-minimal.md` — Wired / MIT Technology Review
- `references/vibrant-lifestyle.md` — Vogue / GQ
- `references/creator.md` — Dazed / i-D / The Face

Each file contains:
- **Editorial Voice** — how the writing should sound
- **Visual Tone** — the feeling and mood (not specific colors or fonts)
- **Media Mood** — what kind of imagery to find

### 4b. Pick a Random Sub-Style

Read `references/substyles.md`. Each style has 5 sub-styles. **Randomly pick one** — do not ask the user, do not always pick the first one. This ensures every magazine looks different even when the same style is chosen.

Include the sub-style name and its one-line description in the prompt to ui-ux-pro-max. For example, if the user picked Creator and you randomly selected "lo-fi analog film," include:

> Style: youth culture magazine (like Dazed, i-D, The Face), with a lo-fi analog film feel — grain, muted tones, disposable camera vibes, nostalgic warmth

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

### 6. Pass to ui-ux-pro-max

Invoke the `ui-ux-pro-max` skill. The prompt should include:

1. **Style line** — the magazine family + randomly picked sub-style (e.g., "youth culture magazine like Dazed/i-D, with a pastel collage scrapbook feel")
2. **Editorial voice** — from the style reference (so ui-ux-pro-max understands the tone)
3. **Media mood** — from the style reference (so it knows what images/videos to find)
4. **Media preference** — the user's choice: "images", "images + video", or "none (pure CSS/SVG)"
5. **Rewritten content** — all magazine elements (masthead, kicker, headline, deck, byline, sections, pull quotes)
6. **Rendering requirements** — below

Do not prescribe colors, fonts, or layout details. Let ui-ux-pro-max make all visual decisions based on the style line and its own design system.

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

IMAGES & MEDIA (follow the user's media preference):

If media preference is "images":
- You (ui-ux-pro-max) are responsible for sourcing photographs that match the content
- Search for and embed relevant images that complement the article
- Follow the media mood from the style reference included above
- If you can't find suitable media, fall back to CSS-only visuals for that element

If media preference is "images + video":
- Source both photographs and background video loops
- Use background video loops (muted, autoplay, looping) on key pages — cover, section openers, or visual breaks. Pause/play videos based on page visibility.
- Follow the media mood from the style reference included above
- If you can't find suitable media, fall back to CSS-only visuals for that element

If media preference is "none":
- Do NOT source or embed any external images or videos
- Use pure CSS and inline SVG for ALL visual elements
- Create striking decorative designs: geometric patterns, gradients, abstract shapes, clip-path compositions, SVG illustrations, ornamental borders, and color blocks
- Each page should have strong visual identity through CSS/SVG art alone
- This should feel intentionally designed, not like missing images — think art zine, brutalist editorial, or modernist print

BRANDING:
- Add a small "Built with html-magazine" watermark in the bottom-right corner of the page
- Fixed position, always visible, subtle and unobtrusive
- "html-magazine" should be a link to https://github.com/bluedusk/html-magazine
- Style: semi-transparent, small font (10-11px), sans-serif
- Example CSS:
  .branding { position: fixed; bottom: 12px; right: 16px; font-family: sans-serif;
    font-size: 10px; color: rgba(255,255,255,0.3); z-index: 9999; letter-spacing: 0.05em; }
  .branding a { color: inherit; text-decoration: none; }
  .branding a:hover { color: rgba(255,255,255,0.6); }
- Example HTML: <div class="branding">Built with <a href="https://github.com/bluedusk/html-magazine" target="_blank">html-magazine</a></div>

CONSTRAINTS:
- Single self-contained HTML file
- No external dependencies (no CDN fonts, no external CSS/JS)
- System font stacks only (Georgia, Helvetica Neue, Courier New families)
- Must work offline (except sourced image URLs)
- Responsive down to mobile
- Print support via @media print (hide branding in print)
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
- [ ] Media matches user preference (images, images+video, or pure CSS/SVG)
- [ ] Editorial voice matches the chosen style and rewrite level
- [ ] File works offline (except image URLs)
