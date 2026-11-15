"""COBU launch post for Instagram (1080x1350): the real product cut out of the owner's photos, set in the
brand book system. Usage: python3 tools/launch_post.py <bottle.png> <whisk.png> <out-dir>
Cutouts were made with rembg (isnet-general-use) from the owner's photos; see product/launch/."""
import base64, pathlib, sys
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
bottle_p, whisk_p, out = map(pathlib.Path, sys.argv[1:4]); out.mkdir(parents=True, exist_ok=True)


def soften(p, lift=1.0):
    """Smooth the cutout outline (blur the mask, then re-sharpen it) and lift the exposure slightly."""
    import numpy as np
    from PIL import ImageEnhance
    im = Image.open(p).convert("RGBA")
    a = np.asarray(im.getchannel("A").filter(ImageFilter.GaussianBlur(2.2)), dtype=np.float32) / 255
    a = np.clip((a - 0.5) * 3.2 + 0.5, 0, 1)
    rgb = im.convert("RGB")
    if lift != 1.0:
        rgb = ImageEnhance.Brightness(rgb).enhance(lift)
    out = rgb.convert("RGBA"); out.putalpha(Image.fromarray((a * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6)))
    return out


def b64(p):
    return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()


tmp = out / "_cut"; tmp.mkdir(exist_ok=True)
soften(bottle_p, 1.08).save(tmp / "bottle.png"); soften(whisk_p).save(tmp / "whisk.png")
bottle_p, whisk_p = tmp / "bottle.png", tmp / "whisk.png"
logo = (ROOT / "logos" / "wordmark" / "cobu-wordmark-navy.svg").read_text()
logo = logo.replace("<svg ", '<svg style="width:250px;height:auto;display:block" ', 1)

FEATURES = [("Mix", "Shake it with the whisk ball."),
            ("Pour", "Even pancakes, no drips."),
            ("Clean", "The base unscrews to open wide.")]
feats = "".join(f'<div class="f"><span class="k">{k}</span><span class="t">{t}</span></div>' for k, t in FEATURES)

HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700&display=swap">
<style>
:root {{ --navy:#1E2A44; --warm:#F6F1E7; --mustard:#D8A23E; --mist:#C9D3DF; --ink:#141A28; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:var(--warm); font-family:'Archivo',sans-serif; color:var(--ink); position:relative; overflow:hidden; }}
.logo {{ position:absolute; top:64px; left:80px; }}
.badge {{ position:absolute; top:62px; right:80px; background:var(--mustard); color:var(--navy); font-stretch:125%; font-weight:600;
          font-size:20px; letter-spacing:.14em; text-transform:uppercase; padding:14px 22px; border-radius:6px; }}
h1 {{ position:absolute; top:168px; left:80px; right:80px; font-stretch:125%; font-weight:600; font-size:76px; line-height:1.02;
      color:var(--navy); letter-spacing:-.01em; }}
.sub {{ position:absolute; top:348px; left:80px; font-size:28px; color:#3A4256; }}
.stage {{ position:absolute; left:0; right:0; top:410px; height:760px; }}
.bottle {{ position:absolute; left:120px; bottom:30px; height:720px; filter:drop-shadow(0 18px 18px rgba(30,42,68,.16)); }}
.whisk {{ position:absolute; left:440px; bottom:34px; width:150px; filter:drop-shadow(0 10px 10px rgba(30,42,68,.14)); }}
.floor {{ position:absolute; left:80px; right:80px; bottom:30px; height:2px; background:rgba(30,42,68,.12); }}
.feats {{ position:absolute; left:610px; right:60px; top:120px; display:grid; gap:44px; }}
.f {{ display:grid; gap:6px; padding-left:22px; border-left:4px solid var(--navy); }}
.k {{ font-stretch:125%; font-weight:600; font-size:40px; color:var(--navy); }}
.t {{ font-size:26px; max-width:390px; line-height:1.3; color:#3A4256; }}
.band {{ position:absolute; left:0; right:0; bottom:0; height:180px; background:var(--navy); color:var(--warm);
         display:flex; align-items:center; justify-content:space-between; padding:0 80px; }}
.band .cta {{ font-stretch:125%; font-weight:600; font-size:42px; line-height:1.1; }}
.band .cta b {{ color:var(--mustard); font-weight:600; }}
.band .h {{ font-size:24px; color:var(--mist); text-align:right; line-height:1.4; }}
</style></head><body>
<div class="logo">{logo}</div>
<div class="badge">New product</div>
<h1>Pancakes,<br>without the mess.</h1>
<p class="sub">The COBU Pancake Batter Dispenser</p>
<div class="stage">
  <div class="floor"></div>
  <img class="bottle" src="{b64(bottle_p)}">
  <img class="whisk" src="{b64(whisk_p)}">
  <div class="feats">{feats}</div>
</div>
<div class="band"><div class="cta">Coming soon<br>on <b>Amazon</b></div><div class="h">Follow<br>@cobugoods</div></div>
</body></html>"""

(out / "launch-post.html").write_text(HTML)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
    pg.set_content(HTML); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(out / "launch-post@2x.png"))
    b.close()
big = Image.open(out / "launch-post@2x.png").convert("RGB")
big.resize((1080, 1350), Image.LANCZOS).save(out / "cobu-launch-post-1080x1350.jpg", quality=95, subsampling=0, optimize=True)
print("ok", big.size)
