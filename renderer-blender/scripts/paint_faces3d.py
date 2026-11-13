"""Paint the swappable faces for the 3D character look test (toon3d.head_mat). Transparent 512x512 PNGs:
eyes, brows, mouth and cheeks only; the head's skin colour shows through. Original designs in the channel's own
kid style (tall oval eyes with a highlight, short brows, small mouth).

usage: python3 -I paint_faces3d.py
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "textures", "faces3d")
S, K = 512, 4            # final size, supersample
INK, WHITE, BLUSH, TONGUE = (30, 27, 51, 255), (255, 255, 255, 255), (244, 150, 140, 150), (224, 84, 70, 255)
EX, EY = 112, 250        # eye offset from centre, eye height (y down)


def canvas():
    im = Image.new("RGBA", (S * K, S * K), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def P(*v): return [x * K for x in v]


def eye(d, cx, cy, w=60, h=92, look=(0, 0)):
    d.ellipse(P(cx - w / 2 - 9, cy - h / 2 - 8, cx + w / 2 + 9, cy + h / 2 + 8), fill=WHITE)   # eye white: keeps the eye readable on any skin tone
    d.ellipse(P(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=INK)
    hx, hy = cx - w * 0.16 + look[0], cy - h * 0.2 + look[1]
    d.ellipse(P(hx - 10, hy - 10, hx + 10, hy + 10), fill=WHITE)


def brow(d, cx, cy, tilt=0, w=68, curve=6):
    s = 1 if cx > S / 2 else -1
    pts = [(cx - w / 2, cy + s * tilt + curve * 0.6), (cx, cy - curve), (cx + w / 2, cy - s * tilt + curve * 0.6)]
    d.line(P(*[c for p in pts for c in p]), fill=INK, width=14 * K, joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse(P(x - 7, y - 7, x + 7, y + 7), fill=INK)


def arc(d, box, a0, a1, width=10):
    d.arc(P(*box), a0, a1, fill=INK, width=width * K)


def blush(d):
    for s in (-1, 1):
        cx = S / 2 + s * 178
        d.ellipse(P(cx - 38, 322, cx + 38, 362), fill=BLUSH)


def face(name):
    im, d = canvas()
    L, R, c = S / 2 - EX, S / 2 + EX, S / 2
    if name == "neutral":
        eye(d, L, EY); eye(d, R, EY); brow(d, L, 168); brow(d, R, 168)
        arc(d, (c - 36, 338, c + 36, 384), 20, 160, 12); blush(d)
    elif name == "happy":
        eye(d, L, EY); eye(d, R, EY); brow(d, L, 162, tilt=-3); brow(d, R, 162, tilt=-3)
        d.chord(P(c - 56, 318, c + 56, 418), 0, 180, fill=INK)
        d.chord(P(c - 32, 376, c + 32, 426), 180, 360, fill=TONGUE); blush(d)
    elif name == "surprised":
        eye(d, L, EY, 70, 104); eye(d, R, EY, 70, 104); brow(d, L, 150, tilt=-7); brow(d, R, 150, tilt=-7)
        d.ellipse(P(c - 28, 342, c + 28, 418), fill=INK)
        d.ellipse(P(c - 15, 380, c + 15, 414), fill=TONGUE)
    elif name == "worried":
        eye(d, L, EY); eye(d, R, EY); brow(d, L, 170, tilt=-14, curve=2); brow(d, R, 170, tilt=-14, curve=2)
        arc(d, (c - 34, 356, c + 34, 404), 200, 340, 12)
    elif name == "deadpan":
        eye(d, L, EY + 6, look=(0, 8)); eye(d, R, EY + 6, look=(0, 8))
        for cx in (L, R):          # half-closed lids: clear the top of each eye, then a flat lid line
            d.rectangle(P(cx - 42, EY - 60, cx + 42, EY - 2), fill=(0, 0, 0, 0))
            d.line(P(cx - 42, EY - 2, cx + 42, EY - 2), fill=INK, width=13 * K)
        brow(d, L, 184, curve=0); brow(d, R, 184, curve=0)
        d.line(P(c - 30, 372, c + 30, 372), fill=INK, width=13 * K)
    elif name == "squint":
        for cx, s in ((L, 1), (R, -1)):
            d.line(P(cx - s * 34, EY - 32, cx + s * 28, EY, cx - s * 34, EY + 32), fill=INK, width=14 * K, joint="curve")
        brow(d, L, 180, tilt=13, curve=0); brow(d, R, 180, tilt=13, curve=0)
        d.rounded_rectangle(P(c - 50, 344, c + 50, 400), radius=12 * K, fill=WHITE, outline=INK, width=10 * K)
        for x in (c - 17, c + 17):
            d.line(P(x, 350, x, 394), fill=INK, width=7 * K)
        d.line(P(c - 44, 372, c + 44, 372), fill=INK, width=7 * K)
    elif name == "blink":      # eyes shut for two frames: used for blinks and between two faces
        for cx in (L, R):
            arc(d, (cx - 32, EY - 30, cx + 32, EY + 14), 20, 160, 13)
        brow(d, L, 172); brow(d, R, 172)
        arc(d, (c - 30, 344, c + 30, 384), 20, 160, 12)
    elif name == "smug":
        eye(d, L, EY + 4, look=(10, 4)); eye(d, R, EY + 4, look=(10, 4))
        for cx in (L, R):
            d.rectangle(P(cx - 42, EY - 60, cx + 42, EY - 16), fill=(0, 0, 0, 0))
            d.line(P(cx - 42, EY - 16, cx + 42, EY - 16), fill=INK, width=13 * K)
        brow(d, L, 176, tilt=4, curve=0); brow(d, R, 150, tilt=-9, curve=7)
        d.line(P(c - 34, 372, c + 6, 378, c + 40, 352), fill=INK, width=13 * K, joint="curve")
    elif name == "nervous":
        for cx in (L, R):
            d.ellipse(P(cx - 40, EY - 44, cx + 40, EY + 44), fill=WHITE, outline=INK, width=10 * K)
            d.ellipse(P(cx - 10, EY - 10, cx + 10, EY + 10), fill=INK)
        brow(d, L, 166, tilt=-12, curve=2); brow(d, R, 166, tilt=-12, curve=2)
        pts = [(c - 44, 372), (c - 26, 358), (c - 8, 374), (c + 10, 358), (c + 28, 374), (c + 44, 360)]
        d.line(P(*[v for p in pts for v in p]), fill=INK, width=12 * K, joint="curve")
        sx, sy = c + 196, 150      # a sweat drop at the temple
        d.polygon(P(sx, sy - 34, sx - 17, sy + 6, sx + 17, sy + 6), fill=(126, 196, 240, 255))
        d.ellipse(P(sx - 18, sy - 10, sx + 18, sy + 26), fill=(126, 196, 240, 255))
    elif name == "laugh":
        for cx in (L, R):
            arc(d, (cx - 34, EY - 26, cx + 34, EY + 42), 200, 340, 14)
        brow(d, L, 170, tilt=-4); brow(d, R, 170, tilt=-4)
        d.chord(P(c - 70, 300, c + 70, 436), 0, 180, fill=INK)
        d.chord(P(c - 40, 388, c + 40, 446), 180, 360, fill=TONGUE)
        d.rectangle(P(c - 52, 366, c + 52, 380), fill=WHITE); blush(d)
    im.resize((S, S), Image.LANCZOS).save(os.path.join(OUT, name + ".png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for nm in ("neutral", "happy", "surprised", "worried", "deadpan", "squint", "smug", "nervous", "laugh", "blink"):
        face(nm); print(nm)
