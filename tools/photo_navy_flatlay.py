"""Usage: python3 tools/photo_navy_flatlay.py <photo.jpg> <output-dir>  (needs opencv-python-headless, numpy)
The cloth corners and part boxes are measured for product/cobu-real-parts-original.jpg; adjust them for a new photo.
COBU real product photo: navy cloth on a warm-white studio surface.
- Green cloth -> navy #1E2A44 (Lab, smoothed chroma; specular highlights in the clear bottle kept).
- Countertop replaced with a clean warm-white surface + soft shadow under the cloth.
- Lint removed from the cloth only (product parts are protected).
- Gentle studio light and white balance on the white parts."""
import sys
import cv2
import numpy as np

SRC, OUTDIR = sys.argv[1], sys.argv[2]
img = cv2.imread(SRC)
H, W = img.shape[:2]

# protected product areas (x0, y0, x1, y1) in source pixels
PARTS = [(380, 540, 615, 740), (555, 745, 765, 905), (185, 985, 625, 1385), (865, 585, 1325, 1545)]

# ---------- recolour ----------
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[..., 0] * 100 / 255; A = lab[..., 1] - 128; B = lab[..., 2] - 128
As, Bs = cv2.GaussianBlur(A, (0, 0), 4), cv2.GaussianBlur(B, (0, 0), 4)
ang = np.degrees(np.arctan2(Bs, As)); C = np.hypot(As, Bs)
w = np.clip((ang - 82) / 10, 0, 1) * np.clip((165 - ang) / 10, 0, 1) * np.clip((C - 1.5) / 3, 0, 1)
w *= np.clip((82 - L) / 14, 0, 1)                   # leave bright reflections on the plastic alone
w = cv2.GaussianBlur(w, (0, 0), 3)
navy = cv2.cvtColor(np.uint8([[[0x44, 0x2A, 0x1E]]]), cv2.COLOR_BGR2LAB)[0, 0].astype(np.float32)
nA, nB = navy[1] - 128, navy[2] - 128; nC = np.hypot(nA, nB); dA, dB = nA / nC, nB / nC
newC = np.maximum(C * 0.55, 6)
L2 = L * (1 - w) + (L * 0.64) * w
A2 = A * (1 - w) + dA * newC * w
B2 = B * (1 - w) + dB * newC * w
rec = cv2.cvtColor(np.dstack([L2 * 2.55, A2 + 128, B2 + 128]).clip(0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

# ---------- cloth outline: everything that is NOT countertop ----------
# countertop = light beige connected to the photo border
counter_like = ((L > 38) & (ang > 15) & (ang < 85) & (C > 5)).astype(np.uint8)
counter_like = cv2.morphologyEx(counter_like, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
ff = counter_like.copy() * 255
seed_mask = np.zeros((H + 2, W + 2), np.uint8)
for sx, sy in [(5, 5), (W - 6, 5), (5, H - 6), (W - 6, H - 6), (W // 2, 5), (W // 2, H - 6)]:
    if ff[sy, sx] == 255:
        cv2.floodFill(ff, seed_mask, (sx, sy), 128)
counter = (ff == 128).astype(np.uint8)
cloth = 1 - counter
n, lbl, st, _ = cv2.connectedComponentsWithStats(cloth)
big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
cloth = (lbl == big).astype(np.uint8)
cloth = cv2.morphologyEx(cloth, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
cloth = cv2.morphologyEx(cloth, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
cloth = cv2.erode(cloth, np.ones((5, 5), np.uint8))          # trim the beige fringe at the hem
# cloth corners measured on the original photo (it was shot at a slight angle, so the top is narrower)
corners = np.array([[300, 546], [1271, 571], [1427, 1566], [92, 1551]], np.float64)
cen = corners.mean(0)
corners = corners + (cen - corners) / np.linalg.norm(cen - corners, axis=1)[:, None] * 7   # 7 px inside the hem
quad = corners.astype(np.int32).reshape(-1, 1, 2)
print("cloth corners", quad.reshape(-1, 2).tolist())
cloth = np.zeros((H, W), np.uint8); cv2.fillPoly(cloth, [quad], 1)

# ---------- whisk ball: steel wires back to neutral silver at their original brightness ----------
wx0, wy0, wx1, wy1 = 555, 745, 765, 905
gray0 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
local = cv2.GaussianBlur(gray0, (0, 0), 9)
wire = np.zeros((H, W), np.float32)
box = np.s_[wy0:wy1, wx0:wx1]
# wires are grey (low raw chroma); the cloth between them is clearly green
Craw = np.hypot(A, B)
wire[box] = np.clip((15 - Craw[box]) / 6, 0, 1)
wire = cv2.GaussianBlur(wire, (0, 0), 0.8)
silver = cv2.cvtColor(np.dstack([L * 2.55, A * 0.15 + 128, B * 0.15 + 128]).clip(0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
rec = (rec * (1 - wire[..., None]) + silver * wire[..., None]).astype(np.uint8)

# ---------- countertop slivers just inside the cloth edge -> navy fabric ----------
band = cloth - cv2.erode(cloth, np.ones((41, 41), np.uint8))
ang_raw = np.degrees(np.arctan2(B, A))
sliver = ((band > 0) & (L > 50) & (ang_raw > 0) & (ang_raw < 90)).astype(np.uint8)
sliver = cv2.dilate(sliver, np.ones((5, 5), np.uint8)) & cloth
rec = cv2.inpaint(rec, sliver, 9, cv2.INPAINT_TELEA)

# ---------- warm-white studio surface ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
base = np.array([0xE7, 0xF1, 0xF6], np.float32)          # #F6F1E7 in BGR
grad = 0.965 + 0.05 * np.exp(-(((xx - 0.3 * W) / W) ** 2 + ((yy - 0.2 * H) / H) ** 2))
surface = base[None, None, :] * grad[..., None]
noise = cv2.GaussianBlur(np.random.default_rng(3).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8) * 1.6
surface += noise[..., None]
# soft contact shadow under the cloth, light from top-left -> shadow toward bottom-right
sh = cv2.GaussianBlur(cv2.warpAffine(cloth.astype(np.float32), np.float32([[1, 0, 10], [0, 1, 14]]), (W, H)), (0, 0), 16)
surface *= (1 - 0.22 * sh)[..., None]
cm = cv2.GaussianBlur(cloth.astype(np.float32), (0, 0), 1.2)[..., None]
comp = surface * (1 - cm) + rec.astype(np.float32) * cm

# ---------- light ----------
key = np.exp(-(((xx - 0.30 * W) / (1.1 * W)) ** 2 + ((yy - 0.25 * H) / (1.1 * H)) ** 2))
comp *= (0.94 + 0.10 * key)[..., None]
labc = cv2.cvtColor(comp.clip(0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
chroma = np.hypot(labc[..., 1] - 128, labc[..., 2] - 128)
whites = np.clip((labc[..., 0] - 165) / 35, 0, 1) * np.clip((20 - chroma) / 8, 0, 1) * cloth  # white plastic on the cloth
labc[..., 1] = 128 + (labc[..., 1] - 128) * (1 - 0.55 * whites)
labc[..., 2] = 128 + (labc[..., 2] - 128) * (1 - 0.55 * whites)
labc[..., 0] = np.clip(labc[..., 0] * (1 + 0.05 * whites), 0, 255)
final = cv2.cvtColor(labc.clip(0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
final = cv2.addWeighted(final, 1.25, cv2.GaussianBlur(final, (0, 0), 1.2), -0.25, 0)
cv2.imwrite(f"{OUTDIR}/full3.png", final)

# ---------- crops centred on the cloth ----------
x, y, w_, h_ = cv2.boundingRect(quad)
cx, cy = x + w_ / 2, y + h_ / 2
def crop(wd, ht):
    x0 = int(round(cx - wd / 2)); y0 = int(round(cy - ht / 2))
    x0 = max(0, min(W - wd, x0)); y0 = max(0, min(H - ht, y0))
    return final[y0:y0 + ht, x0:x0 + wd]
cv2.imwrite(f"{OUTDIR}/crop45_3.png", crop(1500, 1875))
cv2.imwrite(f"{OUTDIR}/crop11_3.png", crop(1500, 1500))
print("cloth box", (x, y, w_, h_))
