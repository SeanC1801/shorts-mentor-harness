"""Finish EP003: transitions between views (whip, dissolve, follow/push), fade in/out,
word-by-word captions (motion rules v2), then encode the preview with narration and one MP4 per shot.

usage: python3 -I finish_ep003.py FRAME_DIR OUT_DIR            # whole preview + every shot
       python3 -I finish_ep003.py FRAME_DIR OUT_DIR S01 S02    # only these shots, each with its narration slice
"""
import json, os, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EP = os.path.join(ROOT, "EPISODES/EP003")
FPS, N = 30, 1575
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", 60)   # ~42 px glyphs at 1920
CAP_Y = 1270
# view starts and the join used to enter each view (from storyboard v2; same table as ep003_render.py)
STARTS = [0, 60, 112, 162, 215, 265, 313, 350, 385, 435, 487, 530, 573, 620, 671, 705, 737, 800, 849, 905, 983, 1035, 1080, 1122, 1189, 1250, 1306, 1371, 1414, 1460, 1511]
JOINS = ["fade-in", "push", "push", "follow", "whip", "follow", "whip", "follow", "push", "follow", "whip", "follow", "whip", "push", "follow", "dissolve", "dissolve", "whip", "whip", "follow", "follow", "follow", "push", "dissolve", "follow", "follow", "dissolve", "dissolve", "dissolve", "dissolve", "whip"]


def words():
    W = json.load(open(os.path.join(EP, "audio/word-timings-v2.json")))
    out = []
    for k in sorted(W["sentences"], key=lambda s: int(s[1:])):
        out += [(round(w["startMs"] * FPS / 1000), w["text"]) for w in W["sentences"][k]]
    return out


WORDS = words()


def caption(im, f):
    cur = [w for w in WORDS if w[0] <= f]
    if not cur or f > round(52400 * FPS / 1000):
        return im
    start, text = cur[-1]
    pop = min(1.0, 0.86 + 0.14 * (f - start) / 3)
    d = ImageDraw.Draw(im)
    w, h = d.textbbox((0, 0), text, font=FONT, stroke_width=6)[2:]
    tmp = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((20, 20), text, font=FONT, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(20, 33, 61, 255))
    sh = Image.new("RGBA", tmp.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((20, 26), text, font=FONT, fill=(0, 0, 0, 110), stroke_width=6, stroke_fill=(0, 0, 0, 110))
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


def finish_frames(src, tmpdir, lo, hi):
    """Write finished frames lo..hi-1; joins that reach outside the range hold the edge frame."""
    load = lambda f: np.asarray(Image.open(os.path.join(src, f"f_{min(hi - 1, max(lo, f)):04d}.png")).convert("RGB"))
    trans = {}
    for b, j in zip(STARTS[1:], JOINS[1:]):
        trans[b] = j
    for f in range(lo, hi):
        img = load(f).astype(np.float32)
        for b, j in trans.items():
            d = f - b   # frames relative to the cut
            if j == "whip" and -3 <= d <= 2:
                strength = 140 * (1 - abs(d + 0.5) / 3.5)
                img = hblur(img.astype(np.uint8), strength).astype(np.float32)
                if d in (-1, 0):
                    other = hblur(load(b if d == -1 else b - 1), strength).astype(np.float32)
                    img = img * 0.6 + other * 0.4
            elif j == "dissolve" and -3 <= d <= 2:
                w = (d + 3.5) / 6   # 0 -> 1 across the cut
                A = load(min(f, b - 1)).astype(np.float32); Bf = load(max(f, b)).astype(np.float32)
                img = A * (1 - w) + Bf * w
            elif j in ("follow", "push") and -1 <= d <= 1:
                w = (d + 1.5) / 3
                A = load(min(f, b - 1)).astype(np.float32); Bf = load(max(f, b)).astype(np.float32)
                img = A * (1 - w) + Bf * w
        if f < 8:
            img *= (f + 1) / 9
        if f >= N - 15:
            img *= (N - f) / 16
        im = caption(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)), f)
        im.save(os.path.join(tmpdir, f"c_{f:04d}.png"))
        if f % 100 == 0:
            print("finished frame", f, flush=True)


def scene_clips(src, out, ids):
    """One reviewable MP4 per shot, with captions and its slice of the narration."""
    ff = shutil.which("ffmpeg")
    audio = os.path.join(EP, "audio/EP003-narration-v2.mp3")
    ep = json.load(open(os.path.join(EP, "episode.json")))
    os.makedirs(os.path.join(out, "scenes"), exist_ok=True)
    for s in ep["shots"]:
        if s["shotId"] not in ids:
            continue
        a, b = s["startFrame"], s["endFrame"]
        tmpdir = tempfile.mkdtemp(prefix="ep003_scene_")
        finish_frames(src, tmpdir, a, b)
        clip = os.path.join(out, "scenes", f"EP003-{s['shotId']}.mp4")
        subprocess.run([ff, "-v", "error", "-y", "-framerate", str(FPS), "-start_number", str(a), "-i", os.path.join(tmpdir, "c_%04d.png"),
                        "-ss", f"{a / FPS:.3f}", "-t", f"{(b - a) / FPS:.3f}", "-i", audio, "-frames:v", str(b - a),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", clip], check=True)
        shutil.rmtree(tmpdir)
        print("WROTE", clip)


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    if len(sys.argv) > 3:
        return scene_clips(src, out, sys.argv[3:])
    tmpdir = tempfile.mkdtemp(prefix="ep003_finish_")
    finish_frames(src, tmpdir, 0, N)
    ff = shutil.which("ffmpeg")
    audio = os.path.join(EP, "audio/EP003-narration-v2.mp3")
    preview = os.path.join(out, "EP003-preview.mp4")
    subprocess.run([ff, "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmpdir, "c_%04d.png"), "-i", audio,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-shortest", preview], check=True)
    ep = json.load(open(os.path.join(EP, "episode.json")))
    os.makedirs(os.path.join(out, "scenes"), exist_ok=True)
    for s in ep["shots"]:
        a, b = s["startFrame"], s["endFrame"]
        subprocess.run([ff, "-v", "error", "-y", "-framerate", str(FPS), "-start_number", str(a), "-i", os.path.join(tmpdir, "c_%04d.png"),
                        "-frames:v", str(b - a), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", os.path.join(out, "scenes", f"EP003-{s['shotId']}.mp4")], check=True)
    shutil.rmtree(tmpdir)
    print("WROTE", preview)


if __name__ == "__main__":
    main()
