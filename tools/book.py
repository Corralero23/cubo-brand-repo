"""COBU brand book ('The Pot O', Archivo Expanded): web page + print layout for the PDF."""
import pathlib
from identity import art, wordmark, icon, NAVY, WARM, MUSTARD, MIST, INK, O_X0, O_X1, O_Y0, O_Y1, STEM_V

ROOT = pathlib.Path(__file__).resolve().parent.parent / "brand"


def vb(bb, pad=0.0):
    x0, y0, x1, y1 = bb; w, h = x1 - x0, y1 - y0
    return f"{x0 - w*pad:.1f} {y0 - h*pad:.1f} {w*(1+2*pad):.1f} {h*(1+2*pad):.1f}"


def W(fill, cls="wm", lid=None):
    inner, bb = art("wordmark", fill, lid)
    return f'<svg class="{cls}" viewBox="{vb(bb)}" role="img" aria-label="COBU logo">{inner}</svg>'


def I(fill, cls="ic", lid=None):
    inner, bb = art("icon", fill, lid)
    return f'<svg class="{cls}" viewBox="{vb(bb)}" role="img" aria-label="COBU pot icon">{inner}</svg>'


def cmyk(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)); k = 1 - max(r, g, b)
    return " ".join(str(round(v * 100)) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))


def rgb(h):
    return " ".join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))


# ---- construction drawing of the icon ----
_, ibb = art("icon", NAVY)
body, lidp, _ = icon()
cx = (O_X0 + O_X1) / 2
gap_top = O_Y0 - STEM_V * 0.40
construction = f'''<svg class="construct" viewBox="{vb(ibb, 0.26)}" role="img" aria-label="How the pot icon is built">
<path d="{body}" fill="{NAVY}" opacity=".9"/><path d="{lidp}" fill="{MUSTARD}"/>
<g fill="none" stroke="{MUSTARD}" stroke-width="5" stroke-dasharray="18 14">
<rect x="{O_X0}" y="{O_Y0}" width="{O_X1-O_X0}" height="{O_Y1-O_Y0}"/>
<line x1="{cx}" y1="{ibb[1]-80}" x2="{cx}" y2="{O_Y1+80}"/></g>
<g stroke="{INK}" stroke-width="4"><line x1="{O_X1+150}" y1="{O_Y0}" x2="{O_X1+150}" y2="{gap_top}"/><line x1="{O_X1+120}" y1="{O_Y0}" x2="{O_X1+180}" y2="{O_Y0}"/><line x1="{O_X1+120}" y1="{gap_top}" x2="{O_X1+180}" y2="{gap_top}"/></g>
<g font-family="Archivo, sans-serif" font-size="84" fill="{INK}">
<text x="{O_X1+120}" y="{(O_Y0+gap_top)/2-70}" text-anchor="end">gap</text>
<text x="{O_X0}" y="{O_Y1+120}">the O from the wordmark</text>
<text x="{cx+60}" y="{ibb[1]-40}">lid</text></g></svg>'''

# ---- clear space drawing ----
wi, wbb = art("wordmark", NAVY)
lid_h = (O_Y0 - STEM_V * 0.40) - wbb[1]          # height of lid + knob = x
x0, y0, x1, y1 = wbb
clear = f'''<svg class="clear" viewBox="{x0-lid_h*1.6:.1f} {y0-lid_h*1.6:.1f} {x1-x0+lid_h*3.2:.1f} {y1-y0+lid_h*3.2:.1f}" role="img" aria-label="Clear space around the logo">
<rect x="{x0-lid_h:.1f}" y="{y0-lid_h:.1f}" width="{x1-x0+2*lid_h:.1f}" height="{y1-y0+2*lid_h:.1f}" fill="none" stroke="{MUSTARD}" stroke-width="10" stroke-dasharray="30 22"/>
{wi}
<g font-family="Archivo, sans-serif" font-size="110" fill="{MUSTARD}" text-anchor="middle">
<text x="{x0-lid_h/2:.1f}" y="{(y0+y1)/2+38:.1f}">x</text><text x="{x1+lid_h/2:.1f}" y="{(y0+y1)/2+38:.1f}">x</text>
<text x="{(x0+x1)/2:.1f}" y="{y1+lid_h/2+38:.1f}">x</text></g></svg>'''

misuse = [
    ("Don't stretch or squash it", f'<div class="mz" style="transform:scaleX(1.4)">{W(NAVY)}</div>'),
    ("Don't rotate it", f'<div class="mz" style="transform:rotate(-12deg)">{W(NAVY)}</div>'),
    ("Don't use colours outside the palette", f'<div class="mz">{W("#2EA36B")}</div>'),
    ("Don't add shadows or effects", f'<div class="mz" style="filter:drop-shadow(6px 8px 4px rgba(0,0,0,.45))">{W(NAVY)}</div>'),
    ("Don't remove or move the lid", f'<div class="mz nolid">{W(NAVY, lid="transparent")}</div>'),
    ("Don't place it on busy backgrounds", f'<div class="mz busy">{W(WARM)}</div>'),
]
misuse_html = "".join(f'<figure class="mis"><div class="mbox">{a}</div><figcaption><b aria-hidden="true">×</b>{c}</figcaption></figure>' for c, a in misuse)

palette = [
    ("Navy", NAVY, "Primary", "Logo, packaging, headlines, buttons.", WARM),
    ("Warm White", WARM, "Primary", "Backgrounds, logo on navy, box interiors.", INK),
    ("Mustard", MUSTARD, "Accent", "Small doses: badges, prices, stickers, ‘New’.", NAVY),
    ("Mist", MIST, "Support", "Panels, table rows, quiet backgrounds.", NAVY),
    ("Ink", INK, "Text", "Body text and fine print.", WARM),
]
swatches = "".join(f'''<div class="sw"><div class="chip" style="background:{h};color:{t}"><span>{n}</span><em>{r}</em></div>
<dl><dt>HEX</dt><dd>{h}</dd><dt>RGB</dt><dd>{rgb(h)}</dd><dt>CMYK*</dt><dd>{cmyk(h)}</dd></dl><p>{u}</p></div>''' for n, h, r, u, t in palette)

CSS = f'''
:root {{
  /* Layout: a stack of full-width plates, one idea each; every plate prints as one A4 landscape page */
  --navy: {NAVY}; --warm: {WARM}; --mustard: {MUSTARD}; --mist: {MIST}; --ink: {INK};
  --paper: #FBF9F4; --line: #DCD6CA; --muted: #5C6474;
  --display: "Archivo", "Helvetica Neue", Arial, sans-serif;
  --body: "Archivo", "Helvetica Neue", Arial, sans-serif;
  color-scheme: light;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--paper); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; margin: 0; }}
.plate {{ padding-block: clamp(48px, 7vw, 96px); padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); border-top: 1px solid var(--line); }}
.wrap {{ max-width: 1120px; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 270px) minmax(0, 1fr); gap: clamp(24px, 4vw, 64px); }}
.head {{ display: flex; flex-direction: column; gap: 12px; }}
.no {{ font-family: var(--display); font-stretch: 125%; font-weight: 500; font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: var(--mustard); }}
h1, h2, h3 {{ font-family: var(--display); font-stretch: 125%; font-weight: 600; margin: 0; text-wrap: balance; letter-spacing: -.005em; }}
h2 {{ font-size: clamp(26px, 3vw, 36px); line-height: 1.08; color: var(--navy); }}
h3 {{ font-size: 16px; color: var(--ink); }}
p {{ margin: 0; max-width: 62ch; }}
.lede {{ color: var(--muted); }}
.body {{ display: flex; flex-direction: column; gap: 28px; min-width: 0; }}
svg {{ display: block; max-width: 100%; }}
.cap {{ font-family: var(--display); font-stretch: 125%; font-weight: 500; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }}

.cover {{ background: var(--navy); color: var(--warm); border-top: 0; }}
.cover .wrap {{ grid-template-columns: 1fr; gap: 56px; padding-block: 24px; }}
.cover .wm {{ width: min(680px, 100%); }}
.cover h1 {{ font-size: clamp(36px, 5vw, 64px); line-height: 1; color: var(--warm); font-weight: 500; }}
.cover .meta {{ display: flex; flex-wrap: wrap; gap: 12px 40px; font-family: var(--display); font-stretch: 125%; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--mist); }}

.mark {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 28px; align-items: center; }}
.construct {{ width: 100%; background: var(--warm); border-radius: 4px; }}
.points {{ display: grid; gap: 16px; }}
.points div {{ display: grid; gap: 4px; padding-left: 16px; border-left: 2px solid var(--line); }}

.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; }}
.tile {{ display: flex; flex-direction: column; gap: 10px; margin: 0; }}
.tile .art {{ aspect-ratio: 16 / 10; display: grid; place-items: center; padding: 12%; border: 1px solid var(--line); border-radius: 4px; }}
.tile .art .wm {{ width: 100%; }}
.tile .art .ic {{ width: 34%; height: auto; }}
.tile figcaption {{ display: grid; gap: 2px; font-size: 14px; color: var(--muted); }}
.tile figcaption b {{ color: var(--ink); font-weight: 600; font-size: 15px; }}

.two {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 32px; align-items: start; }}
.clear {{ width: 100%; background: var(--warm); border-radius: 4px; }}
.min {{ display: flex; flex-wrap: wrap; align-items: flex-end; gap: 28px; padding: 24px; background: var(--warm); border-radius: 4px; }}
.min figure {{ margin: 0; display: grid; gap: 8px; justify-items: start; }}

.mgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }}
.mis {{ margin: 0; display: grid; gap: 8px; }}
.mbox {{ aspect-ratio: 16 / 10; display: grid; place-items: center; background: var(--warm); border-radius: 4px; overflow: hidden; }}
.mz {{ width: 66%; }} .mz svg {{ width: 100%; }}
.mbox:has(.busy) {{ background: repeating-linear-gradient(135deg, #7A8F5E 0 14px, #C9A15B 14px 28px, #4F6E8C 28px 42px); }}
.mis figcaption {{ font-size: 14px; display: flex; gap: 8px; align-items: baseline; }}
.mis figcaption b {{ color: #B4432A; font-size: 18px; line-height: 1; }}

.swatches {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; }}
.sw {{ display: grid; gap: 10px; align-content: start; }}
.chip {{ aspect-ratio: 4 / 3; border-radius: 4px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: inset 0 0 0 1px rgba(20,26,40,.08); }}
.chip span {{ font-family: var(--display); font-stretch: 125%; font-size: 17px; font-weight: 600; }}
.chip em {{ font-style: normal; font-family: var(--display); font-stretch: 125%; font-size: 10px; letter-spacing: .14em; text-transform: uppercase; opacity: .85; }}
.sw dl {{ display: grid; grid-template-columns: auto 1fr; gap: 2px 10px; margin: 0; font-size: 12.5px; font-variant-numeric: tabular-nums; }}
.sw dt {{ color: var(--muted); }} .sw dd {{ margin: 0; }}
.sw p {{ font-size: 13.5px; color: var(--muted); }}
.ratio {{ display: flex; height: 44px; border-radius: 4px; overflow: hidden; }}
.ratio div {{ display: flex; align-items: center; padding-left: 12px; font-size: 12px; letter-spacing: .04em; }}
.note {{ font-size: 13px; color: var(--muted); }}

.spec {{ display: grid; border-top: 1px solid var(--line); }}
.row {{ display: grid; grid-template-columns: minmax(0, 200px) minmax(0, 1fr); gap: 20px; padding-block: 18px; border-bottom: 1px solid var(--line); align-items: baseline; }}
.row .cap {{ line-height: 1.7; }}
.t1 {{ font-family: var(--display); font-stretch: 125%; font-weight: 600; font-size: clamp(28px, 3.4vw, 40px); line-height: 1.08; color: var(--navy); }}
.t2 {{ font-family: var(--display); font-stretch: 125%; font-weight: 600; font-size: 22px; }}
.t3 {{ font-family: var(--body); font-size: 16px; line-height: 1.55; }}
.t4 {{ font-family: var(--display); font-stretch: 125%; font-weight: 500; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; }}

.apps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 20px; }}
.app {{ margin: 0; display: grid; gap: 10px; align-content: start; }}
.app figcaption {{ font-size: 14px; color: var(--muted); }} .app figcaption b {{ color: var(--ink); font-weight: 600; display: block; }}
.box {{ aspect-ratio: 4 / 5; background: var(--navy); color: var(--warm); border-radius: 3px; padding: 9%; display: flex; flex-direction: column; justify-content: space-between; position: relative; box-shadow: 14px 14px 0 -2px #121A2C; }}
.box .wm {{ width: 72%; }}
.box h4 {{ font-family: var(--display); font-stretch: 125%; font-weight: 500; font-size: clamp(17px, 1.8vw, 21px); line-height: 1.2; margin: 0; }}
.box small {{ font-family: var(--display); font-stretch: 125%; font-size: 10px; letter-spacing: .16em; text-transform: uppercase; color: var(--mist); }}
.badge {{ display: inline-block; margin-bottom: 10px; background: var(--mustard); color: var(--navy); font-family: var(--display); font-stretch: 125%; font-weight: 600; font-size: 10px; letter-spacing: .14em; text-transform: uppercase; padding: 6px 10px; border-radius: 99px; }}
.ig {{ aspect-ratio: 4 / 5; background: #fff; border: 1px solid var(--line); border-radius: 4px; padding: 10%; display: flex; flex-direction: column; gap: 16px; align-items: center; justify-content: center; text-align: center; font-family: system-ui, sans-serif; }}
.ig .av {{ width: 60%; aspect-ratio: 1; border-radius: 50%; background: var(--navy); display: grid; place-items: center; }}
.ig .av svg {{ width: 62%; }}
.ig b {{ font-weight: 600; font-size: 16px; color: #111; }} .ig span {{ font-size: 13px; color: #555; }}
.lidmock {{ aspect-ratio: 4 / 5; background: var(--mist); border-radius: 4px; display: grid; place-items: center; }}
.lidmock div {{ width: 76%; aspect-ratio: 1; border-radius: 50%; background: radial-gradient(circle at 38% 32%, #5A6B86 0%, #2C3A55 55%, #1A2438 100%); display: grid; place-items: center; box-shadow: 0 10px 22px rgba(20,26,40,.35); }}
.lidmock svg {{ width: 46%; filter: drop-shadow(0 -1px 0 rgba(255,255,255,.25)) drop-shadow(0 2px 1px rgba(0,0,0,.45)); }}
.seal {{ aspect-ratio: 4 / 5; background: #D8C9B0; border-radius: 4px; display: grid; place-items: center; }}
.seal div {{ width: 62%; aspect-ratio: 1; border-radius: 50%; background: var(--mustard); display: grid; place-items: center; box-shadow: 0 2px 0 rgba(0,0,0,.1); }}
.seal svg {{ width: 66%; }}

.name {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }}
.name div {{ background: var(--warm); border-radius: 4px; padding: 20px; display: grid; gap: 8px; }}
.foot {{ max-width: 1120px; margin: 0 auto; padding-block: 28px 40px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; font-family: var(--display); font-stretch: 125%; font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }}
@media (max-width: 760px) {{ .wrap {{ grid-template-columns: minmax(0, 1fr); }} .row {{ grid-template-columns: minmax(0, 1fr); gap: 6px; }} }}
'''

PRINT = '''
@page { size: 297mm 210mm; margin: 0; }
.plate { width: 297mm; height: 210mm; overflow: hidden; padding: 15mm 16mm !important; break-after: page; border-top: 0; display: flex; align-items: center; }
.plate > .wrap { width: 100%; max-width: none; grid-template-columns: 64mm minmax(0, 1fr); gap: 12mm; }
.cover > .wrap { grid-template-columns: 1fr; }
.foot { display: none; }
h2 { font-size: 28px; }
.tile .art, .mbox { aspect-ratio: 16 / 9; }
.tiles { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.tiles.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.apps { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.swatches { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }
.mgrid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.chip { aspect-ratio: 4 / 2.6; }
.mark { grid-template-columns: 1.2fr 1fr; }
.two { grid-template-columns: 1.4fr 1fr; }
.row { padding-block: 11px; }
.body { gap: 18px; }
'''


def section(no, title, lede, body, cls=""):
    return (f'<section class="plate {cls}"><div class="wrap"><div class="head"><span class="no">{no}</span><h2>{title}</h2>'
            f'<p class="lede">{lede}</p></div><div class="body">{body}</div></div></section>')


def build():
    s = [f'''<section class="plate cover"><div class="wrap">{W(WARM)}<h1>Brand Book</h1>
<div class="meta"><span>Home &amp; Kitchen</span><span>Version 1.0</span><span>October 2026</span></div></div></section>''']

    s.append(section("01 · The idea", "The O lifts its lid",
        "COBU is set in a wide, sturdy typeface. Its O is broad enough to be a Dutch oven, so we gave it a lid. Read the name and you already know what we make.",
        f'''<div class="mark">{construction}<div class="points">
<div><h3>The pot is the letter</h3><p>The body is the exact O from the wordmark, so the icon and the name always match.</p></div>
<div><h3>A domed lid</h3><p>Its thickness matches the letters’ strokes, and it floats a short gap above the pot as if steam had just lifted it.</p></div>
<div><h3>Handles on the icon</h3><p>Used on its own, the pot gets two side handles so it reads as cookware at any size.</p></div></div></div>'''))

    s.append(section("02 · Logo set", "A wordmark and an icon",
        "Use the wordmark wherever there is room. Use the icon when space is square or small, or when the name is already nearby.",
        f'''<div class="tiles">
<figure class="tile"><div class="art" style="background:var(--warm)">{W(NAVY)}</div><figcaption><b>Wordmark (primary)</b>Packaging, website, Amazon brand store, documents.</figcaption></figure>
<figure class="tile"><div class="art" style="background:var(--warm)">{I(NAVY)}</div><figcaption><b>Icon</b>Social avatars, favicons, product stamping, stickers, tags.</figcaption></figure></div>'''))

    s.append(section("03 · Colour versions", "Navy on warm white comes first",
        "Choose the version by the background. On photographs, use whichever of navy or warm white gives more contrast.",
        f'''<div class="tiles four">
<figure class="tile"><div class="art" style="background:var(--warm)">{W(NAVY)}</div><figcaption><b>Navy on warm white</b>The primary version.</figcaption></figure>
<figure class="tile"><div class="art" style="background:var(--navy);border-color:var(--navy)">{W(WARM)}</div><figcaption><b>Warm white on navy</b>Boxes, social media, merchandise.</figcaption></figure>
<figure class="tile"><div class="art" style="background:var(--mustard);border-color:var(--mustard)">{I(NAVY)}</div><figcaption><b>Navy on mustard</b>Icon only: stickers, promotions.</figcaption></figure>
<figure class="tile"><div class="art" style="background:#fff">{W("#000")}</div><figcaption><b>Single colour</b>Embossing, laser etching, one-colour print.</figcaption></figure></div>'''))

    s.append(section("04 · Space and size", "Give it room",
        "Keep a margin of at least <i>x</i>, the height of the lid and knob, on every side. Below the minimum sizes the gap under the lid starts to close.",
        f'''<div class="two">{clear}<div class="min">
<figure><svg viewBox="{vb(wbb)}" style="width:140px">{wi}</svg><span class="cap">Wordmark · min 30 mm / 140 px</span></figure>
<figure>{I(NAVY).replace('class="ic"', 'class="ic" style="width:36px"')}<span class="cap">Icon · min 8 mm / 32 px</span></figure></div></div>'''))

    s.append(section("05 · Misuse", "Keep it as drawn",
        "The logo only works exactly as supplied. Always use the master files; never retype COBU in a font or redraw the pot.",
        f'<div class="mgrid">{misuse_html}</div>'))

    s.append(section("06 · Colour", "Navy, warm white and a spoon of mustard",
        "Navy and warm white carry the brand. Mustard is the accent: use it sparingly so it keeps its punch.",
        f'''<div class="swatches">{swatches}</div>
<div class="ratio" role="img" aria-label="Colour proportions: 60 percent warm white, 30 percent navy, 7 percent mist, 3 percent mustard">
<div style="flex:60;background:var(--warm);color:var(--ink)">Warm White 60%</div><div style="flex:30;background:var(--navy);color:var(--warm)">Navy 30%</div><div style="flex:7;background:var(--mist);color:var(--navy)">7%</div><div style="flex:3;background:var(--mustard)"></div></div>
<p class="note">*CMYK values are a starting point. Ask your printer for a proof, or match against a Pantone swatch book before a production run.</p>'''))

    s.append(section("07 · Typography", "Archivo, wide and sturdy",
        "Archivo Expanded, the face behind the logo, sets headlines and labels. Regular-width Archivo keeps longer text easy to read. Both are free on Google Fonts.",
        '''<div class="spec">
<div class="row"><span class="cap">Headline<br>Archivo Expanded SemiBold</span><span class="t1">Made for the way you cook</span></div>
<div class="row"><span class="cap">Subhead<br>Archivo Expanded SemiBold</span><span class="t2">Mix, pour and clean in one bottle</span></div>
<div class="row"><span class="cap">Body<br>Archivo Regular · 16/25</span><span class="t3">Fill the bottle, drop in the whisk ball and shake. The silicone valve gives you clean, even pours for pancakes, crêpes and muffins.</span></div>
<div class="row"><span class="cap">Label<br>Archivo Expanded Medium · caps</span><span class="t4">Dishwasher safe · Made for everyday cooking</span></div></div>'''))

    s.append(section("08 · In use", "Out in the world",
        "Four everyday uses. The rules stay the same: generous space, navy and warm white, a small touch of mustard.",
        f'''<div class="apps">
<figure class="app"><div class="box">{W(WARM)}<div><span class="badge">New</span><h4>Pancake Batter Dispenser</h4><small>Home &amp; Kitchen</small></div></div><figcaption><b>Packaging</b>Warm white wordmark on a navy box; mustard only for the badge.</figcaption></figure>
<figure class="app"><div class="ig"><div class="av">{I(WARM)}</div><b>cobu</b><span>Home &amp; Kitchen</span></div><figcaption><b>Social avatar</b>Warm white pot on navy, centred in the circle.</figcaption></figure>
<figure class="app"><div class="lidmock"><div>{I("#2A3954")}</div></div><figcaption><b>Product marking</b>Single-colour icon cast or embossed on lids and handles.</figcaption></figure>
<figure class="app"><div class="seal"><div>{I(NAVY)}</div></div><figcaption><b>Seal sticker</b>Mustard sticker for mailers and gift wrap.</figcaption></figure></div>'''))

    s.append(section("09 · The name", "How to write COBU",
        "The name is always written in capitals, in text and in the logo.",
        '''<div class="name">
<div><span class="cap" style="color:var(--navy)">Write</span><p class="t2">COBU</p><p>“The new COBU dispenser is on Amazon.”</p></div>
<div><span class="cap" style="color:#B4432A">Avoid</span><p class="t2">Cobu · cobu · C.O.B.U.</p><p>In running text these look like typos or a different brand.</p></div></div>'''))
    return "\n".join(s)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700&display=swap">')

if __name__ == "__main__":
    body = build()
    foot = '<footer class="foot"><span>COBU Brand Book</span><span>Version 1.0 · October 2026</span></footer>'
    (ROOT / "cobu-brand-book.html").write_text(
        f'<title>COBU Brand Book</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n<style>{CSS}</style>\n<main>{body}</main>\n{foot}\n')
    (pathlib.Path(__file__).resolve().parent / "print.html").write_text(
        f'<!doctype html><html><head><meta charset="utf-8"><title>COBU Brand Book</title>{FONTS}<style>{CSS}{PRINT}</style></head><body><main>{body}</main></body></html>')
    print("ok")
