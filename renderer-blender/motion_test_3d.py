"""MOTION TEST (2026-11-13): the bean-build kid acting in the workshop set, 100 frames (3.3 s) at 30 fps.

Shows what look tests v1 and v2 could not: the 3D character moving. Poses snap over 5 frames with a small
overshoot and then hold still; faces change through a 2-frame blink; a hop and a stretch mark the big beat; the
camera moves the whole time. No captions or narration.

usage: blender -b -P renderer-blender/motion_test_3d.py -- OUT_DIR [scale%] [start] [end] [--dry]
       --dry runs every frame's animation and prints key frames, but renders nothing.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
import papercraft as pc
pc.CEL = True
import toon3d as t3
from toon3d import kid, pose_kid, face_kid, mix_pose, POSES
import toon_sets

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/motion3d"]
OUT = argv[0]
_pos = [a for a in argv[1:] if not a.startswith("--")]
for _a in _pos:
    if not _a.isdigit():
        sys.exit(f"motion_test_3d: argument {_a!r} is not a whole number (expected: OUT_DIR [scale] [start] [end])")
SCALE = int(_pos[0]) if len(_pos) > 0 else 100
N = 100
START, END = (int(_pos[1]) if len(_pos) > 1 else 0), min(N, int(_pos[2]) if len(_pos) > 2 else N)
DRY = "--dry" in argv
sc = pc.setup(SCALE, samples=32)
cam, aim = pc.camera()
V = Vector
t3.SKIN_SOFT = 0.45
t3.glow(sc, strength=0.4, threshold=1.0, size=0.5, vignette=0.35)
SUN = pc.light("sun", "SUN", V((0, 0, 20)), 4.0, "#FFFFFF", angle=1.2)
WS = toon_sets.workshop()
toon_sets.state("warm", SUN)
SPOT = V((0.25, 1.45, 0))
kid("hero", SPOT, pose="stand", face="neutral", skin="#F4EFE6", top="#F2B10C", shoes="#C9482F", hair="#4A2C1A", build="bean")
JAR, JAR_LIGHT = bpy.data.objects["glow_jar"], bpy.data.objects["jar_light"]
JAR_EM = next(nd for nd in JAR.data.materials[0].node_tree.nodes if nd.bl_idname == "ShaderNodeEmission")

# extra poses for this clip, in the same shape as toon3d.POSES
P = dict(POSES)
P["glance"] = dict(L=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), R=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), look=30, tilt=-4)
P["think"] = dict(POSES["think"], look=14)
P["idea"] = dict(POSES["point_up"], look=0, tilt=-10)
P["shrug"] = dict(POSES["shrug"], tilt=6, look=8)
P["jump"] = dict(POSES["shock"], look=38, tilt=-6, lean=-5)

# frame, pose, face, hop height (m)
KEYS = [(0, "stand", "neutral", 0.0), (10, "glance", "neutral", 0.0), (24, "think", "worried", 0.0),
        (46, "idea", "surprised", 0.08), (56, "idea", "happy", 0.0), (68, "shrug", "smug", 0.0), (86, "jump", "nervous", 0.05)]
BLINKS = (36, 80)          # idle blinks (2 frames each), besides the blink on every face change
SNAP = 5                   # frames a pose change takes


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def snap(u):
    """Ease out with a small overshoot: fast, lands a little past the pose, settles."""
    u = max(0.0, min(1.0, u)); c = 1.25
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def animate(f):
    i = max(k for k in range(len(KEYS)) if KEYS[k][0] <= f)
    kf, pose, face, hop = KEYS[i]
    prev = KEYS[i - 1] if i else KEYS[0]
    u = (f - kf) / SNAP
    pose_now = mix_pose(P[prev[1]], P[pose], snap(u)) if i else P[pose]
    air = math.sin(math.pi * min(1.0, u * SNAP / 8)) if (hop and u < 8 / SNAP) else 0.0
    pose_kid("hero", pose_now, hop=hop * air, squash=1 + 0.07 * air)
    changed = i and prev[2] != face and face != "nervous"      # a startle is instant: no blink first
    blink = (changed and kf <= f < kf + 2) or any(b <= f < b + 2 for b in BLINKS)
    face_kid("hero", "blink" if blink else face)
    # the jar flares from frame 82: that is what startles the kid
    flare = ease((f - 82) / 4) * (0.75 + 0.25 * math.sin(f * 1.9))
    JAR_EM.inputs[1].default_value = 2.0 + 2.2 * flare
    JAR_LIGHT.data.energy = 22 + 130 * flare
    # camera: one continuous push-in, with a quick extra push on the idea
    k = ease(f / (N - 1)); k2 = ease((f - 44) / 8)
    cam.location = V((-0.95, -1.5, 1.25)).lerp(V((-0.5, -0.95, 1.14)), k) + V((0.05, 0.16, -0.02)) * k2
    aim.location = V((0.25, 1.5, 0.86)).lerp(V((0.27, 1.45, 0.95)), k)
    cam.data.lens = 28 + 1 * k + 1 * k2
    cam.data.dof.aperture_fstop = 4.0
    return pose, face, blink


pc.cel_ink(sc)
os.makedirs(OUT, exist_ok=True)
for f in range(START, END):
    pose, face, blink = animate(f)
    if DRY:
        if f in (0, 9, 10, 12, 15, 24, 25, 26, 36, 46, 47, 50, 54, 56, 57, 68, 73, 86, 87, 90, 99):
            bpy.context.view_layer.update()
            c = cam.evaluated_get(bpy.context.evaluated_depsgraph_get())
            rig = t3.RIGS["hero"]
            head = w2c(sc, c, rig["head"].matrix_world.translation)
            hands = [w2c(sc, c, h.matrix_world.translation) for h in rig["hands"]]
            feet = [w2c(sc, c, s.matrix_world.translation) for s in rig["shoes"]]
            arm = rig["arms"][1]; zs = [v.co.z for v in arm.data.vertices]
            print(f"F{f:3d} pose={pose:6s} face={'blink' if blink else face:9s} head=({head.x:.2f},{head.y:.2f}) "
                  f"handL=({hands[0].x:.2f},{hands[0].y:.2f}) handR=({hands[1].x:.2f},{hands[1].y:.2f}) feet_y={feet[0].y:.2f} "
                  f"armR_z={min(zs):.2f}..{max(zs):.2f} root_z={rig['root'].location.z:.3f} lens={cam.data.lens:.1f} jar={JAR_LIGHT.data.energy:.0f}W", flush=True)
        continue
    sc.render.filepath = os.path.join(OUT, f"m_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f, flush=True)
print("RANGE", START, END - 1, "DRY" if DRY else "RENDERED", flush=True)
