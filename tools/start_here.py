"""'Start Here' Instagram highlight for COBU, built from the brand book identity.
Output: 1080x1920 PNGs (Instagram's native story size), rendered at 2x and downsampled."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from identity import art, NAVY, WARM, MUSTARD, MIST, INK
from PIL import Image
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).resolve().parent.parent / "instagram" / "highlights" / "01-start-here"; OUT.mkdir(parents=True, exist_ok=True)
TMP = pathlib.Path(__file__).resolve().parent / ".tmp"; TMP.mkdir(parents=True, exist_ok=True)
BATTER, VALVE = "#F0D48A", "#C8372D"


def vb(bb, pad=0.0):
    x0, y0, x1, y1 = bb; w, h = x1 - x0, y1 - y0
    return f"{x0-w*pad:.1f} {y0-h*pad:.1f} {w*(1+2*pad):.1f} {h*(1+2*pad):.1f}"


def W(fill, style=""):
    inner, bb = art("wordmark", fill); return f'<svg viewBox="{vb(bb)}" style="{style}" role="img" aria-label="COBU">{inner}</svg>'


def I(fill, style="", lid=None):
    inner, bb = art("icon", fill, lid); return f'<svg viewBox="{vb(bb)}" style="{style}" role="img" aria-label="COBU pot">{inner}</svg>'


# Flat brand-style illustration of the dispenser (red valve tip, screw lid, clear body, whisk ball, screw-off base)
BOTTLE = f'''<svg viewBox="0 0 400 1000" style="height:100%;display:block" role="img" aria-label="Pancake batter dispenser">
  <path d="M176 20h48l12 92h-72z" fill="{VALVE}"/>
  <rect x="152" y="104" width="96" height="18" rx="4" fill="{WARM}" stroke="{NAVY}" stroke-width="6"/>
  <rect x="112" y="122" width="176" height="56" rx="10" fill="{WARM}" stroke="{NAVY}" stroke-width="6"/>
  <rect x="96" y="174" width="208" height="104" rx="14" fill="{WARM}" stroke="{NAVY}" stroke-width="6"/>
  <path d="M104 278h192l26 590H78z" fill="#FFFFFF" fill-opacity=".55" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/>
  <path d="M93 520h214l15 348H78z" fill="{BATTER}"/>
  <path d="M104 278h192l26 590H78z" fill="none" stroke="{NAVY}" stroke-width="6" stroke-linejoin="round"/>
  <path d="M120 320l-10 500" stroke="#FFFFFF" stroke-width="12" stroke-linecap="round" opacity=".8"/>
  <g fill="none" stroke="{NAVY}" stroke-width="5" opacity=".85">
    <circle cx="200" cy="700" r="62"/><ellipse cx="200" cy="660" rx="58" ry="14"/><ellipse cx="200" cy="700" rx="62" ry="20"/><ellipse cx="200" cy="740" rx="58" ry="14"/>
  </g>
  <rect x="70" y="860" width="260" height="120" rx="18" fill="{WARM}" stroke="{NAVY}" stroke-width="6"/>
  <line x1="78" y1="884" x2="322" y2="884" stroke="{NAVY}" stroke-width="4" opacity=".35"/>
</svg>'''

CSS = f'''
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; }}
body {{ font-family: "Archivo", sans-serif; -webkit-font-smoothing: antialiased; }}
.s {{ width: 1080px; height: 1920px; position: relative; display: flex; flex-direction: column; padding: 300px 96px 330px; }}
.navy {{ background: {NAVY}; color: {WARM}; }} .warm {{ background: {WARM}; color: {INK}; }} .mist {{ background: {MIST}; color: {NAVY}; }}
.lbl {{ font-stretch: 125%; font-weight: 600; font-size: 30px; letter-spacing: .2em; text-transform: uppercase; color: {MUSTARD}; }}
.navy .lbl {{ color: {MUSTARD}; }} .warm .lbl, .mist .lbl {{ color: #B07F1F; }}
h1 {{ font-stretch: 125%; font-weight: 600; font-size: 92px; line-height: 1.04; letter-spacing: -.01em; }}
.warm h1, .mist h1 {{ color: {NAVY}; }}
p {{ font-size: 40px; line-height: 1.45; }}
.foot {{ position: absolute; left: 96px; right: 96px; bottom: 300px; display: flex; justify-content: space-between; align-items: center; font-stretch: 125%; font-weight: 500; font-size: 26px; letter-spacing: .16em; text-transform: uppercase; opacity: .75; }}
.pill {{ display: inline-flex; align-items: center; gap: 18px; background: {MUSTARD}; color: {NAVY}; font-stretch: 125%; font-weight: 600; font-size: 34px; letter-spacing: .04em; padding: 30px 46px; border-radius: 999px; }}
'''

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700&display=swap">'


def foot(n, theme_icon):
    return f'<div class="foot"><span>{n} / 5</span>{I(theme_icon, "height:46px")}</div>'


STORIES = {
"01-welcome": f'''<div class="s navy" style="justify-content:center;align-items:center;text-align:center;gap:70px">
  <span class="lbl">Start here</span>
  {W(WARM, "width:820px")}
  <p style="font-stretch:125%;font-weight:500;font-size:36px;letter-spacing:.22em;text-transform:uppercase;color:{MIST}">Home &amp; Kitchen</p>
  <p style="font-size:36px;color:{MIST};margin-top:60px">Tap to get to know us →</p>
  {foot("01", WARM)}</div>''',

"02-who-we-are": f'''<div class="s warm" style="gap:56px">
  <span class="lbl">Who we are</span>
  <h1>Kitchen tools that make everyday cooking easier.</h1>
  <p style="color:#3A4256">COBU designs simple, practical tools for home cooks. Fewer bowls, fewer drips, more time at the table.</p>
  <div style="flex:1;display:grid;place-items:center">{I(NAVY, "width:520px", MUSTARD)}</div>
  {foot("02", NAVY)}</div>''',

"03-why-we-started": f'''<div class="s navy" style="gap:56px">
  <span class="lbl">Why we started</span>
  <h1>Breakfast shouldn’t end with a sticky counter.</h1>
  <div style="display:grid;gap:26px;margin-top:20px">
    {"".join(f'<p style="font-size:44px;color:{MIST};text-decoration:line-through;text-decoration-color:{MUSTARD};text-decoration-thickness:5px">{t}</p>' for t in ("A bowl to mix", "A ladle to pour", "Drips on the pan", "A sink full of dishes"))}
  </div>
  <p style="font-stretch:125%;font-weight:600;font-size:58px;line-height:1.15;color:{MUSTARD};margin-top:40px">So we made one bottle that does it all.</p>
  {foot("03", WARM)}</div>''',

"04-first-product": f'''<div class="s warm" style="gap:40px">
  <span class="lbl">Our first product</span>
  <h1 style="font-size:84px">Pancake Batter Dispenser</h1>
  <div style="flex:1;display:grid;grid-template-columns:330px 1fr;gap:56px;align-items:center;min-height:0">
    <div style="height:860px">{BOTTLE}</div>
    <div style="display:grid;gap:52px">
      {"".join(f'<div style="display:grid;gap:10px"><span style="font-stretch:125%;font-weight:600;font-size:52px;color:{NAVY}">{h}</span><p style="font-size:34px;line-height:1.35;color:#3A4256">{t}</p></div>' for h, t in (("Mix", "Drop in the whisk ball and shake."), ("Pour", "The silicone valve gives clean, even pours."), ("Clean", "The base unscrews so it opens wide.")))}
    </div>
  </div>
  {foot("04", NAVY)}</div>''',

"05-coming-soon": f'''<div class="s navy" style="justify-content:center;align-items:center;text-align:center;gap:64px">
  <span class="lbl">Coming soon</span>
  {I(WARM, "width:500px", MUSTARD)}
  <h1 style="font-size:88px">Launching soon on Amazon.</h1>
  <p style="color:{MIST};max-width:820px">Follow @cobugoods and turn on notifications to be the first to know.</p>
  <span class="pill">🔔 Turn on notifications</span>
  {foot("05", WARM)}</div>''',

# highlight cover: the pot centred where Instagram crops the circle
"00-highlight-cover": f'''<div class="s navy" style="padding:0;display:grid;place-items:center">{I(WARM, "width:560px", MUSTARD)}</div>''',
}

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        for name, body in STORIES.items():
            pg.set_content(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>{body}</body></html>')
            pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            raw = TMP / f"{name}@2x.png"; pg.screenshot(path=str(raw))
            Image.open(raw).convert("RGB").resize((1080, 1920), Image.LANCZOS).save(OUT / f"cobu-start-here-{name}.png", optimize=True)
        b.close()
    for f in sorted(OUT.glob("*.png")):
        print(f.name, Image.open(f).size)
