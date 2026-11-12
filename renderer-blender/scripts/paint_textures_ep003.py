"""Paint the EP003 bedroom look-test textures and cut the approved kid cards.

Textures are painted procedurally (layered value noise plus brush strokes) so
surfaces read as hand-painted (set-specs v1). Kid cards are cut from the
approved SVG (read only) with headless Chrome.

usage: python3 -I paint_textures_ep003.py
"""
import math, os, random, re, subprocess, tempfile, time
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEX = os.path.join(ROOT, "renderer-blender/textures")
CARDS = os.path.join(ROOT, "renderer-blender/cards")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
rng = np.random.default_rng(3)
random.seed(3)


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def fbm(w, h, scale, octaves=5, seed=0):
    """Value noise in [0,1]: sum of upsampled random grids."""
    r = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        gw, gh = max(2, int(w / scale * 2 ** o)), max(2, int(h / scale * 2 ** o))
        g = Image.fromarray((r.random((gh, gw)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += amp * np.asarray(g, float) / 255
        tot += amp
        amp *= 0.5
    return out / tot


def strokes(img, n, color_fn, length, width, angle, jitter, alpha, blur=1.2):
    """Semi-transparent brush strokes painted over img (RGB PIL)."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    W, H = img.size
    for _ in range(n):
        x, y = random.uniform(0, W), random.uniform(0, H)
        a = math.radians(angle + random.uniform(-jitter, jitter))
        L = length * random.uniform(0.5, 1.3)
        c = tuple(int(v) for v in color_fn()) + (int(alpha * random.uniform(0.5, 1.0)),)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=c, width=max(1, int(width * random.uniform(0.6, 1.4))))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def tint(base, n, amount):
    return np.clip(base[None, None, :] * (1 + amount * (n[..., None] - 0.5)), 0, 255)


def save(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(TEX, name)) if isinstance(arr, np.ndarray) else arr.save(os.path.join(TEX, name))
    print(name)


def wallpaper(S=1024):
    n = fbm(S, S, 220, seed=1) * 0.6 + fbm(S, S, 40, seed=2) * 0.4
    img = tint(hexrgb("#F2DFBD"), n, 0.16)
    x = np.arange(S)[None, :]
    stripe = (np.sin(x / S * 2 * math.pi * 8) > 0.55)[..., None]
    img = np.where(stripe, img * 0.88, img)
    im = Image.fromarray(img.astype(np.uint8))
    d = ImageDraw.Draw(im)
    for gy in range(12):
        for gx in range(12):
            cx = (gx + 0.5 + (gy % 2) * 0.5) * S / 12 + random.uniform(-5, 5)
            cy = (gy + 0.5) * S / 12 + random.uniform(-5, 5)
            col = random.choice([(214, 129, 112), (95, 160, 150), (226, 174, 92)])
            for k in range(5):
                a = k * 2 * math.pi / 5
                px, py = cx + 11 * math.cos(a), cy + 11 * math.sin(a)
                d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col)
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(250, 236, 200))
            d.line([(cx, cy + 14), (cx + 6, cy + 34)], fill=(110, 150, 110), width=3)
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im = strokes(im, 900, lambda: hexrgb("#FFF3DA") * random.uniform(0.9, 1.02), 60, 6, 90, 8, 40)
    save(im, "wallpaper.png")


def wood(S, base, planks, name, plank_gap=True):
    img = np.zeros((S, S, 3))
    ph = S // planks
    for p in range(planks):
        c = hexrgb(base) * random.uniform(0.88, 1.08)
        y0 = p * ph
        yy, xx = np.mgrid[0:ph, 0:S]
        off = random.uniform(0, 100)
        grain = np.sin((yy + 6 * np.sin(xx / random.uniform(40, 90) + off)) / random.uniform(2.5, 4.0)) * 0.5 + 0.5
        n = fbm(S, ph, 120, seed=10 + p)
        shade = 0.9 + 0.12 * n - 0.07 * grain
        img[y0:y0 + ph] = c[None, None, :] * shade[..., None]
        if plank_gap:
            img[y0:y0 + 3] = hexrgb(base) * 0.55
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(planks // 2 + 2):
        cx, cy = random.uniform(0, S), random.uniform(0, S)
        for r in (14, 9, 4):
            d.ellipse([cx - r * 1.8, cy - r, cx + r * 1.8, cy + r], outline=tuple(int(v) for v in hexrgb(base) * 0.6), width=2)
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.6)), 1800, lambda: hexrgb(base) * random.uniform(0.6, 1.25), 90, 3, 0, 4, 80)
    save(im, name)


def fabric(S, base, name, folds=0):
    n = fbm(S, S, 160, seed=21)
    img = tint(hexrgb(base), n, 0.14)
    if folds:
        x = np.arange(S)[None, :] / S
        f = 0.82 + 0.18 * (np.sin(x * 2 * math.pi * folds) * 0.5 + 0.5)
        img = img * f[..., None]
    yy, xx = np.mgrid[0:S, 0:S]
    weave = ((xx // 3 + yy // 3) % 2) * 0.04
    img = img * (1 - weave[..., None])
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    hem = tuple(int(v) for v in hexrgb(base) * 0.7)
    d.rectangle([0, S - 40, S, S - 28], fill=hem)
    im = strokes(im, 1200, lambda: hexrgb(base) * random.uniform(0.8, 1.15), 120, 5, 90, 6, 45)
    save(im, name)


def sky(name, top, horizon, cloud, cloud_shade, n_clouds=7, W=2048, H=1024, glow=None):
    y = np.linspace(0, 1, H)[:, None, None]
    img = hexrgb(top)[None, None] * (1 - y) + hexrgb(horizon)[None, None] * y
    img = np.repeat(img, W, axis=1)
    if glow:
        cx, cy, col = glow
        yy, xx = np.mgrid[0:H, 0:W]
        g = np.exp(-(((xx - cx * W) / (W * 0.25)) ** 2 + ((yy - cy * H) / (H * 0.35)) ** 2))
        img = img * (1 - 0.6 * g[..., None]) + hexrgb(col)[None, None] * 0.6 * g[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im = strokes(im, 600, lambda: hexrgb(horizon) * random.uniform(0.95, 1.05), 160, 10, 0, 5, 30, 2)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n_clouds):
        cx, cy = random.uniform(0.05, 0.95) * W, random.uniform(0.15, 0.7) * H
        s = random.uniform(70, 140)
        for _ in range(9):
            ox, oy = random.uniform(-2.2, 2.2) * s, random.uniform(-0.5, 0.3) * s
            r = s * random.uniform(0.55, 1.0)
            d.ellipse([cx + ox - r, cy + oy - r * 0.8 + r * 0.25, cx + ox + r, cy + oy + r * 0.8 + r * 0.25], fill=tuple(int(v) for v in hexrgb(cloud_shade)) + (255,))
            d.ellipse([cx + ox - r, cy + oy - r * 0.8, cx + ox + r, cy + oy + r * 0.8 - r * 0.15], fill=tuple(int(v) for v in hexrgb(cloud)) + (255,))
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    im = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    im = strokes(im, 500, lambda: hexrgb(cloud) * random.uniform(0.95, 1.0), 50, 5, 0, 20, 35)
    save(im, name)


def globe(name="globe.png", W=1024, H=512):
    n = fbm(W, H, 140, seed=31)
    img = tint(hexrgb("#4A90C8"), fbm(W, H, 60, seed=32), 0.18)
    land = n > 0.56
    landc = np.where((fbm(W, H, 90, seed=33) > 0.5)[..., None], hexrgb("#7DB66A"), hexrgb("#D9B77A"))
    img = np.where(land[..., None], landc * (0.9 + 0.2 * fbm(W, H, 30, seed=34)[..., None]), img)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    edge = Image.fromarray((land * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)
    im.paste((60, 90, 70), mask=edge.filter(ImageFilter.MaxFilter(3)))
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.8)), 700, lambda: hexrgb("#6FA9D8") * random.uniform(0.9, 1.1), 40, 4, 0, 30, 40)
    save(im, name)


def rock(name="rock.png", S=512):
    img = tint(hexrgb("#A8865E"), fbm(S, S, 50, seed=41), 0.35)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im = strokes(im, 600, lambda: hexrgb("#8F7C66") * random.uniform(0.8, 1.2), 30, 3, 0, 180, 70)
    save(im, name)


def rug(name="rug.png", S=1024):
    yy, xx = np.mgrid[0:S, 0:S]
    r = np.hypot(xx - S / 2, yy - S / 2) / (S / 2)
    cols = [hexrgb(c) for c in ("#E58B7B", "#F2C14E", "#6BAFA6", "#FFF1D6", "#E58B7B", "#F2C14E")]
    band = np.clip((r * 6).astype(int), 0, 5)
    img = np.stack([np.choose(band, [c[i] for c in cols]) for i in range(3)], -1)
    img = img * (0.9 + 0.15 * fbm(S, S, 30, seed=51)[..., None])
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im = strokes(im, 1500, lambda: hexrgb("#FFF1D6") * random.uniform(0.8, 1.0), 20, 3, 0, 180, 40)
    save(im, name)


def plain(name, base, scale=60, amt=0.2, stroke_ang=0, n_strokes=500):
    S = 512
    img = tint(hexrgb(base), fbm(S, S, scale, seed=hash(name) % 100), amt)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    im = strokes(im, n_strokes, lambda: hexrgb(base) * random.uniform(0.92, 1.08), 40, 4, stroke_ang, 15, 35)
    save(im, name)


def picture(name="picture.png", W=768, H=576):
    """A small painted landscape for a wall frame (hills, a house, a sun)."""
    sky("_tmp_sky.png", "#7FC0E8", "#F3E3B8", "#FFFFFF", "#E2E8EE", n_clouds=3, W=W, H=H)
    im = Image.open(os.path.join(TEX, "_tmp_sky.png")).convert("RGB")
    os.unlink(os.path.join(TEX, "_tmp_sky.png"))
    d = ImageDraw.Draw(im)
    d.ellipse([W * 0.7, H * 0.12, W * 0.84, H * 0.3], fill=(250, 214, 110))
    for k, (col, y) in enumerate((((120, 170, 95), 0.62), ((96, 150, 80), 0.72), ((80, 130, 70), 0.84))):
        pts = [(x, H * y + 30 * math.sin(x / W * 6 + k)) for x in range(0, W + 8, 8)] + [(W, H), (0, H)]
        d.polygon(pts, fill=col)
    d.rectangle([W * 0.2, H * 0.55, W * 0.32, H * 0.68], fill=(240, 228, 205), outline=(90, 70, 60), width=3)
    d.polygon([(W * 0.18, H * 0.56), (W * 0.26, H * 0.46), (W * 0.34, H * 0.56)], fill=(200, 90, 70), outline=(90, 70, 60))
    im = strokes(im, 900, lambda: np.array(im.getpixel((random.randrange(W), random.randrange(H)))) * random.uniform(0.85, 1.1), 18, 4, 0, 180, 120, 0.6)
    save(im, name)


def kid_cards():
    SVG = "http://www.w3.org/2000/svg"
    ET.register_namespace("", SVG)
    src = os.path.join(ROOT, "02_CONTEXT/assets/characters/ASSET-CHAR-KID-MASTER-v001.svg")
    for keep, drop, out in (("CHAR-KID-front", "CHAR-KID-back", "KID-FRONT.png"), ("CHAR-KID-back", "CHAR-KID-front", "KID-BACK.png")):
        root = ET.parse(src).getroot()
        for el in list(root):
            if el.get("id") in ("preview-backdrop", drop) or el.tag.endswith("text"):
                root.remove(el)
        for el in list(root):
            if el.get("id") == keep:
                # the panel's contact shadow is replaced by a 3D one in Blender
                for c in list(el):
                    if c.get("id") == "contact-shadow":
                        el.remove(c)
        svg = ET.tostring(root, encoding="unicode")
        W, H = 3000, 2000
        svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{W}" height="{H}"', svg, count=1)
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
            t.write(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
        png = os.path.join(CARDS, out)
        if os.path.exists(png):
            os.unlink(png)
        p = subprocess.Popen([CHROME, "--headless=new", "--no-first-run", "--disable-gpu", "--hide-scrollbars",
                              f"--user-data-dir={tempfile.gettempdir()}/rasterize-chrome", "--default-background-color=00000000",
                              f"--window-size={W},{H}", f"--screenshot={png}", "file://" + t.name],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):
            time.sleep(0.5)
            if p.poll() is not None or (os.path.exists(png) and os.path.getsize(png) > 0):
                time.sleep(1.0)
                break
        p.kill(); p.wait(); os.unlink(t.name)
        im = Image.open(png).convert("RGBA")
        box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        im.crop(box).save(png)
        print(out, im.crop(box).size)


# ---------------- textures for the other seven sets ----------------
def roof_tiles(name, base, S=1024, rows=14, cols=10):
    img = Image.new("RGB", (S, S), tuple(int(v) for v in hexrgb(base) * 0.6))
    d = ImageDraw.Draw(img)
    rh, cw = S / rows, S / cols
    for r in range(rows + 1):
        off = (r % 2) * cw / 2
        for c in range(-1, cols + 1):
            x0, y0 = c * cw + off, r * rh - rh * 0.4
            col = tuple(int(v) for v in hexrgb(base) * random.uniform(0.85, 1.12))
            d.chord([x0 + 2, y0, x0 + cw - 2, y0 + rh * 1.5], 0, 180, fill=col, outline=tuple(int(v) for v in hexrgb(base) * 0.55), width=3)
    img = strokes(img.filter(ImageFilter.GaussianBlur(0.7)), 800, lambda: hexrgb(base) * random.uniform(0.9, 1.3), 30, 3, 0, 30, 60)
    save(img, name)


def brick(name="brick.png", S=512, rows=12):
    img = Image.new("RGB", (S, S), (226, 210, 180))
    d = ImageDraw.Draw(img)
    rh = S / rows
    for r in range(rows):
        off = (r % 2) * S / 8
        for c in range(-1, 5):
            col = tuple(int(v) for v in hexrgb("#B5583F") * random.uniform(0.82, 1.12))
            d.rounded_rectangle([c * S / 4 + off + 3, r * rh + 3, (c + 1) * S / 4 + off - 3, (r + 1) * rh - 3], radius=5, fill=col)
    img = strokes(img.filter(ImageFilter.GaussianBlur(0.6)), 500, lambda: hexrgb("#B5583F") * random.uniform(0.8, 1.2), 20, 3, 0, 30, 60)
    save(img, name)


def speckle(name, base, dots, S=1024, waves=None):
    img = tint(hexrgb(base), fbm(S, S, 120, seed=len(name)), 0.16)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for col, n, r in dots:
        for _ in range(n):
            x, y = random.uniform(0, S), random.uniform(0, S)
            rr = r * random.uniform(0.5, 1.3)
            d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=tuple(int(v) for v in hexrgb(col) * random.uniform(0.9, 1.1)))
    if waves:
        for _ in range(waves[1]):
            x, y = random.uniform(0, S), random.uniform(0, S)
            d.arc([x - 40, y - 8, x + 40, y + 8], 200, 340, fill=tuple(int(v) for v in hexrgb(waves[0])), width=3)
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.6)), 900, lambda: hexrgb(base) * random.uniform(0.88, 1.1), 50, 4, 0, 10, 45)
    save(im, name)


def sea(name="sea.png", S=1024):
    y = np.linspace(0, 1, S)[:, None, None]
    img = np.repeat(hexrgb("#3FA9B8")[None, None] * (1 - y) + hexrgb("#7FD6D0")[None, None] * y, S, axis=1)
    im = Image.fromarray(np.clip(img * (0.92 + 0.12 * fbm(S, S, 80, seed=61)[..., None]), 0, 255).astype(np.uint8))
    im = strokes(im, 1400, lambda: hexrgb("#2E8E9E") * random.uniform(0.9, 1.1), 90, 5, 0, 6, 90)
    im = strokes(im, 700, lambda: hexrgb("#F2FBF8"), 60, 4, 0, 8, 160, 0.8)
    save(im, name)


def bark(name="bark.png", S=512):
    img = tint(hexrgb("#9C7350"), fbm(S, S, 60, seed=71), 0.2)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for y in range(0, S, 32):
        d.arc([-40, y - 10, S + 40, y + 22], 0, 180, fill=(110, 78, 52), width=5)
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.6)), 500, lambda: hexrgb("#9C7350") * random.uniform(0.8, 1.2), 30, 3, 90, 10, 60)
    save(im, name)


def leaf(name, base, vein, S=512, stripes=True):
    img = tint(hexrgb(base), fbm(S, S, 50, seed=len(name) + 80), 0.2)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.line([(0, S / 2), (S, S / 2)], fill=tuple(int(v) for v in hexrgb(vein)), width=10)
    if stripes:
        for x in range(0, S, 22):
            d.line([(x, S / 2), (x + 40, 0)], fill=tuple(int(v) for v in hexrgb(base) * 0.75), width=3)
            d.line([(x, S / 2), (x + 40, S)], fill=tuple(int(v) for v in hexrgb(base) * 0.75), width=3)
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.8)), 500, lambda: hexrgb(base) * random.uniform(0.85, 1.25), 40, 4, 0, 20, 60)
    save(im, name)


def windows(name, wall, glass, S=512, cols=4, rows=6):
    img = tint(hexrgb(wall), fbm(S, S, 80, seed=len(name) + 90), 0.15)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for r in range(rows):
        for c in range(cols):
            x0, y0 = (c + 0.2) * S / cols, (r + 0.22) * S / rows
            lit = random.random() < 0.25
            col = hexrgb("#F6D88A") if lit else hexrgb(glass) * random.uniform(0.9, 1.15)
            d.rounded_rectangle([x0, y0, x0 + S / cols * 0.6, y0 + S / rows * 0.55], radius=4, fill=tuple(int(v) for v in col),
                                outline=tuple(int(v) for v in hexrgb(wall) * 0.6), width=3)
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.6)), 400, lambda: hexrgb(wall) * random.uniform(0.85, 1.15), 40, 4, 90, 10, 45)
    save(im, name)


def equirect(name, zenith, horizon, ground, clouds=(), glow=None, W=4096, H=2048, stars=0, nebula=()):
    v = np.linspace(1, -1, H)[:, None, None]  # +1 = zenith, 0 = horizon
    up = np.clip(v, 0, 1) ** 0.6
    img = hexrgb(horizon)[None, None] * (1 - up) + hexrgb(zenith)[None, None] * up
    img = np.where(v < 0, hexrgb(ground)[None, None] * np.ones_like(up), img)
    img = np.repeat(img, W, axis=1)
    yy, xx = np.mgrid[0:H, 0:W]
    if glow:
        for gu in (glow[0], glow[0] - 1, glow[0] + 1):
            g = np.exp(-(((xx - gu * W) / (W * 0.12)) ** 2 + ((yy - glow[1] * H) / (H * 0.12)) ** 2))
            img = img * (1 - 0.7 * g[..., None]) + hexrgb(glow[2])[None, None] * 0.7 * g[..., None]
    for col, (cu, cv, sx, sy) in nebula:
        g = np.exp(-(((xx - cu * W) / (W * sx)) ** 2 + ((yy - cv * H) / (H * sy)) ** 2)) * fbm(W, H, 300, seed=int(cu * 100))
        img = img * (1 - 0.8 * g[..., None]) + hexrgb(col)[None, None] * 0.8 * g[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(stars):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.choice([1, 1, 1.5, 2, 3])
        c = random.choice([(255, 255, 255), (255, 240, 200), (200, 220, 255)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        if r >= 3:
            d.line([(x - 9, y), (x + 9, y)], fill=c, width=1); d.line([(x, y - 9), (x, y + 9)], fill=c, width=1)
    im = strokes(im, 1500, lambda: np.array(im.getpixel((random.randrange(W), random.randrange(H // 2)))) * random.uniform(0.96, 1.04), 220, 12, 0, 4, 40, 2)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    for col, shade, n, vmin, vmax in clouds:
        for _ in range(n):
            cx, cy = random.uniform(0, W), H * random.uniform(vmin, vmax)
            s = random.uniform(40, 110)
            for _ in range(8):
                ox, oy, r = random.uniform(-2.5, 2.5) * s, random.uniform(-0.4, 0.2) * s, s * random.uniform(0.5, 1.0)
                dl.ellipse([cx + ox - r, cy + oy - r * 0.6 + r * 0.2, cx + ox + r, cy + oy + r * 0.6 + r * 0.2], fill=tuple(int(v) for v in hexrgb(shade)) + (255,))
                dl.ellipse([cx + ox - r, cy + oy - r * 0.6, cx + ox + r, cy + oy + r * 0.6 - r * 0.1], fill=tuple(int(v) for v in hexrgb(col)) + (255,))
    im = Image.alpha_composite(im.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(3))).convert("RGB")
    save(im, name)


def ring_band(name="ring_band.png", W=2048, H=256):
    v = np.linspace(0, 1, H)[:, None]
    bands = 0.86 + 0.14 * np.sin(v * 60 + 3 * np.sin(v * 13)) * np.sin(v * 7)
    img = hexrgb("#D6C4A6")[None, None] * bands[..., None] * (0.9 + 0.2 * fbm(W, H, 40, seed=101)[..., None])
    img = np.repeat(img, 1, axis=0)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(6000):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.uniform(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(c) for c in hexrgb(random.choice(["#8C7660", "#D8C3A2", "#6E5C4A"]))))
    im = strokes(im, 500, lambda: hexrgb("#C9B18C") * random.uniform(0.85, 1.1), 120, 4, 0, 2, 70)
    a = np.full((H, W), 235.0)
    for c, w in ((0.30, 0.03), (0.55, 0.05), (0.78, 0.025)):
        a *= 1 - 0.85 * np.exp(-(((np.arange(H)[:, None] / H) - c) / w) ** 2)
    a *= np.clip(np.minimum(np.arange(H) / (H * 0.06), (H - np.arange(H)) / (H * 0.06)), 0, 1)[:, None]
    im = im.convert("RGBA"); im.putalpha(Image.fromarray(a.astype(np.uint8)).resize(im.size))
    save(im, name)


def ripples(name="water_surface.png", S=1024):
    layer = Image.new("RGBA", (S, S), (210, 250, 245, 60))
    d = ImageDraw.Draw(layer)
    for _ in range(500):
        x, y, w = random.uniform(0, S), random.uniform(0, S), random.uniform(30, 90)
        d.arc([x - w, y - w * 0.3, x + w, y + w * 0.3], random.uniform(180, 220), random.uniform(320, 360), fill=(240, 255, 250, 200), width=4)
    layer.filter(ImageFilter.GaussianBlur(1.5)).save(os.path.join(TEX, name)); print(name)


def dedupe_attrs(svg):
    """Keep the first of any repeated attribute in a tag, as browsers do (some sheets repeat `stroke`)."""
    def fix(m):
        seen, out = set(), []
        for a in re.finditer(r'\s+([\w:-]+)="[^"]*"', m.group(2)):
            if a.group(1) not in seen:
                seen.add(a.group(1)); out.append(a.group(0))
        return "<" + m.group(1) + "".join(out) + m.group(3) + ">"
    return re.sub(r'<([\w:]+)((?:\s+[\w:-]+="[^"]*")*)\s*(/?)>', fix, svg)


def cut_cards():
    """Cut posed cards from the approved character sheets (read only)."""
    SVG = "http://www.w3.org/2000/svg"
    ET.register_namespace("", SVG)
    jobs = [("ASSET-CHAR-KID-OUTFITS-v001.svg", "OUTFIT-BEACH-1", "KID-BEACH-LOOKUP.png"),
            ("ASSET-CHAR-KID-POSES-v001.svg", "POSE-KID-ARM-SWEEP", "KID-ARM-SWEEP.png"),
            ("ASSET-CHAR-KID-OUTFITS-v001.svg", "OUTFIT-NORTH-3", "KID-NORTH-SHRUG.png"),
            ("ASSET-CHAR-TRILOBITE-v001.svg", 1, "TRILOBITE-LOOKUP.png"),
            ("ASSET-CHAR-DINO-v001.svg", 2, "DINO-LOOKUP.png"),
            ("ASSET-CHAR-DINO-v001.svg", 0, "DINO-STEP-A.png"),
            ("ASSET-CHAR-DINO-v001.svg", 1, "DINO-STEP-B.png"),
            ("ASSET-CHAR-KID-POSES-v001.svg", "POSE-KID-CURTAINS", "KID-CURTAINS.png"),
            ("ASSET-CHAR-KID-POSES-v001.svg", "POSE-KID-LOOK-UP", "KID-LOOK-UP.png"),
            ("ASSET-CHAR-KID-POSES-v001.svg", "POSE-KID-BACK-LOOK-UP", "KID-BACK-LOOK-UP.png")]
    for src, keep, out in jobs:
        root = ET.fromstring(dedupe_attrs(open(os.path.join(ROOT, "02_CONTEXT/assets/characters", src)).read()))
        gs = [el for el in root if el.tag.endswith("}g")]
        target = gs[keep] if isinstance(keep, int) else next(el for el in gs if el.get("id") == keep)
        for el in list(root):
            if el.tag.endswith("}g") and el is not target or el.tag.endswith("text") or el.get("id") == "preview-backdrop":
                root.remove(el)
        for el in target.iter():
            for c in list(el):
                if c.get("id") == "contact-shadow":
                    el.remove(c)
        vb = [float(x) for x in root.get("viewBox").split()]
        W, H = int(vb[2] * 1.4), int(vb[3] * 1.4)
        svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{W}" height="{H}"', ET.tostring(root, encoding="unicode"), count=1)
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
            t.write(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
        png = os.path.join(CARDS, out)
        if os.path.exists(png):
            os.unlink(png)
        p = subprocess.Popen([CHROME, "--headless=new", "--no-first-run", "--disable-gpu", "--hide-scrollbars",
                              f"--user-data-dir={tempfile.gettempdir()}/rasterize-chrome", "--default-background-color=00000000",
                              f"--window-size={W},{H}", f"--screenshot={png}", "file://" + t.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):
            time.sleep(0.5)
            if p.poll() is not None or (os.path.exists(png) and os.path.getsize(png) > 0):
                time.sleep(1.0); break
        p.kill(); p.wait(); os.unlink(t.name)
        im = Image.open(png).convert("RGBA")
        box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        im.crop(box).save(png)
        print(out, im.crop(box).size)


def sets_textures():
    roof_tiles("roof_red.png", "#C8654A"); roof_tiles("roof_blue.png", "#5C7FA8"); roof_tiles("roof_snow.png", "#EEF3F8")
    for nm, c in (("plaster_cream", "#EED9B0"), ("plaster_blue", "#9CC3D9"), ("plaster_pink", "#E6AFA0"), ("plaster_green", "#A9C99A")):
        plain(nm + ".png", c, amt=0.18)
    brick()
    wood(512, "#B8473B", 10, "siding_red.png"); wood(512, "#E1B44C", 10, "siding_yellow.png")
    plain("glass.png", "#3E5F86", amt=0.15)
    speckle("sand.png", "#E8CF9A", [("#C9A66B", 900, 3), ("#F7E9C6", 500, 3)])
    sea(); bark()
    leaf("palm_leaf.png", "#5DA857", "#3E7D3C"); leaf("fern.png", "#4E9E6A", "#2F6E4A")
    speckle("concrete.png", "#C9C2B4", [("#A69E90", 700, 2), ("#DAD4C7", 400, 3)])
    plain("metal.png", "#5E7A8C", amt=0.15)
    windows("bldg_a.png", "#D9B48A", "#5A7FA6"); windows("bldg_b.png", "#A9BCC9", "#45627F"); windows("bldg_c.png", "#E7C9B5", "#5A7FA6")
    speckle("snow.png", "#EEF4FA", [("#D5E2F0", 800, 4), ("#FFFFFF", 300, 2)])
    plain("pine.png", "#3F7A5A", amt=0.3, stroke_ang=70)
    speckle("seabed.png", "#D9C39A", [("#B9A178", 700, 3), ("#EADBB8", 300, 3)], waves=("#BFA67D", 220))
    plain("sponge_orange.png", "#E0874F", amt=0.3); plain("sponge_purple.png", "#9A6BB0", amt=0.3)
    speckle("grass.png", "#8DBB5E", [("#6E9E45", 1500, 3), ("#B8D67E", 600, 2)])
    plain("hills.png", "#7FA864", scale=150, amt=0.2)
    ring_band(); ripples()
    equirect("sky_day_eq.png", "#5FA8E6", "#D6EEF8", "#CFE3D9", clouds=[("#FFFFFF", "#D6E4F2", 26, 0.36, 0.48), ("#FFFFFF", "#D6E4F2", 10, 0.15, 0.32)])
    equirect("sky_cool_eq.png", "#7F9CCB", "#F2D3BE", "#DDE6EE", clouds=[("#F4F0F2", "#D2D3E0", 14, 0.38, 0.48)], glow=(0.25, 0.5, "#FFE0B8"))
    equirect("sky_dawn_eq.png", "#8FA6D6", "#F6C9A8", "#D9CFC4", clouds=[("#FFF2E6", "#E7C6C8", 14, 0.36, 0.47)], glow=(0.0, 0.5, "#FFE6C0"))
    equirect("space_eq.png", "#141C44", "#1B2350", "#141C44", stars=2600,
             nebula=[("#5B3E8E", (0.3, 0.35, 0.18, 0.2)), ("#2E7C8C", (0.62, 0.6, 0.2, 0.25)), ("#7A4A8E", (0.85, 0.3, 0.12, 0.15))])
    equirect("water_eq.png", "#8FDCD2", "#2F7E86", "#1E5560", clouds=[])
    cut_cards()


# ---------------- props textures ----------------
CONTINENTS = {  # coarse (lon, lat) outlines for a toy desk globe; stylized, not a map
    "namerica": [(-168, 66), (-140, 70), (-110, 72), (-80, 74), (-62, 60), (-56, 50), (-66, 45), (-75, 35), (-81, 25), (-97, 26), (-97, 18), (-87, 15), (-80, 8), (-90, 14), (-105, 20), (-115, 30), (-125, 40), (-125, 50), (-135, 58), (-150, 60), (-165, 62)],
    "greenland": [(-55, 60), (-45, 60), (-20, 70), (-20, 80), (-40, 83), (-60, 80), (-70, 77)],
    "samerica": [(-80, 8), (-60, 10), (-50, 0), (-35, -7), (-40, -22), (-48, -28), (-58, -38), (-65, -55), (-72, -50), (-75, -40), (-72, -18), (-81, -5)],
    "eurasia": [(-10, 36), (-9, 44), (-2, 48), (5, 52), (10, 58), (5, 62), (15, 70), (30, 71), (60, 70), (80, 73), (110, 77), (140, 72), (170, 70), (180, 66), (160, 60), (140, 55), (135, 45), (122, 38), (120, 25), (108, 18), (105, 10), (100, 2), (98, 15), (90, 22), (80, 8), (72, 20), (60, 25), (50, 28), (57, 22), (52, 15), (44, 12), (35, 30), (28, 36), (20, 38), (12, 40), (3, 42)],
    "africa": [(-17, 21), (-10, 30), (-5, 36), (10, 37), (20, 32), (32, 31), (35, 25), (43, 12), (51, 12), (40, -5), (40, -15), (32, -28), (20, -35), (15, -28), (12, -15), (10, -2), (8, 5), (-8, 5), (-15, 10)],
    "australia": [(114, -22), (122, -17), (130, -12), (137, -12), (142, -11), (146, -19), (153, -27), (150, -37), (140, -38), (130, -32), (115, -34)],
    "madagascar": [(44, -13), (50, -15), (48, -25), (44, -24)],
    "uk": [(-6, 50), (2, 51), (-2, 58), (-6, 57)],
    "japan": [(130, 31), (141, 36), (142, 43), (139, 40), (132, 34)],
    "indonesia": [(95, 5), (105, -6), (115, -8), (120, -5), (110, 2), (100, 5)],
    "newguinea": [(131, -1), (150, -6), (141, -9)],
}


def map_texture(name, shapes, ocean, land_cols, W=2048, H=1024, ice=True, outline="#3C5A4A"):
    img = tint(hexrgb(ocean), fbm(W, H, 90, seed=201), 0.16)
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for pts in shapes:
        d.polygon([((lon + 180) / 360 * W, (90 - lat) / 180 * H) for lon, lat in pts], fill=255)
    if ice:
        d.rectangle([0, H * (90 + 66) / 180, W, H], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2)).point(lambda v: 255 if v > 128 else 0)
    n = fbm(W, H, 120, seed=202)
    land = np.where((n > 0.5)[..., None], hexrgb(land_cols[0]), hexrgb(land_cols[1])) * (0.9 + 0.2 * fbm(W, H, 30, seed=203)[..., None])
    if ice:
        yy = np.arange(H)[:, None, None]
        land = np.where((yy < H * 0.1) | (yy > H * 0.86), hexrgb("#F2F6FA"), land)
    im = Image.composite(Image.fromarray(np.clip(land, 0, 255).astype(np.uint8)), im, mask)
    im.paste(Image.new("RGB", im.size, tuple(int(v) for v in hexrgb(outline))), mask=mask.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3)))
    im = strokes(im.filter(ImageFilter.GaussianBlur(0.7)), 1500, lambda: hexrgb(ocean) * random.uniform(0.9, 1.12), 50, 5, 0, 20, 45)
    save(im, name)


def blobs_lonlat(specs, seed=0):
    r = random.Random(seed)
    out = []
    for lon, lat, rx, ry in specs:
        pts = []
        for k in range(36):
            a = k / 36 * 2 * math.pi
            j = 1 + 0.16 * math.sin(2 * a + r.uniform(0, 6)) + 0.06 * math.sin(5 * a + r.uniform(0, 6))
            pts.append((lon + rx * j * math.cos(a), max(-89, min(89, lat + ry * j * math.sin(a)))))
        out.append(pts)
    return out


def prop_textures():
    map_texture("earth_map.png", CONTINENTS.values(), "#4A90C8", ("#7DB66A", "#D9B77A"))
    # an ancient world: large southern landmass and scattered smaller ones, bare land (illustrative only)
    map_texture("ancient_map.png", blobs_lonlat([(20, -55, 70, 30), (-60, 5, 28, 18), (-15, -30, 16, 12), (85, 15, 22, 14), (130, -10, 12, 8)], seed=7),
                "#3E86B8", ("#C9A877", "#A98A62"), ice=False, outline="#6E5640")
    plain("asteroid.png", "#8F7F6E", scale=40, amt=0.4)
    im = Image.open(os.path.join(TEX, "asteroid.png")).convert("RGB"); d = ImageDraw.Draw(im)
    for _ in range(40):
        x, y, r = random.uniform(0, 512), random.uniform(0, 512), random.uniform(6, 26)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(108, 94, 80)); d.arc([x - r, y - r, x + r, y + r], 200, 380, fill=(176, 160, 140), width=3)
    im.filter(ImageFilter.GaussianBlur(0.8)).save(os.path.join(TEX, "asteroid.png"))
    plain("ice.png", "#CFEFFF", scale=40, amt=0.25, stroke_ang=45)
    S = 512; yy, xx = np.mgrid[0:S, 0:S]; r = np.hypot(xx - S / 2, yy - S / 2) / (S / 2)
    a = np.clip(1 - r, 0, 1) ** 1.8
    glow = np.dstack([np.full((S, S), 255), np.full((S, S), 236), np.full((S, S), 190), (a * 255)]).astype(np.uint8)
    Image.fromarray(glow, "RGBA").save(os.path.join(TEX, "glow.png")); print("glow.png")
    disc = np.dstack([np.full((S, S), 255), np.full((S, S), 246), np.full((S, S), 214), (np.clip((1 - r) * 12, 0, 1) * 255)]).astype(np.uint8)
    Image.fromarray(disc, "RGBA").save(os.path.join(TEX, "sun_disc.png")); print("sun_disc.png")
    # ring v2: many rock chunks in soft bands, gaps where the sky shows through
    W, H = 2048, 256
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    dens = lambda v: 0.25 + 0.75 * (0.5 + 0.5 * math.sin(v * 19 + 2 * math.sin(v * 7))) * (0.15 if abs(v - 0.55) < 0.04 else 1)
    for _ in range(26000):
        v = random.random()
        if random.random() > dens(v):
            continue
        x, y, rr = random.uniform(0, W), v * H, random.uniform(1.5, 4.5)
        col = tuple(int(c) for c in hexrgb(random.choice(["#CDB898", "#B49A7A", "#E3D2B4", "#9C8468"]))) + (255,)
        d.ellipse([x - rr * 1.4, y - rr, x + rr * 1.4, y + rr], fill=col)
    base = Image.new("RGBA", (W, H), tuple(int(c) for c in hexrgb("#D6C4A6")) + (90,))
    im = Image.alpha_composite(base, layer)
    a = np.asarray(im.getchannel("A"), float) * np.clip(np.minimum(np.arange(H) / (H * 0.06), (H - np.arange(H)) / (H * 0.06)), 0, 1)[:, None]
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    im.save(os.path.join(TEX, "ring_band.png")); print("ring_band.png (v2 chunks)")


def counter_cards():
    """Counter states 1..21, from the approved PROP-COUNTER-21 art (only the number changes)."""
    src = open(os.path.join(ROOT, "02_CONTEXT/assets/props/ASSET-PROP-COUNTER-21-v001.svg")).read()
    tmp = os.path.join(tempfile.gettempdir(), "ep003_counter")
    os.makedirs(tmp, exist_ok=True)
    for k in range(1, 22):
        open(os.path.join(tmp, f"PROP-COUNTER-{k:02d}-v001.svg"), "w").write(src.replace(">21</text>", f">{k}</text>"))
    cut_props(tmp)


def cut_props(src=None):
    """Printed prop cards from the draft SVGs (backdrop dropped)."""
    src = src or os.path.join(ROOT, "02_CONTEXT/assets/drafts/props")
    for f in sorted(os.listdir(src)):
        if not f.startswith("PROP-"):
            continue
        svg = open(os.path.join(src, f)).read()
        svg = re.sub(r'<rect id="preview-backdrop"[^>]*/>', "", svg)
        vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
        W, H = int(vb[2] * 2), int(vb[3] * 2)
        svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{W}" height="{H}"', svg, count=1)
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
            t.write(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
        png = os.path.join(CARDS, f.replace("-v001.svg", ".png"))
        if os.path.exists(png):
            os.unlink(png)
        p = subprocess.Popen([CHROME, "--headless=new", "--no-first-run", "--disable-gpu", "--hide-scrollbars",
                              f"--user-data-dir={tempfile.gettempdir()}/rasterize-chrome", "--default-background-color=00000000",
                              f"--window-size={W},{H}", f"--screenshot={png}", "file://" + t.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):
            time.sleep(0.5)
            if p.poll() is not None or (os.path.exists(png) and os.path.getsize(png) > 0):
                time.sleep(1.0); break
        p.kill(); p.wait(); os.unlink(t.name)
        im = Image.open(png).convert("RGBA")
        box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        im.crop(box).save(png); print(os.path.basename(png), im.crop(box).size)


if __name__ == "__main__":
    os.makedirs(TEX, exist_ok=True); os.makedirs(CARDS, exist_ok=True)
    wallpaper()
    wood(1024, "#A8723F", 8, "floor.png")
    wood(512, "#D19A62", 3, "trim.png", plank_gap=False)
    fabric(1024, "#5E9E9A", "curtain.png", folds=9)
    fabric(512, "#E58B7B", "cushion.png")
    sky("sky_day.png", "#6FB8EA", "#D3ECF8", "#FFFFFF", "#D6E4F2")
    sky("sky_dawn.png", "#8FA6D6", "#F6C9A8", "#FFF2E6", "#E7C6C8", n_clouds=5, glow=(0.62, 0.95, "#FFE2B8"))
    globe(); rock(); rug()
    plain("brass.png", "#C9A04E", amt=0.25)
    plain("toy_red.png", "#D9564A"); plain("toy_cream.png", "#F6E7C8")
    plain("ceiling.png", "#F6EBD6", scale=200, amt=0.1, n_strokes=120)
    picture()
    plain("pot.png", "#C9734A"); plain("leaf.png", "#5E9A4E", amt=0.3, stroke_ang=60)
    if os.environ.get('ONLY_RENDER_CARDS'):
        cut_cards(); counter_cards()
    elif os.environ.get('ONLY_PROPS'):
        prop_textures(); cut_props()
    else:
        cut_cards() if os.environ.get('ONLY_CARDS') else (kid_cards(), sets_textures(), prop_textures(), cut_props())
