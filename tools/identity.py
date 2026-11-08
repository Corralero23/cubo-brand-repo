"""COBU 'Pot O' identity set in Archivo Expanded SemiBold. All artwork is outlined.
Units: font size 1000, baseline at y=0 (negative y is up)."""
from kit import text, glyph, P

NAVY, WARM, MUSTARD, MIST, INK = "#1E2A44", "#F6F1E7", "#D8A23E", "#C9D3DF", "#141A28"

SIZE, TRACK = 1000, 0.10
# measured from the Archivo Expanded SemiBold O at size 1000
O_X0, O_X1, O_Y0, O_Y1 = 67, 951, -699, 12        # O bounds in screen coords (y up is negative)
STEM_H, STEM_V = 157, 134                         # side stroke, top/bottom stroke


def lid(cx, o_top, o_w):
    """Domed lid with knob, sitting just above the O. Returns (path, top_y)."""
    gap = STEM_V * 0.40
    lb = o_top - gap                  # lid base line
    lw = o_w * 0.94; lh = STEM_V * 1.05
    rr = (lw * lw / 4 + lh * lh) / (2 * lh)
    dome = f"M{P(cx-lw/2, lb)}A{rr:.2f} {rr:.2f} 0 0 1 {P(cx+lw/2, lb)}Z"
    kw, kh = o_w * 0.15, STEM_V * 0.62
    kt = lb - lh - kh
    knob = (f"M{P(cx-kw/2, lb-lh+3)}V{kt+kw*0.22:.2f}Q{P(cx-kw/2, kt)} {P(cx-kw/4, kt)}H{cx+kw/4:.2f}"
            f"Q{P(cx+kw/2, kt)} {P(cx+kw/2, kt+kw*0.22)}V{lb-lh+3:.2f}Z")
    return dome + knob, kt


def wordmark():
    """Returns (letters_path, lid_path, bbox) with bbox = (x0, y0, x1, y1)."""
    d = []; x = 0.0
    for ch in "COBU":
        gd, adv = glyph("archivo", ch, SIZE, x, 0)
        if ch == "O":
            o_cx = x + (O_X0 + O_X1) / 2
            o_x = x
        d.append(gd)
        x += adv + SIZE * TRACK
    width = x - SIZE * TRACK
    lp, top = lid(o_cx, O_Y0, O_X1 - O_X0)
    return "".join(d), lp, (67, top, width - 91 + 853 - 853, O_Y1)


def icon():
    """Pot: the Archivo O as the body, side handles, domed lid. Returns (body_path, lid_path, bbox)."""
    gd, _ = glyph("archivo", "O", SIZE, 0, 0)
    cx = (O_X0 + O_X1) / 2; cy = (O_Y0 + O_Y1) / 2
    rx = (O_X1 - O_X0) / 2; ry = (O_Y1 - O_Y0) / 2
    hy = cy - ry * 0.40; ht = STEM_V * 0.80; hw = rx * 0.22
    handles = ""
    for sgn in (-1, 1):
        inner = cx + sgn * rx * 0.86; outer = cx + sgn * (rx + hw)
        l, r = min(inner, outer), max(inner, outer)
        handles += f"M{P(l, hy-ht/2)}H{r:.2f}V{hy+ht/2:.2f}H{l:.2f}Z"
    lp, top = lid(cx, O_Y0, O_X1 - O_X0)
    return gd + handles, lp, (cx - rx - hw, top, cx + rx + hw, O_Y1)


def art(kind, fill, lid_fill=None):
    """SVG inner markup for 'wordmark' or 'icon'."""
    body, lp, bb = wordmark() if kind == "wordmark" else icon()
    return f'<path d="{body}" fill="{fill}"/><path d="{lp}" fill="{lid_fill or fill}"/>', bb


def svg_file(kind, fill, bg=None, pad=0.0, square=False, lid_fill=None):
    inner, (x0, y0, x1, y1) = art(kind, fill, lid_fill)
    w, h = x1 - x0, y1 - y0
    px, py = w * pad, h * pad if not square else w * pad
    vx, vy, vw, vh = x0 - px, y0 - py, w + 2 * px, h + 2 * py
    if square:
        side = max(vw, vh); vx -= (side - vw) / 2; vy -= (side - vh) / 2; vw = vh = side
    b = f'<rect x="{vx:.2f}" y="{vy:.2f}" width="{vw:.2f}" height="{vh:.2f}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">{b}{inner}</svg>', vw / vh
