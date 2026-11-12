"""Paint the EP004 textures and cut the CHAR-RAINKID cards (set-specs v1, approved 2026-11-11).

Reuses the EP003 painting helpers (imported, not changed). New textures get an `ep4_` prefix so
no EP003 texture is overwritten. Kid cards are drawn from the approved RAINKID generators
(same code as the approved sheets; one pose at full size, the card's own contact shadow removed
because Blender adds one) and rasterized with headless Chrome.

usage: python3 -I paint_textures_ep004.py [textures|cards|all] [card file ...]
"""
import os, re, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paint_textures_ep003 as p3  # helpers only; its __main__ block does not run on import
from paint_textures_ep003 import plain, wood, fabric, equirect, speckle, hexrgb, fbm, tint, strokes, save

ROOT, TEX, CARDS = p3.ROOT, p3.TEX, p3.CARDS
CHAR_DIR = os.path.join(ROOT, "02_CONTEXT/assets/drafts/characters")
sys.path.insert(0, CHAR_DIR)


def textures():
    wood(512, "#E8CF8E", 10, "ep4_siding_yellow.png")          # soft yellow house (set-specs decision 1)
    wood(512, "#3FA7A0", 3, "ep4_trim_teal.png", plank_gap=False)  # teal window frame
    wood(512, "#F3E7CF", 3, "ep4_trim_cream.png", plank_gap=False)
    wood(512, "#B8875A", 6, "ep4_planter.png")
    plain("ep4_soil.png", "#6E4A33", amt=0.35)
    plain("ep4_flower_pink.png", "#EE8FA6", amt=0.2); plain("ep4_flower_white.png", "#F6F1E6", amt=0.15)
    plain("ep4_lampshade.png", "#F6D9A0", amt=0.15)
    books()
    plain("ep4_cloud.png", "#FBF8FF", scale=120, amt=0.08, n_strokes=300)
    plain("ep4_cloud_grey.png", "#A9B0BF", scale=120, amt=0.12, n_strokes=300)
    plain("ep4_wave.png", "#7FD3CF", scale=80, amt=0.15, stroke_ang=0)
    equirect("ep4_sky_high_eq.png", "#4F8FD6", "#CFE6F6", "#8FC4D6",
             clouds=[("#FFFFFF", "#D9E4F2", 18, 0.42, 0.495), ("#F4F8FF", "#D3DEEE", 8, 0.30, 0.40)])
    speckle("ep4_lawn.png", "#8DAA66", [("#76924F", 1400, 3), ("#A9C283", 600, 2)])
    equirect("ep4_sky_rain_eq.png", "#8E9BB0", "#C9D0DA", "#9AA4AE",
             clouds=[("#BCC4D0", "#9AA3B3", 40, 0.30, 0.49), ("#C7CED8", "#A7AFBD", 24, 0.12, 0.30)])
    equirect("ep4_sky_bright_eq.png", "#6FB4EA", "#DCEFF8", "#C9DDC4",
             clouds=[("#FFFFFF", "#DCE6F0", 6, 0.40, 0.47)])
    # later additions go last, so the random strokes of earlier textures stay identical
    speckle("ep4_wet_sand.png", "#B89B6E", [("#9C805A", 900, 3), ("#CDB487", 500, 3)], waves=("#A68B62", 160))
    speckle("ep4_seabed_dry.png", "#CDB78F", [("#B39C74", 900, 3), ("#E2D0AC", 400, 3)], waves=("#BBA47C", 200))
    plain("ep4_seaweed.png", "#5E8A4E", amt=0.3, stroke_ang=80)
    wood(512, "#C9A06A", 5, "ep4_boat.png")
    # BG-INLAND sky card: the LS5 bright sky with no painted clouds (S07-S08's thinning 3D clouds stand alone)
    equirect("ep4_sky_thin_eq.png", "#6FB4EA", "#DCEFF8", "#C9DDC4", clouds=[])


def books(name="ep4_books.png", S=512):
    """A shelf row of painted book spines."""
    cols = ["#C8574A", "#4E7FB0", "#E1B44C", "#5E9A6A", "#8E6BB0", "#E58B7B", "#3F7A8C", "#D9A066"]
    img = np.zeros((S, S, 3))
    x, rng = 0, np.random.default_rng(4)
    while x < S:
        w = min(int(rng.integers(26, 52)), S - x); c = hexrgb(cols[int(rng.integers(len(cols)))])
        top = int(rng.integers(0, 70))
        img[top:, x:x + w] = tint(c, fbm(w, S - top, 30, seed=x), 0.2)
        img[top + 30:top + 38, x + 4:x + w - 4] = c * 0.7
        img[top:, x:x + 3] = c * 0.6
        x += w
    im = strokes(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)), 300, lambda: hexrgb("#FFFFFF") * 0.9, 30, 2, 90, 5, 25)
    save(im, name)


# ---------------- CHAR-RAINKID cards ----------------
CARD_JOBS = [  # (pose, outfit, face, card file)
    ("POSE-RAINKID-WINDOW", "OUTFIT-RAINKID-INDOOR", "curious", "RAINKID-WINDOW-CURIOUS.png"),
    ("POSE-RAINKID-WINDOW", "OUTFIT-RAINKID-INDOOR", "wistful", "RAINKID-WINDOW-WISTFUL.png"),
    ("POSE-RAINKID-SHOCK", "OUTFIT-RAINKID-RAIN", "shocked", "RAINKID-SHOCK-RAIN.png"),
    ("POSE-RAINKID-SHORE", "OUTFIT-RAINKID-RAIN", "deadpan", "RAINKID-SHORE-RAIN.png"),
    ("POSE-RAINKID-POINT-UP", "OUTFIT-RAINKID-RAIN", "worried", "RAINKID-POINTUP-RAIN.png"),   # S07 V4
]


def cards(only=None):
    """Cut the kid cards; `only` limits the run to the named card files (earlier cards stay untouched)."""
    import make_rainkid_batch2_v001 as b2
    tmp = os.path.join(CARDS, "_svg"); os.makedirs(tmp, exist_ok=True)
    paths = []
    for pose, outfit, face, out in CARD_JOBS:
        if only and out not in only:
            continue
        fig = b2.figure(pose, outfit, face, 0, 0, 1.0)
        fig = re.sub(r'<ellipse cx="0" cy="2" rx="150" ry="20" fill="url\(#cshadow\)"/>', "", fig, count=1)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-320 -960 640 1000" width="640" height="1000">'
               f'{b2.defs()}{fig}</svg>')
        n = 0
        while 'id="mclip"' in svg:
            n += 1; svg = svg.replace('id="mclip"', f'id="mclip{n}"', 1).replace('url(#mclip)', f'url(#mclip{n})', 1)
        p = os.path.join(tmp, out.replace(".png", ".svg")); open(p, "w").write(svg); paths.append(p)
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "rasterize.py"), tmp, "2"] + paths, check=True)
    for p in paths:
        png = p.replace(".svg", ".png")
        im = Image.open(png).convert("RGBA")
        box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        dst = os.path.join(CARDS, os.path.basename(png))
        im.crop(box).save(dst); print(os.path.basename(dst), im.crop(box).size)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    os.makedirs(TEX, exist_ok=True); os.makedirs(CARDS, exist_ok=True)
    if what in ("textures", "all"):
        textures()
    if what in ("cards", "all"):
        cards(sys.argv[2:] or None)
