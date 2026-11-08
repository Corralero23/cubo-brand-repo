"""Exports every logo variation as SVG + high-resolution PNG, in separate folders."""
import pathlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from identity import svg_file, art, NAVY, WARM, MUSTARD

ROOT = pathlib.Path(__file__).resolve().parent.parent / "logos"
COLOURS = {"navy": NAVY, "warm-white": WARM, "black": "#000000", "white": "#FFFFFF"}

jobs = []   # (folder, name, svg, png_width)
for kind, W in (("wordmark", 4000), ("icon", 3000)):
    for cname, c in COLOURS.items():
        s, _ = svg_file(kind, c, pad=0.04)
        jobs.append((kind, f"cobu-{kind}-{cname}", s, W, True))
    for name, fg, bg in (("navy-on-warm-white", NAVY, WARM), ("warm-white-on-navy", WARM, NAVY), ("navy-on-mustard", NAVY, MUSTARD)):
        if kind == "wordmark" and name == "navy-on-mustard":
            continue
        s, _ = svg_file(kind, fg, bg, pad=0.16 if kind == "wordmark" else 0.24, square=(kind == "icon"))
        jobs.append((kind, f"cobu-{kind}-{name}", s, W, False))

T = str(pathlib.Path(__file__).resolve().parent / ".mass.png")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 1000})

    def render(svg, w, path, transparent):
        styled = svg.replace("<svg ", f'<svg style="width:{w}px;height:auto;display:block" ', 1)
        pg.set_viewport_size({"width": w, "height": 200})
        pg.set_content(f"<html><body style='margin:0;background:transparent'>{styled}</body></html>")
        pg.locator("svg").screenshot(path=str(path), omit_background=transparent)

    for folder, name, s, w, transp in jobs:
        d = ROOT / folder; d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.svg").write_text(s)
        render(s, w, d / f"{name}.png", transp)

    # Instagram: optical centre = halfway between box centre and visual mass centre (the lid is light, the pot heavy)
    inner, (x0, y0, x1, y1) = art("icon", "#000")
    probe = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}">{inner}</svg>'
    render(probe, 1000, T, False)
    a = np.asarray(Image.open(T).convert("L")) < 128
    h, w = a.shape
    my = (a * np.arange(h)[:, None]).sum() / a.sum() / h        # 0..1 down the box
    mx = (a * np.arange(w)[None, :]).sum() / a.sum() / w
    oy = y0 + (y1 - y0) * (0.5 + my) / 2; ox = x0 + (x1 - x0) * (0.5 + mx) / 2
    bw, bh = x1 - x0, y1 - y0
    side = max(bw, bh) / 0.60                                    # artwork ~60% of the canvas width
    vb = f"{ox - side/2:.2f} {oy - side/2:.2f} {side:.2f} {side:.2f}"
    ig = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><rect x="{ox-side/2:.2f}" y="{oy-side/2:.2f}" width="{side:.2f}" height="{side:.2f}" fill="{NAVY}"/>'
          + art("icon", WARM)[0] + "</svg>")
    d = ROOT / "instagram"; d.mkdir(exist_ok=True)
    (d / "cobu-instagram-profile.svg").write_text(ig)
    render(ig, 2048, d / "cobu-instagram-profile.png", False)
    print("mass centre (0-1):", round(mx, 3), round(my, 3))
    b.close()

for f in sorted(ROOT.rglob("*.png")):
    im = Image.open(f); print(f.relative_to(ROOT), im.size, im.mode)
