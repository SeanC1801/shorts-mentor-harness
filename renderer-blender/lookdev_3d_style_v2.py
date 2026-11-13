"""LOOK TEST v2 (2026-11-13): 3D characters in dense, dressed sets with mood lighting.

After the creator approved look test v1 as the direction and asked for a comparison with Ricks Clips: this round
tries what that comparison showed (sets full of story props and readable signs; warm practical lights, glow, striped
window light, depth blur; a slimmer bean-bodied figure with a wider range of faces) and fixes v1's known flaws
(muddy shadow on the face, low contrast on dark skin, flat bright daylight). Characters stay the channel's own kid.

usage: blender -b -P renderer-blender/lookdev_3d_style_v2.py -- OUT_DIR [scale%] [--only name,name]
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import papercraft as pc
pc.CEL = True
import toon3d as t3
from toon3d import flat, lathe, ball, tube, kid, sign
import toon_sets
from toon_sets import B, E, lamp, to_dir

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/lookdev3d-v2"]
OUT = argv[0]
SCALE = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 100
ONLY = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
sc = pc.setup(SCALE, samples=32)
cam, aim = pc.camera()
V = Vector
rnd = random.Random(9)
t3.SKIN_SOFT = 0.45
t3.glow(sc, strength=0.4, threshold=1.0, size=0.5, vignette=0.35)
HERO = dict(skin="#F4EFE6", top="#F2B10C", bottom="#2E6FD1", shoes="#C9482F", hair="#4A2C1A", build="bean")
FRIEND = dict(skin="#C98F62", top="#3FA58C", bottom="#3B3F5C", shoes="#F2F2F2", hair=None, hat="#D9483B", build="bean")
CHARS = {}
SUN = pc.light("sun", "SUN", V((0, 0, 20)), 4.0, "#FFFFFF", angle=1.2)


def put(key, O, **kw):
    cfg = dict(HERO); cfg.update(kw)
    root, parts = kid(key, O, **cfg)
    CHARS[key] = [root] + parts
    return root


# ================= studio =================
ST = pc.collection("STUDIO")
SO = V((300, 0, 0))
pc.plane("studio_floor", SO + V((0, 20, 0)), (120, 80), (0, 0, 0), flat("#E7DFCF"))
for x in (-40, 20, 40):
    B("studio_step", SO + V((x, 2.2, 0.75)), (6.0, 1.6, 1.5), "#D9CFBB")
for k in (1, 2):                                     # stairs for the three rows of faces
    B("studio_stair", SO + V((0, 0.55 * k + 0.72, 0.8 * k - 0.4)), (4.0, 2.0, 0.8), "#D9CFBB")
B("studio_wall", SO + V((0, 9, 6)), (140, 0.4, 14), "#EFE9DC")
# builds: v1 "classic" beside v2 "bean", front and three-quarter
for i, (bd, turn) in enumerate((("classic", 0), ("bean", 0), ("classic", 40), ("bean", 40))):
    put(f"build{i}", SO + V((-40 - 0.5 + (i % 2) * 1.0, 0.3 if i < 2 else 2.0, 0 if i < 2 else 1.5)), build=bd, turn=turn, face="happy" if bd == "bean" else "neutral")
# nine faces, three rows of three
FACES = ("neutral", "happy", "laugh", "surprised", "worried", "nervous", "deadpan", "smug", "squint")
for i, f in enumerate(FACES):
    put("face_" + f, SO + V((-0.5 + (i % 3) * 0.5, 0.55 * (i // 3), 0.8 * (i // 3))), face=f)
# poses (bean)
for i, (ps, f) in enumerate((("stand", "neutral"), ("wave", "happy"), ("point_up", "surprised"), ("shock", "nervous"), ("shrug", "smug"), ("think", "worried"))):
    put("pose_" + ps, SO + V((20 - 0.85 + (i % 3) * 0.85, 0.3 if i < 3 else 2.0, 0 if i < 3 else 1.5)), pose=ps, face=f)
# skin and outfit variants (bean)
VAR = [dict(), dict(skin="#C98F62", hair="#1E1B22", top="#3FA58C", shoes="#F2F2F2"),
       dict(skin="#8A5A3C", hair=None, hat="#D9483B", top="#3D7BE0", shoes="#2B2B33"),
       dict(skin="#E8B890", hair="#B5532A", top="#B56FE0", shoes="#F2B10C")]
for i, cfg in enumerate(VAR):
    put(f"var{i}", SO + V((40 - 0.45 + (i % 2) * 0.9, 0.3 if i < 2 else 2.0, 0 if i < 2 else 1.5)), face=("happy", "smug", "laugh", "surprised")[i],
        pose=("wave", "stand", "shrug", "point_up")[i], **cfg)

# ================= set A: the workshop (interior, warm) =================
WS = toon_sets.workshop()
# characters in the workshop
WA = V((0.25, 1.45, 0))
put("w_think", WA, pose="think", face="worried", turn=-14)
put("w_smug", WA, pose="stand", face="smug", turn=10)
put("w_point", WA, pose="point_up", face="surprised")
put("w_shock", WA + V((0.1, 0.3, 0)), pose="shock", face="nervous", turn=-8)
put("w_friend", WA + V((-0.95, -0.15, 0)), pose="wave", face="laugh", turn=28, **{k: v for k, v in FRIEND.items() if k != "build"})
put("w_friend_shrug", WA + V((-0.8, -0.1, 0)), pose="shrug", face="deadpan", turn=20, **{k: v for k, v in FRIEND.items() if k != "build"})

# ================= set B: the street at night =================
SR = toon_sets.street()
# characters on the street
SA = V((-2.9, 5.2, 0.14))
put("s_lamp", SA, pose="stand", face="neutral", turn=14)
put("s_wave", SA, pose="wave", face="happy", turn=10)
put("s_close", V((-2.4, 5.5, 0.14)), pose="stand", face="surprised", turn=35)
put("s_back", V((2.6, 7.9, 0.14)), pose="stand", face="neutral", turn=172)
put("s_point", V((-1.7, 7.0, 0.14)), pose="point_up", face="laugh", turn=-12, **{k: v for k, v in FRIEND.items() if k != "build"})
put("s_vend_a", V((-0.62, 7.75, 0.14)), pose="think", face="worried", turn=40)
put("s_vend_b", V((1.12, 7.6, 0.14)), pose="shrug", face="smug", turn=-40, **{k: v for k, v in FRIEND.items() if k != "build"})


def state(name):
    toon_sets.state(name, SUN)

S3 = SO
STILLS = [   # name, state, collection, characters, camera position, aim, lens, f-stop
    ("01-builds-v1-and-v2", "studio", ST, ["build0", "build1", "build2", "build3"], S3 + V((-40, -5.4, 1.7)), S3 + V((-40, 1.0, 1.5)), 42, 16),
    ("02-nine-faces", "studio", ST, ["face_" + f for f in FACES], S3 + V((0, -6.4, 1.9)), S3 + V((0, 0.5, 1.68)), 50, 16),
    ("03-poses", "studio", ST, ["pose_stand", "pose_wave", "pose_point_up", "pose_shock", "pose_shrug", "pose_think"], S3 + V((20, -6.6, 1.7)), S3 + V((20, 1.0, 1.5)), 36, 16),
    ("04-skin-and-outfits", "studio", ST, ["var0", "var1", "var2", "var3"], S3 + V((40, -5.4, 1.7)), S3 + V((40, 1.0, 1.5)), 42, 16),
    ("05-workshop-wide", "warm", WS, ["w_think", "w_friend"], V((0.5, -3.6, 1.5)), V((0.2, 2.6, 1.25)), 22, 11),
    ("06-workshop-medium", "warm", WS, ["w_think"], V((-0.7, -0.9, 1.1)), V((0.3, 1.6, 0.95)), 30, 5.6),
    ("07-workshop-closeup", "warm", WS, ["w_smug"], V((-0.45, -0.35, 1.05)), V((0.25, 1.45, 0.96)), 50, 2.0),
    ("08-workshop-prop-insert", "warm", WS, [], V((0.15, 1.25, 1.3)), V((0.5, 2.6, 1.12)), 40, 2.8),
    ("09-workshop-low-angle", "warm", WS, ["w_point"], V((0.95, 0.25, 0.3)), V((0.25, 1.45, 1.1)), 22, 8),
    ("10-workshop-two-characters", "warm", WS, ["w_shock", "w_friend_shrug"], V((-0.3, -1.1, 1.0)), V((-0.2, 1.5, 0.85)), 32, 5.6),
    ("11-workshop-high-angle", "warm", WS, ["w_think", "w_friend"], V((1.7, -0.9, 2.8)), V((0.0, 1.7, 0.3)), 22, 8),
    ("12-street-wide", "night", SR, ["s_lamp"], V((-1.4, -4.8, 1.7)), V((-1.7, 9, 2.6)), 22, 11),
    ("13-street-medium", "night", SR, ["s_wave"], V((-1.9, 2.2, 1.1)), V((-2.9, 5.2, 0.95)), 32, 5.6),
    ("14-street-closeup", "night", SR, ["s_close"], V((-1.45, 4.15, 1.2)), V((-2.4, 5.5, 1.1)), 50, 2.0),
    ("15-street-low-angle-signs", "night", SR, ["s_point"], V((-1.2, 5.4, 0.35)), V((-1.9, 9, 3.0)), 20, 8),
    ("16-street-back-view", "night", SR, ["s_back"], V((3.4, 5.0, 1.4)), V((2.5, 9, 1.4)), 30, 4),
    ("17-street-two-characters", "night", SR, ["s_vend_a", "s_vend_b"], V((0.25, 3.6, 1.15)), V((0.25, 8.0, 1.0)), 30, 5.6),
    ("18-street-high-angle", "night", SR, ["s_lamp", "s_point"], V((-7.0, 1.0, 6.5)), V((-1.0, 7.5, 0.6)), 24, 11),
]

pc.cel_ink(sc)
os.makedirs(OUT, exist_ok=True)
for name, st, col, chars, cpos, apos, lens, fstop in STILLS:
    if ONLY and not any(k in name for k in ONLY):
        continue
    state(st)
    for c in (ST, WS, SR):
        c.hide_render = c is not col
    for key, objs in CHARS.items():
        for o in objs:
            o.hide_render = key not in chars
    cam.location, aim.location, cam.data.lens = V(cpos), V(apos), lens
    cam.data.dof.aperture_fstop = fstop
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("STILL", name, flush=True)
