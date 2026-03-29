#!/usr/bin/env python3
"""Rebuild samples/index.html from all HTML files and deploy to Vercel.

Usage:
  python3 scripts/deploy-samples.py              # rebuild + deploy
  python3 scripts/deploy-samples.py --no-deploy   # rebuild index.html only
  python3 scripts/deploy-samples.py --deploy-only  # deploy without rebuilding
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(ROOT, "samples")

PALETTES = [
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#1a0a0e 100%)", "accent": "#C8102E", "spine": "#4a0812"},
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#1a1408 100%)", "accent": "#c9a96e", "spine": "#5a4a1e"},
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#181800 100%)", "accent": "#FFE500", "spine": "#6a6a00"},
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#0a1414 100%)", "accent": "#4ECDC4", "spine": "#1a5a52"},
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#140a1e 100%)", "accent": "#7B61FF", "spine": "#2a1170"},
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#1a1008 100%)", "accent": "#FF6B35", "spine": "#6a2a05"},
    {"bg": "#0c0c0c", "grad": "linear-gradient(160deg,#0c0c0c 0%,#0a1018 100%)", "accent": "#00B4D8", "spine": "#004858"},
]


def extract_title(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        head = f.read(4096)
    m = re.search(r"<title>(.*?)</title>", head, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip().split("—")[0].split("|")[0].strip()
    return os.path.splitext(os.path.basename(filepath))[0].replace("-", " ").title()


def get_samples():
    files = sorted(
        f
        for f in os.listdir(SAMPLES_DIR)
        if f.endswith(".html") and f != "index.html"
    )
    samples = []
    for f in files:
        title = extract_title(os.path.join(SAMPLES_DIR, f))
        samples.append({"file": f, "title": title})
    return samples


def build_card(sample, idx):
    p = PALETTES[idx % len(PALETTES)]
    issue = str(idx + 1).zfill(2)
    return f"""      <a href="{sample['file']}" class="mag" style="--accent:{p['accent']};--spine:{p['spine']};--cover-bg:{p['grad']}">
        <div class="mag-spine"></div>
        <div class="mag-cover">
          <div class="mag-cover-inner">
            <span class="mag-issue">Issue {issue}</span>
            <h2 class="mag-title">{sample['title']}</h2>
            <div class="mag-rule"></div>
            <span class="mag-label">html-magazine</span>
          </div>
          <div class="mag-gloss"></div>
        </div>
      </a>"""


TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HTML Magazine — Sample Gallery</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Bodoni:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Public+Sans:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js" defer></script>
<style>
:root {{
  --bg:#06060a;--surface:#111118;--text:#e8e6e1;--text-dim:#777;--text-muted:#444;
  --font-display:'Libre Bodoni',Georgia,serif;
  --font-ui:'Public Sans',-apple-system,Helvetica,Arial,sans-serif;
}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{font-family:var(--font-ui);background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;-webkit-font-smoothing:antialiased;}}

/* ─── HERO ─── */
.hero{{height:100vh;height:100dvh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative;overflow:hidden;}}
.hero::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 50% 40% at 50% 50%,rgba(200,16,46,.05) 0%,transparent 70%);pointer-events:none;}}
.hero-label{{font-size:clamp(10px,1.2vw,12px);font-weight:600;text-transform:uppercase;letter-spacing:.5em;color:var(--text-muted);margin-bottom:28px;opacity:0;}}
.hero-title{{font-family:var(--font-display);font-size:clamp(52px,11vw,150px);font-weight:400;letter-spacing:-.025em;line-height:.88;opacity:0;}}
.hero-title em{{font-style:italic;color:#C8102E;}}
.hero-sub{{font-size:clamp(13px,1.4vw,17px);font-weight:300;color:var(--text-dim);margin-top:20px;letter-spacing:.1em;opacity:0;}}
.hero-line{{width:1px;height:0;background:var(--text-muted);margin-top:48px;}}
.hero-scroll{{font-size:10px;text-transform:uppercase;letter-spacing:.35em;color:var(--text-muted);margin-top:16px;opacity:0;}}

/* ─── SHELF SECTION ─── */
.shelves{{max-width:1200px;margin:0 auto;padding:0 clamp(24px,5vw,80px) clamp(60px,10vw,120px);}}
.shelf-header{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:clamp(40px,6vw,72px);padding-bottom:14px;border-bottom:1px solid #1a1a22;}}
.shelf-title{{font-size:clamp(10px,1vw,12px);font-weight:600;text-transform:uppercase;letter-spacing:.35em;color:var(--text-dim);}}
.shelf-count{{font-size:11px;color:var(--text-muted);letter-spacing:.12em;}}

/* ─── SHELF ROW ─── */
.shelf{{position:relative;margin-bottom:clamp(48px,7vw,80px);}}
.shelf-row{{display:flex;align-items:flex-end;justify-content:center;gap:clamp(16px,2.5vw,32px);padding:0 8px clamp(8px,1.2vw,14px);perspective:1800px;flex-wrap:wrap;}}
.shelf-plank{{height:clamp(10px,1.4vw,16px);background:linear-gradient(180deg,#2a221a 0%,#1e180f 40%,#16120c 100%);border-radius:2px;box-shadow:0 4px 20px rgba(0,0,0,.5),0 1px 0 rgba(255,255,255,.04) inset;position:relative;}}
.shelf-plank::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.06),transparent);}}

/* ─── MAGAZINE CARD ─── */
.mag{{
  width:clamp(130px,17vw,190px);aspect-ratio:210/297;
  position:relative;display:block;text-decoration:none;color:inherit;
  transform-style:preserve-3d;
  transform:rotateY(-6deg) translateZ(0);
  transition:transform .5s cubic-bezier(.4,0,.2,1),box-shadow .5s cubic-bezier(.4,0,.2,1);
  box-shadow:-3px 3px 10px rgba(0,0,0,.5),-1px 1px 3px rgba(0,0,0,.3);
  cursor:pointer;
  opacity:0;
}}
.mag:hover{{
  transform:rotateY(0deg) translateY(-28px) scale(1.08) translateZ(0);
  box-shadow:0 24px 48px rgba(0,0,0,.55),0 8px 16px rgba(0,0,0,.3);
  z-index:10;
}}

/* Spine */
.mag-spine{{
  position:absolute;left:0;top:0;bottom:0;width:clamp(6px,.8vw,10px);
  background:var(--spine);border-radius:2px 0 0 2px;z-index:2;
  box-shadow:1px 0 4px rgba(0,0,0,.3) inset;
}}

/* Cover surface */
.mag-cover{{
  position:absolute;inset:0;overflow:hidden;border-radius:2px;
  background:var(--cover-bg);
}}

.mag-cover-inner{{
  position:absolute;inset:0;
  display:flex;flex-direction:column;justify-content:center;align-items:center;
  padding:clamp(16px,3%,32px) clamp(12px,4%,24px);
  text-align:center;
}}

/* Gloss / shine */
.mag-gloss{{
  position:absolute;inset:0;z-index:5;pointer-events:none;
  background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.03) 45%,rgba(255,255,255,.07) 50%,rgba(255,255,255,.03) 55%,transparent 70%);
  opacity:0;transition:opacity .4s;
}}
.mag:hover .mag-gloss{{opacity:1;}}

/* Cover typography */
.mag-issue{{
  font-family:var(--font-ui);
  font-size:clamp(7px,.9vw,9px);font-weight:600;
  text-transform:uppercase;letter-spacing:.3em;
  color:var(--accent);opacity:.6;
  position:absolute;top:clamp(12px,2%,20px);
}}

.mag-title{{
  font-family:var(--font-display);
  font-size:clamp(14px,2.2vw,22px);font-weight:500;
  color:#e8e6e1;letter-spacing:.03em;line-height:1.2;
}}

.mag-rule{{
  width:24px;height:2px;background:var(--accent);
  margin:clamp(8px,1.2vw,14px) auto;
}}

.mag-label{{
  font-family:var(--font-ui);
  font-size:clamp(6px,.7vw,8px);font-weight:600;
  text-transform:uppercase;letter-spacing:.25em;
  color:var(--text-muted);
  position:absolute;bottom:clamp(12px,2%,20px);
}}

/* ─── FOOTER ─── */
.footer{{text-align:center;padding:clamp(40px,6vw,72px) 20px;border-top:1px solid #1a1a22;margin-top:clamp(20px,4vw,40px);}}
.footer-text{{font-size:12px;color:var(--text-muted);letter-spacing:.1em;}}
.footer-link{{color:var(--text-dim);text-decoration:none;transition:color .2s;}}
.footer-link:hover{{color:var(--text);}}

/* ─── RESPONSIVE ─── */
@media(max-width:640px){{
  .shelf-row{{gap:12px;}}
  .mag{{width:clamp(110px,40vw,150px);}}
}}
@media(prefers-reduced-motion:reduce){{
  *,*::before,*::after{{animation-duration:.01ms!important;transition-duration:.01ms!important;}}
  .mag{{opacity:1!important;transform:none!important;}}
}}
</style>
</head>
<body>

<section class="hero">
  <div class="hero-label">Sample Gallery</div>
  <h1 class="hero-title">HTML<em>Magazine</em></h1>
  <p class="hero-sub">AI-generated editorial pages you can flip through</p>
  <div class="hero-line"></div>
  <div class="hero-scroll">Scroll</div>
</section>

<section class="shelves">
  <div class="shelf-header">
    <span class="shelf-title">Issues</span>
    <span class="shelf-count">{count} samples</span>
  </div>
{shelves}
</section>

<footer class="footer">
  <p class="footer-text">
    Built with <a href="https://github.com/bluedusk/html-magazine" class="footer-link">html-magazine</a>
    — a Claude Code plugin
  </p>
</footer>

<script>
document.addEventListener('DOMContentLoaded',()=>{{
  if(typeof gsap==='undefined')return;
  gsap.registerPlugin(ScrollTrigger);

  /* Hero entrance */
  const tl=gsap.timeline({{defaults:{{ease:'power3.out'}}}});
  tl.to('.hero-label',{{opacity:1,duration:.8,delay:.3}})
    .from('.hero-title',{{y:50,duration:1,ease:'power4.out'}},'-=.5')
    .to('.hero-title',{{opacity:1,duration:.8}},'-=.8')
    .to('.hero-sub',{{opacity:1,duration:.6}},'-=.3')
    .to('.hero-line',{{height:56,duration:.8,ease:'power2.inOut'}},'-=.2')
    .to('.hero-scroll',{{opacity:1,duration:.5}},'-=.3');
  gsap.to('.hero-scroll',{{opacity:.3,duration:1.2,repeat:-1,yoyo:true,ease:'sine.inOut',delay:2.5}});

  /* Shelf plank slide-in */
  gsap.utils.toArray('.shelf-plank').forEach(plank=>{{
    gsap.from(plank,{{
      scaleX:0,opacity:0,duration:.8,ease:'power3.out',
      scrollTrigger:{{trigger:plank,start:'top 90%',once:true}}
    }});
  }});

  /* Magazine entrance — slide up from shelf, rotate in */
  gsap.utils.toArray('.mag').forEach((m,i)=>{{
    const row=m.closest('.shelf-row');
    const siblings=Array.from(row.children);
    const localIdx=siblings.indexOf(m);
    gsap.to(m,{{
      opacity:1,duration:.6,delay:localIdx*.12,
      ease:'power3.out',
      scrollTrigger:{{trigger:row,start:'top 85%',once:true}}
    }});
    gsap.from(m,{{
      y:60,rotateY:-20,duration:.8,delay:localIdx*.12,
      ease:'back.out(1.4)',
      scrollTrigger:{{trigger:row,start:'top 85%',once:true}}
    }});
  }});

  /* 3D tilt on mousemove */
  document.querySelectorAll('.mag').forEach(card=>{{
    card.addEventListener('mousemove',e=>{{
      const r=card.getBoundingClientRect();
      const x=(e.clientX-r.left)/r.width-.5;
      const y=(e.clientY-r.top)/r.height-.5;
      gsap.to(card.querySelector('.mag-gloss'),{{
        background:`linear-gradient(${{115+x*40}}deg,transparent 25%,rgba(255,255,255,.03) 42%,rgba(255,255,255,.09) 50%,rgba(255,255,255,.03) 58%,transparent 75%)`,
        duration:.3
      }});
    }});
  }});
}});
</script>
</body>
</html>"""


PER_SHELF = 4


def rebuild_index(samples):
    # Group samples into shelf rows
    rows = [samples[i : i + PER_SHELF] for i in range(0, len(samples), PER_SHELF)]
    shelves_html = ""
    card_idx = 0
    for row in rows:
        cards = "\n".join(build_card(s, card_idx + i) for i, s in enumerate(row))
        card_idx += len(row)
        shelves_html += f"""  <div class="shelf">
    <div class="shelf-row">
{cards}
    </div>
    <div class="shelf-plank"></div>
  </div>
"""

    html = TEMPLATE.format(count=len(samples), shelves=shelves_html)
    index_path = os.path.join(SAMPLES_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  rebuilt index.html ({len(samples)} samples)")


def deploy():
    print("  deploying to Vercel (production)...")
    result = subprocess.run(
        ["npx", "vercel", "deploy", SAMPLES_DIR, "--yes", "--prod"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        url = result.stdout.strip().splitlines()[-1]
        print(f"  deployed: {url}")
    else:
        print(f"  deploy failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    args = set(sys.argv[1:])
    no_deploy = "--no-deploy" in args
    deploy_only = "--deploy-only" in args

    if not deploy_only:
        samples = get_samples()
        if not samples:
            print("no HTML files found in samples/", file=sys.stderr)
            sys.exit(1)
        rebuild_index(samples)

    if not no_deploy:
        deploy()


if __name__ == "__main__":
    main()
