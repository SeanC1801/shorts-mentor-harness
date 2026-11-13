"""LOOK TEST (2026-11-13, not an approved style): 3D characters and a flat two-tone environment.

Builds a plain studio (turnaround, faces, poses, variants) and a small outdoor set (house, tree, fence, hills)
lit three ways (day, sunset, night), then writes stills. Compare with visual-style v3 (painted sets, cutout cards).

usage: blender -b -P renderer-blender/lookdev_3d_style.py -- OUT_DIR [scale%] [--only name,name]
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import papercraft as pc
pc.CEL = True
import toon3d as t3
from toon3d import flat, lathe, ball, tube, kid

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/lookdev3d"]
OUT = argv[0]
SCALE = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 100
ONLY = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
sc = pc.setup(SCALE, samples=32)
cam, aim = pc.camera()
V = Vector
rnd = random.Random(5)
pc.G_SAT.outputs[0].default_value = 1.0
HERO = dict(skin="#F4EFE6", top="#F2B10C", bottom="#2E6FD1", shoes="#C9482F", hair="#4A2C1A")
FRIEND = dict(skin="#C98F62", top="#3FA58C", bottom="#3B3F5C", shoes="#F2F2F2", hair=None, hat="#D9483B")
CHARS = {}


def put(key, O, **kw):
    cfg = dict(HERO); cfg.update(kw)
    root, parts = kid(key, O, **cfg)
    CHARS[key] = [root] + parts
    return root


def box(name, c, size, color, bevel=0.0, rot=(0, 0, 0)):
    return pc.box(name, V(c), size, flat(color), bevel, rot)


# ---------------- studio: a floor and one tall step, so two rows of figures fit a vertical frame ----------------
ST = pc.collection("STUDIO")
SO = V((200, 0, 0))
pc.plane("studio_floor", SO + V((0, 20, 0)), (80, 80), (0, 0, 0), flat("#E7DFCF"))
for k in range(3):
    box("studio_step", SO + V((k * 20, 2.2, 0.75)), (6.0, 1.6, 1.5), "#D9CFBB")
box("studio_wall", SO + V((20, 9, 6)), (90, 0.4, 14), "#EFE9DC")
# turnaround
for i, turn in enumerate((0, 40, 90, 180)):
    put(f"turn{i}", SO + V((-60 + (i % 2) * 1.0 - 0.5, 0.2 if i < 2 else 2.0, 0 if i < 2 else 1.5)), turn=turn)
box("studio_step", SO + V((-60, 2.2, 0.75)), (6.0, 1.6, 1.5), "#D9CFBB")
# faces (busts, two rows of three)
for i, f in enumerate(("neutral", "happy", "surprised", "worried", "deadpan", "squint")):
    put("face_" + f, SO + V((-0.62 + (i % 3) * 0.62, 0.3 if i < 3 else 1.9, 0 if i < 3 else 1.5)), face=f)
# poses (two rows of three)
for i, (ps, f) in enumerate((("stand", "neutral"), ("wave", "happy"), ("point_up", "surprised"), ("shock", "surprised"), ("shrug", "deadpan"), ("think", "worried"))):
    put("pose_" + ps, SO + V((20 - 0.85 + (i % 3) * 0.85, 0.3 if i < 3 else 2.0, 0 if i < 3 else 1.5)), pose=ps, face=f)
put("pose_walk", SO + V((20 - 1.7, 0.3, 0)), pose="walk", face="happy", turn=-55)
put("pose_shield", SO + V((20 + 1.7, 0.3, 0)), pose="shield", face="squint")
# variants (two rows of two)
VAR = [dict(), dict(skin="#C98F62", hair="#1E1B22", top="#3FA58C", bottom="#3B3F5C", shoes="#F2F2F2"),
       dict(skin="#8A5A3C", hair=None, hat="#D9483B", top="#3D7BE0", bottom="#F0A23C", shoes="#2B2B33"),
       dict(skin="#F4EFE6", hair=None, hat="#3FA58C", top="#EE6F4E", bottom="#4A4E5A", shoes="#F2B10C")]
for i, cfg in enumerate(VAR):
    put(f"var{i}", SO + V((40 - 0.45 + (i % 2) * 0.9, 0.3 if i < 2 else 2.0, 0 if i < 2 else 1.5)), face=("happy", "neutral", "deadpan", "surprised")[i],
        pose=("wave", "stand", "shrug", "point_up")[i], **cfg)

# ---------------- outdoor set ----------------
EN = pc.collection("ENV")
pc.plane("ground", V((0, 60, 0)), (400, 400), (0, 0, 0), flat("#63BE4E"))
for x, y, r, col, sq in ((-40, 95, 34, "#4FA94A", 0.42), (30, 110, 44, "#57B056", 0.36), (95, 150, 60, "#5FB7A0", 0.34), (-110, 160, 70, "#6BBFAE", 0.3)):
    ball("hill", V((x, y, -r * sq * 0.35)), r, flat(col), scale=(1.5, 1, sq))
path = [(0.4, -6), (0.2, 0), (-0.2, 4), (0.6, 8), (2.4, 10.5), (3.4, 12)]
pc.strip("path", [V((x, y, 0.012)) for x, y in path], [1.5, 1.4, 1.3, 1.2, 1.1, 1.0], flat("#E9C98A"))
H = V((3.6, 14.2, 0))
box("house", H + V((0, 0, 1.55)), (5.2, 4.2, 3.1), "#F6DFA6", 0.04)
pc.wedge("roof", H + V((0, 0, 3.1)), 5.0, 1.8, 5.8, flat("#D8503F"), bevel=0.05)
box("chimney", H + V((1.5, 0.6, 4.2)), (0.6, 0.6, 1.6), "#B9684A", 0.03)
box("door", H + V((-0.2, -2.12, 1.0)), (0.95, 0.1, 2.0), "#7A4A2B", 0.03)
ball("knob", H + V((0.12, -2.19, 1.0)), 0.05, flat("#F2C84B"))
box("step", H + V((-0.2, -2.45, 0.08)), (1.5, 0.6, 0.16), "#CFC7B6", 0.02)
WINDOWS = []
for wx in (-1.75, 1.45):
    box("window_frame", H + V((wx, -2.11, 1.75)), (1.15, 0.1, 1.15), "#FFFFFF", 0.02)
    WINDOWS.append(pc.box("window_pane", H + V((wx, -2.15, 1.75)), (0.92, 0.06, 0.92), flat("#A9D8F0")))
    box("window_bar", H + V((wx, -2.19, 1.75)), (0.06, 0.03, 0.92), "#FFFFFF")
    box("window_bar", H + V((wx, -2.19, 1.75)), (0.92, 0.03, 0.06), "#FFFFFF")
    box("planter", H + V((wx, -2.3, 1.08)), (1.2, 0.3, 0.22), "#B9684A", 0.03)
    for k in range(5):
        ball("planter_flower", H + V((wx - 0.45 + k * 0.225, -2.32, 1.27)), 0.085, flat(("#F27BA0", "#FFFFFF", "#F2C84B")[k % 3]))


def tree(c, h=3.0, r=1.5, col="#3F9E52", col2="#56B95F"):
    c = V(c)
    tube("trunk", [c, c + V((0.05, 0, h * 0.55)), c + V((0, 0, h))], 0.26, flat("#8A5A35"), r_end=0.18, sides=14)
    for dx, dy, dz, k, cc in ((0, 0, 0.5, 1.0, col), (-0.75, 0.1, 0.0, 0.72, col), (0.8, -0.1, 0.1, 0.76, col), (0.15, -0.2, 1.15, 0.7, col2)):
        ball("crown", c + V((dx * r, dy * r, h + dz * r)), r * k, flat(cc), scale=(1, 1, 0.92))


tree((-3.4, 11.5, 0), 3.0, 1.6)
tree((9.5, 22, 0), 3.6, 1.9, "#3A9450", "#4FAE5A")
tree((-12, 30, 0), 4.2, 2.3)
for bx, by, n in ((-0.9, 12.6, 3), (7.0, 12.4, 4), (-7.5, 14.5, 3)):
    for k in range(n):
        ball("bush", V((bx + k * 0.62 - n * 0.3, by + rnd.uniform(-0.2, 0.2), 0.3 + 0.12 * (k % 2))), rnd.uniform(0.42, 0.58), flat("#4BAA55"), scale=(1.1, 1, 0.85))
for k in range(13):                       # picket fence on the left, with two rails
    x = -8.2 + k * 0.55
    box("picket", V((x, 9.2, 0.45)), (0.16, 0.06, 0.9), "#FBF6EA", 0.02)
for zz in (0.3, 0.68):
    box("rail", V((-4.9, 9.25, zz)), (7.2, 0.04, 0.09), "#FBF6EA")
box("mail_post", V((1.5, 5.4, 0.5)), (0.1, 0.1, 1.0), "#8A5A35")
box("mailbox", V((1.5, 5.4, 1.1)), (0.34, 0.55, 0.3), "#D8503F", 0.05)
for x, y, r in ((-2.2, 5.6, 0.22), (2.6, 7.4, 0.3), (-5.0, 7.8, 0.36), (4.4, 4.6, 0.18)):
    ball("rock", V((x, y, r * 0.3)), r, flat("#A4ADB8"), scale=(1.3, 1, 0.65))
for k in range(26):
    x, y = rnd.uniform(-7, 7), rnd.uniform(2.5, 12)
    if abs(x - 0.2) < 1.2 or (1.0 < x < 6.4 and y > 11):
        continue
    ball("flower", V((x, y, 0.07)), 0.06, flat(("#F27BA0", "#FFFFFF", "#F2C84B", "#B58CF2")[k % 4]), scale=(1, 1, 0.7))
CLOUDS = []
for cx, cy, cz, s in ((-22, 120, 34, 6.0), (18, 140, 46, 7.5), (48, 110, 26, 5.0), (-55, 150, 52, 8.0), (4, 170, 70, 9.0)):
    for dx, dz, k in ((0, 0, 1.0), (-1.2, -0.15, 0.7), (1.25, -0.1, 0.78), (0.4, 0.5, 0.62)):
        CLOUDS.append(ball("cloud", V((cx + dx * s, cy, cz + dz * s)), s * k, flat("#FFFFFF"), scale=(1.25, 1, 0.72)))
SUN_DISC = ball("sun_disc", V((60, 330, 60)), 15, pc.emit("#FFF2B8", 1.0))
MOON = ball("moon", V((-55, 330, 130)), 11, pc.emit("#F6F2DC", 1.6))
STARS = []
for k in range(90):
    a, el = rnd.uniform(-1.2, 1.2), rnd.uniform(0.12, 1.2)
    STARS.append(ball("star", V((math.sin(a) * math.cos(el), math.cos(a) * math.cos(el), math.sin(el))) * 420, rnd.uniform(0.5, 1.2), pc.emit("#FFFFFF", 2.6)))
SUN = pc.light("sun", "SUN", V((0, 0, 20)), 4.0, "#FFFFFF", angle=1.5)
EN.objects.unlink(SUN); sc.collection.objects.link(SUN)      # the sun lights the studio too, so it lives outside ENV
# outdoor characters (several share a spot; each still shows the ones it names)
A = V((-0.6, 6.5, 0))
put("a_wave", A, pose="wave", face="happy", turn=8)
put("a_close", A, pose="stand", face="happy")
put("a_point", A, pose="point_up", face="surprised")
put("a_think", A + V((-0.35, 0, 0)), pose="think", face="worried", turn=-18)
put("b_shrug", A + V((0.55, 0.15, 0)), pose="shrug", face="deadpan", turn=22, **FRIEND)
put("a_walk", V((0.2, 4.6, 0)), pose="walk", face="happy", turn=160)
put("b_stand", V((1.4, 7.6, 0)), pose="wave", face="happy", turn=-150, **FRIEND)
BX = V((-4.2, 7.4, 0))
put("a_shock", BX, pose="shock", face="surprised")
put("a_shield", A, pose="shield", face="squint", turn=-10)
put("a_night", V((2.3, 10.6, 0)), pose="stand", face="worried", turn=25)
put("a_stand", A, pose="stand", face="neutral")


def to_dir(v):
    return tuple(V(v).normalized().to_track_quat("Z", "Y").to_euler())


def state(name):
    """Lighting and colour state: sky gradient, sun, shadow tint, grade, window glow."""
    day, sunset, night, studio = name == "day", name == "sunset", name == "night", name == "studio"
    cfg = {"day": ("#2F86E6", "#BFE6F7", "#63BE4E", (-0.30, -0.62, 0.72), 4.0, (0.56, 0.60, 0.92), "#FFFFFF", 1.0),
           "sunset": ("#5A4AA6", "#FF9E7A", "#63BE4E", (-0.45, -0.70, 0.36), 3.4, (0.60, 0.44, 0.78), "#FFD9C4", 1.05),
           "night": ("#0A0F33", "#2B3F8C", "#1C3A4A", (0.5, -0.45, 0.74), 2.2, (0.52, 0.56, 0.86), "#8E9EF2", 1.0),
           "studio": ("#EFE9DC", "#EFE9DC", "#E7DFCF", (-0.30, -0.62, 0.72), 4.0, (0.62, 0.62, 0.86), "#FFFFFF", 1.0)}[name]
    zen, hor, gnd, sdir, energy, tint, grade, sat = cfg
    t3.sky(zen, hor, gnd)
    SUN.rotation_euler = to_dir(sdir); SUN.data.energy = energy
    t3.set_shade(tint, t3.AMBIENT + 0.2 * energy / math.pi)
    pc.G_RGB.outputs[0].default_value = pc.hexcol(grade); pc.G_SAT.outputs[0].default_value = sat
    for w in WINDOWS:
        w.data.materials[0] = flat("#A9D8F0") if (day or studio) else pc.emit("#FFD98A", 1.1 if sunset else 3.2)
    SUN_DISC.hide_render = not sunset
    SUN_DISC.location = V((-70, 330, 30))
    MOON.hide_render = not night
    for s in STARS:
        s.hide_render = not night
    for c in CLOUDS:
        c.data.materials[0] = flat({"day": "#FFFFFF", "sunset": "#FFC9B0", "night": "#3C4C96", "studio": "#FFFFFF"}[name])


S3 = SO
STILLS = [   # name, state, characters shown, camera position, aim, lens (mm), f-stop
    ("01-turnaround", "studio", ["turn0", "turn1", "turn2", "turn3"], S3 + V((-60, -5.6, 1.7)), S3 + V((-60, 1.0, 1.45)), 50, 16),
    ("02-faces", "studio", ["face_neutral", "face_happy", "face_surprised", "face_worried", "face_deadpan", "face_squint"], S3 + V((0, -5.0, 1.85)), S3 + V((0, 1.0, 1.72)), 38, 16),
    ("03-poses", "studio", ["pose_stand", "pose_wave", "pose_point_up", "pose_shock", "pose_shrug", "pose_think"], S3 + V((20, -6.6, 1.7)), S3 + V((20, 1.0, 1.5)), 36, 16),
    ("04-more-poses", "studio", ["pose_walk", "pose_shield", "pose_wave"], S3 + V((20, -5.2, 0.9)), S3 + V((20, 0.3, 0.72)), 50, 16),
    ("05-variants", "studio", ["var0", "var1", "var2", "var3"], S3 + V((40, -5.4, 1.7)), S3 + V((40, 1.0, 1.5)), 42, 16),
    ("06-day-wide", "day", ["a_wave"], V((-1.6, -3.6, 1.7)), V((1.0, 12, 1.9)), 24, 11),
    ("07-day-medium", "day", ["a_wave"], V((-1.1, 3.3, 0.95)), V((-0.6, 6.5, 0.8)), 35, 5.6),
    ("08-day-closeup", "day", ["a_close"], V((-0.95, 5.0, 1.02)), V((-0.6, 6.5, 0.98)), 55, 2.0),
    ("09-day-low-angle", "day", ["a_point"], V((-0.2, 5.2, 0.22)), V((-0.6, 6.5, 0.95)), 24, 8),
    ("10-day-high-angle", "day", ["a_walk", "b_stand"], V((-2.4, 1.6, 4.8)), V((0.6, 6.6, 0.4)), 28, 8),
    ("11-day-two-characters", "day", ["a_think", "b_shrug"], V((-0.5, 3.5, 0.95)), V((-0.65, 6.55, 0.78)), 35, 5.6),
    ("12-outline-test-wide", "day", ["a_shock"], V((-3.6, 3.4, 0.9)), V((-4.2, 7.4, 0.85)), 28, 11),
    ("13-outline-test-zoomed", "day", ["a_shock"], V((-3.6, 3.4, 0.9)), V((-4.2, 7.4, 0.95)), 62, 11),
    ("14-sunset-wide", "sunset", ["a_walk"], V((-3.4, -3.0, 1.5)), V((1.2, 12, 2.2)), 24, 11),
    ("15-sunset-medium", "sunset", ["a_shield"], V((-1.5, 3.4, 0.9)), V((-0.6, 6.5, 0.85)), 35, 5.6),
    ("16-night-wide", "night", ["a_stand"], V((-1.6, -3.6, 1.7)), V((1.0, 12, 2.1)), 24, 11),
    ("17-night-medium", "night", ["a_night"], V((1.5, 7.5, 0.95)), V((2.3, 10.6, 0.82)), 35, 4),
]

pc.cel_ink(sc)
os.makedirs(OUT, exist_ok=True)
for name, st, chars, cpos, apos, lens, fstop in STILLS:
    if ONLY and not any(k in name for k in ONLY):
        continue
    state(st)
    ST.hide_render, EN.hide_render = st != "studio", st == "studio"
    for key, objs in CHARS.items():
        for o in objs:
            o.hide_render = key not in chars
    cam.location, aim.location, cam.data.lens = V(cpos), V(apos), lens
    cam.data.dof.aperture_fstop = fstop
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("STILL", name, flush=True)
