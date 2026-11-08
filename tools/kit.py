"""Shared helpers: outline text from font files, simple geometry."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = str(__import__("pathlib").Path(__file__).resolve().parent / "fonts") + "/"
_cache = {}


def font(name):
    if name not in _cache:
        _cache[name] = TTFont(FONTS + name + ".ttf")
    return _cache[name]


def metrics(name, size):
    f = font(name); s = size / f["head"].unitsPerEm; os2 = f["OS/2"]
    return {"cap": os2.sCapHeight * s, "x": os2.sxHeight * s}


def glyph(name, ch, size, x=0.0, y=0.0, rot=0.0):
    """Outline of one character; (x, y) is the baseline origin. Returns (d, advance)."""
    f = font(name); gs = f.getGlyphSet(); g = f.getBestCmap()[ord(ch)]
    s = size / f["head"].unitsPerEm
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pen = SVGPathPen(gs)
    # scale, flip y, rotate, translate
    gs[g].draw(TransformPen(pen, (s * c, s * si, s * si, -s * c, x, y)))
    return pen.getCommands(), f["hmtx"][g][0] * s


def text(name, string, size, tracking=0.0, x=0.0, y=0.0, kern=None):
    """Outline a string on a baseline. tracking in em. kern: {pair: em}. Returns (d, width)."""
    d, cx = [], x
    for i, ch in enumerate(string):
        if ch == " ":
            cx += size * 0.28 + size * tracking
            continue
        gd, adv = glyph(name, ch, size, cx, y)
        d.append(gd)
        cx += adv + size * tracking
        if kern and i + 1 < len(string):
            cx += size * kern.get(string[i:i + 2], 0)
    return "".join(d), cx - x - size * tracking


def width(name, string, size, tracking=0.0, kern=None):
    return text(name, string, size, tracking, kern=kern)[1]


def text_on_circle(name, string, size, cx, cy, r, centre_deg=-90, tracking=0.0):
    """Characters set clockwise along a circle, centred on centre_deg (screen angles)."""
    advs = []
    for ch in string:
        advs.append(size * 0.28 if ch == " " else glyph(name, ch, size)[1])
    total = sum(advs) + size * tracking * (len(string) - 1)
    ang = math.radians(centre_deg) - (total / r) / 2
    d = []
    for ch, adv in zip(string, advs):
        mid = ang + (adv / 2) / r
        if ch != " ":
            # place glyph so its centre sits on the circle, upright = pointing outward
            px, py = cx + r * math.cos(mid), cy + r * math.sin(mid)
            rot = math.degrees(mid) + 90
            ox, oy = -adv / 2, 0
            c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            gx = px + ox * c - oy * s
            gy = py + ox * s + oy * c
            d.append(glyph(name, ch, size, gx, gy, rot)[0])
        ang += (adv + size * tracking) / r
    return "".join(d)


def P(x, y):
    return f"{x:.2f} {y:.2f}"


def svg(w, h, inner, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{inner}</svg>'
