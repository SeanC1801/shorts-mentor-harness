"""Shared renderer for the flat 3D look (visual style v4). One copy for every episode.

usage: blender -b -P renderer-blender/render_episode.py -- EPISODE OUT_DIR [scale%] [start] [end] [--frames a,b,c] [--dry]

EPISODE names a file in renderer-blender/episodes/ (for example `motion_test` or `ep005`). That file supplies only what
is specific to the episode:
    TIMING   path of its timing file (EPISODES/<ID>/episode.json), the single source of every frame range
    VIEWS    {"S01-V1": dict(set="workshop", state="warm", animate=fn)}; fn(ctx, f, t) poses characters and the camera
             for frame f, where t runs 0..1 across the view
    build(ctx)          optional: make the characters and props (called once, after the sets)
    report(ctx, f)      optional: a line of text for --dry
    GLOW                optional: settings for toon3d.glow
Only the sets used by the frames asked for are built. --dry runs every frame's animation and prints, but renders nothing.
Frames are written as f_NNNN.png; joins, captions and audio are added by scripts/finish_episode.py.
"""
import importlib, os, sys, types
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "episodes")]
import bpy
from mathutils import Vector
import papercraft as pc
pc.CEL = True
import toon3d as t3
import toon_sets, timing

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
flags = {"--dry", "--frames"}
pos, i = [], 0
while i < len(argv):
    if argv[i] == "--frames":
        i += 2; continue
    if argv[i].startswith("--"):
        if argv[i] not in flags:
            sys.exit(f"render_episode: unknown option {argv[i]!r}")
        i += 1; continue
    pos.append(argv[i]); i += 1
if len(pos) < 2:
    sys.exit("render_episode: expected EPISODE OUT_DIR [scale] [start] [end]")
for a in pos[2:]:      # a range passed as one argument ("861 917") once made every job render from frame 0
    if not a.isdigit():
        sys.exit(f"render_episode: argument {a!r} is not a whole number (expected: EPISODE OUT_DIR [scale] [start] [end])")
NAME, OUT = pos[0], pos[1]
SCALE = int(pos[2]) if len(pos) > 2 else 100
DRY = "--dry" in argv
EP = importlib.import_module(NAME)
T = timing.load(EP.TIMING)
START, END = (int(pos[3]) if len(pos) > 3 else 0), min(T["total"], int(pos[4]) if len(pos) > 4 else T["total"])
if "--frames" in argv:
    FRAMES = [int(x) for x in argv[argv.index("--frames") + 1].split(",")]
else:
    FRAMES = list(range(START, END))
if not FRAMES or min(FRAMES) < 0 or max(FRAMES) >= T["total"]:
    sys.exit(f"render_episode: no frames to render in {START}..{END} (the episode has frames 0..{T['total'] - 1})")
missing = sorted({v["key"] for v in T["views"]} - set(EP.VIEWS))
used = []
for f in FRAMES:
    k = timing.view_at(T, f)["key"]
    if k not in used:
        used.append(k)
bad = [k for k in used if k not in EP.VIEWS]
if bad:
    sys.exit(f"render_episode: {NAME} has no VIEWS entry for {bad}")
need_sets = []
for k in used:
    if EP.VIEWS[k]["set"] not in need_sets:
        need_sets.append(EP.VIEWS[k]["set"])

sc = pc.setup(SCALE, samples=getattr(EP, "SAMPLES", 32))
cam, aim = pc.camera()
t3.SKIN_SOFT = getattr(EP, "SKIN_SOFT", 0.45)
t3.glow(sc, **getattr(EP, "GLOW", dict(strength=0.4, threshold=1.0, size=0.5, vignette=0.35)))
sun = pc.light("sun", "SUN", Vector((0, 0, 20)), 4.0, "#FFFFFF", angle=1.2)
sets = {name: toon_sets.SETS[name]() for name in need_sets}      # only what these frames need
print("SETS", need_sets, "of", sorted(toon_sets.SETS), flush=True)
print("RANGE", f"{len(FRAMES)} frames {FRAMES[0]}-{FRAMES[-1]}", "views", used, "DRY" if DRY else "", flush=True)
if missing:
    print("NOTE views in the timing file with no VIEWS entry yet:", missing, flush=True)


def use(name):
    """Make new objects land in a set's collection (so they show and hide with it); None = always visible."""
    vl = bpy.context.view_layer
    vl.active_layer_collection = vl.layer_collection if name is None else vl.layer_collection.children[sets[name].name]


ctx = types.SimpleNamespace(sc=sc, cam=cam, aim=aim, sun=sun, sets=sets, timing=T, use=use, V=Vector, t3=t3, pc=pc, toon_sets=toon_sets)
if hasattr(EP, "build"):
    EP.build(ctx)
use(None)
pc.cel_ink(sc)
os.makedirs(OUT, exist_ok=True)
current = None
for f in FRAMES:
    v = timing.view_at(T, f)
    view = EP.VIEWS[v["key"]]
    if current != v["key"]:
        for name, col in sets.items():
            col.hide_render = name != view["set"]
        toon_sets.state(view["state"], sun)
        current = v["key"]
    view["animate"](ctx, f, (f - v["start"]) / max(1, v["end"] - v["start"] - 1))
    if DRY:
        if hasattr(EP, "report"):
            bpy.context.view_layer.update()
            line = EP.report(ctx, f)
            if line:
                print(f"DRY {f:4d} {v['key']} {line}", flush=True)
        continue
    sc.render.filepath = os.path.join(OUT, f"f_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f, flush=True)
print("DONE", len(FRAMES), "frames", "(dry run, nothing rendered)" if DRY else "rendered", flush=True)
