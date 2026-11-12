"""EP004 look test: BG-WINDOW-RAINY in both states with CHAR-RAINKID (set-specs v1), cel look.

A rainy (LS1): medium shot from outside, the kid (curious) behind wet glass, rain streaks.
B dry (LS5): wider pull-back, clean pane, bright sky, the kid (wistful), roof and neighbours.

usage: blender -b -P renderer-blender/ep004_lookdev_window.py -- OUT_DIR [scale%]
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import papercraft as pc
pc.CEL = True
import ep004_sets as s4

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep004_lookdev"]
OUT, SCALE = argv[0], int(argv[1]) if len(argv) > 1 else 100
os.makedirs(OUT, exist_ok=True)

sc = pc.setup(SCALE, samples=48)
cam, aim = pc.camera()
O = Vector((0, 0, 0))
W = s4.window_set(O)
sun = pc.light("sun", "SUN", (0, 0, 10), 2.0, "#FFFFFF", rot=s4.deg(35, -40, 0), angle=8)
pc.cel_ink(sc)


def show(objs, on):
    for o in objs:
        if o is not None:
            o.hide_render = not on


STATES = {
    # world texture, world strength, grade, saturation, sun energy, sun colour, lamp energy
    "LS1": ("ep4_sky_rain_eq.png", 1.8, "#F2F4F9", 1.15, 4.8, "#E8EDF6", 260),
    "LS5": ("ep4_sky_bright_eq.png", 0.9, "#F1EADC", 1.08, 4.2, "#FFF4E2", 120),
}
SHOTS = [
    # name, state, rainy?, kid, camera loc, aim, lens, f-stop
    ("A-rainy-window", "LS1", True, "kid_curious", (0.25, -3.1, 1.15), (0.0, 0.2, 1.05), 24, 4.0),
    ("B-dry-pullback", "LS5", False, "kid_wistful", (0.7, -10.6, 1.0), (0.0, 0.0, 2.0), 24, 8.0),
]
for name, state, rainy, kid, loc, tgt, lens, fstop in SHOTS:
    tex, st, grade, sat, e, col, lamp = STATES[state]
    pc.set_world(tex, st, grade, sat)
    sun.data.energy, sun.data.color = e, pc.hexcol(col)[:3]
    W["lamp"].data.energy = lamp
    show(W["rain"], rainy)
    show(W["kid_curious"], kid == "kid_curious"); show(W["kid_wistful"], kid == "kid_wistful")
    cam.location, aim.location = loc, tgt
    cam.data.lens, cam.data.dof.aperture_fstop = lens, fstop
    pc.face_cards(loc)
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("STILL", name)
