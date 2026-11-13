"""Shared finish step: joins between views, optional fades, word-by-word captions, then one MP4 per shot or the full
preview with narration. Everything it needs comes from the episode's timing file (see ../timing.py).

usage: python3 -I renderer-blender/scripts/finish_episode.py TIMING FRAMES_DIR OUT_DIR S01 [S02 ...]   # scene clips
       python3 -I renderer-blender/scripts/finish_episode.py TIMING FRAMES_DIR OUT_DIR --preview       # the whole episode

Scene clips go to OUT_DIR/scenes/. The preview goes to OUT_DIR/preview/ and never touches the scene clips.
Settings in the timing file's "finish": fadeIn, fadeOut, captions, captionPx.
"""
import os, shutil, subprocess, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import timing

CAP_Y = 1270          # caption centre, about 66% down a 1920 frame
FONT_FILE = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def caption(im, f, T, font):
    cur = [w for w in T["words"] if w[0] <= f]
    if not cur:
        return im
    start, text = cur[-1]
    pop = min(1.0, 0.86 + 0.14 * (f - start) / 3)
    edge = max(4, font.size // 10)
    d = ImageDraw.Draw(im)
    w, h = d.textbbox((0, 0), text, font=font, stroke_width=edge)[2:]
    tmp = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((20, 20), text, font=font, fill=(255, 255, 255, 255), stroke_width=edge, stroke_fill=(20, 33, 61, 255))
    sh = Image.new("RGBA", tmp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((20, 26), text, font=font, fill=(0, 0, 0, 110), stroke_width=edge, stroke_fill=(0, 0, 0, 110))
    tmp = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), tmp)
    if pop < 1:
        tmp = tmp.resize((max(1, int(tmp.width * pop)), max(1, int(tmp.height * pop))), Image.LANCZOS)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    layer.alpha_composite(tmp, (im.width // 2 - tmp.width // 2, CAP_Y - tmp.height // 2))
    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")


def hblur(arr, px):
    """Horizontal motion blur (whip) by averaging shifted copies."""
    if px < 1:
        return arr
    n = max(2, int(px // 4))
    acc = np.zeros_like(arr, dtype=np.float32)
    for k in range(n):
        acc += np.roll(arr, int(-px / 2 + px * k / (n - 1)), axis=1)
    return (acc / n).astype(np.uint8)


def finish_frames(job):
    """Write finished frames a..b-1 of the range lo..hi; joins that reach outside lo..hi hold the edge frame."""
    path, src, tmpdir, lo, hi, a, b = job
    T = timing.load(path)
    font = ImageFont.truetype(FONT_FILE, T["finish"]["captionPx"])
    N = T["total"]
    load = lambda f: np.asarray(Image.open(os.path.join(src, f"f_{min(hi - 1, max(lo, f)):04d}.png")).convert("RGB"))
    joins = {v["start"]: v["join"] for v in T["views"] if v["start"] > 0}
    for f in range(a, b):
        img = load(f).astype(np.float32)
        for cut, j in joins.items():
            d = f - cut
            if j == "whip" and -3 <= d <= 2:
                strength = 140 * (1 - abs(d + 0.5) / 3.5)
                img = hblur(img.astype(np.uint8), strength).astype(np.float32)
                if d in (-1, 0):
                    other = hblur(load(cut if d == -1 else cut - 1), strength).astype(np.float32)
                    img = img * 0.6 + other * 0.4
            elif j == "dissolve" and -3 <= d <= 2:
                w = (d + 3.5) / 6
                img = load(min(f, cut - 1)).astype(np.float32) * (1 - w) + load(max(f, cut)).astype(np.float32) * w
            elif j in ("follow", "push") and -1 <= d <= 1:
                w = (d + 1.5) / 3
                img = load(min(f, cut - 1)).astype(np.float32) * (1 - w) + load(max(f, cut)).astype(np.float32) * w
        if T["finish"]["fadeIn"] and f < 8:
            img *= (f + 1) / 9
        if T["finish"]["fadeOut"] and f >= N - 15:
            img *= (N - f) / 16
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        if T["finish"]["captions"]:
            im = caption(im, f, T, font)
        im.save(os.path.join(tmpdir, f"c_{f:04d}.png"))
    return b - a


def finish_range(path, src, tmpdir, lo, hi, workers=6):
    step = max(20, (hi - lo + workers - 1) // workers)
    jobs = [(path, src, tmpdir, lo, hi, a, min(hi, a + step)) for a in range(lo, hi, step)]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return sum(ex.map(finish_frames, jobs))


def encode(T, tmpdir, a, b, out):
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(T["fps"]), "-start_number", str(a), "-i", os.path.join(tmpdir, "c_%04d.png")]
    if T["audio"]:
        cmd += ["-ss", f"{a / T['fps']:.3f}", "-t", f"{(b - a) / T['fps']:.3f}", "-i", T["audio"]]
    cmd += ["-frames:v", str(b - a), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18"]
    if T["audio"]:
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    subprocess.run(cmd + [out], check=True)
    print("WROTE", out, flush=True)


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    path, src, out, what = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    T = timing.load(path)
    if what == ["--preview"]:
        ranges = [("preview", 0, T["total"], os.path.join(out, "preview", f"{T['id']}-preview.mp4"))]
    else:
        ranges = [(s, timing.shot(T, s)["start"], timing.shot(T, s)["end"], os.path.join(out, "scenes", f"{T['id']}-{s}.mp4")) for s in what]
    for name, a, b, target in ranges:
        miss = [f for f in range(a, b) if not os.path.exists(os.path.join(src, f"f_{f:04d}.png"))]
        if miss:
            sys.exit(f"finish_episode: {name} is missing {len(miss)} rendered frames (first {miss[0]}) in {src}")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        tmpdir = tempfile.mkdtemp(prefix="finish_")
        finish_range(T["path"], src, tmpdir, a, b)
        encode(T, tmpdir, a, b, target)
        shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
