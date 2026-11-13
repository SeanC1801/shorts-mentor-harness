"""The approved 3D motion test (2026-11-13) as an episode file for render_episode.py: the pattern every episode follows.
An episode file holds only what is specific to it: where its timings are, and what each view shows.
"""
import math
import bpy
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector as V
import toon3d as t3
from toon3d import kid, pose_kid, face_kid, mix_pose, POSES

TIMING = "renderer-blender/episodes/motion_test.timing.json"
N = 100
P = dict(POSES)          # extra poses for this clip, in the same shape as toon3d.POSES
P["glance"] = dict(L=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), R=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), look=30, tilt=-4)
P["think"] = dict(POSES["think"], look=14)
P["idea"] = dict(POSES["point_up"], look=0, tilt=-10)
P["shrug"] = dict(POSES["shrug"], tilt=6, look=8)
P["jump"] = dict(POSES["shock"], look=38, tilt=-6, lean=-5)
# frame, pose, face, hop height (m)
KEYS = [(0, "stand", "neutral", 0.0), (10, "glance", "neutral", 0.0), (24, "think", "worried", 0.0),
        (46, "idea", "surprised", 0.08), (56, "idea", "happy", 0.0), (68, "shrug", "smug", 0.0), (86, "jump", "nervous", 0.05)]
BLINKS = (36, 80)
SNAP = 5
S = {}


def build(ctx):
    ctx.use("workshop")
    kid("hero", V((0.25, 1.45, 0)), pose="stand", face="neutral", skin="#F4EFE6", top="#F2B10C", shoes="#C9482F", hair="#4A2C1A", build="bean")
    S["jar"], S["jar_light"] = bpy.data.objects["glow_jar"], bpy.data.objects["jar_light"]
    S["jar_em"] = next(nd for nd in S["jar"].data.materials[0].node_tree.nodes if nd.bl_idname == "ShaderNodeEmission")


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def snap(u):
    u = max(0.0, min(1.0, u)); c = 1.25
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def animate(ctx, f, t):
    i = max(k for k in range(len(KEYS)) if KEYS[k][0] <= f)
    kf, pose, face, hop = KEYS[i]
    prev = KEYS[i - 1] if i else KEYS[0]
    u = (f - kf) / SNAP
    pose_now = mix_pose(P[prev[1]], P[pose], snap(u)) if i else P[pose]
    air = math.sin(math.pi * min(1.0, u * SNAP / 8)) if (hop and u < 8 / SNAP) else 0.0
    pose_kid("hero", pose_now, hop=hop * air, squash=1 + 0.07 * air)
    changed = i and prev[2] != face and face != "nervous"
    blink = (changed and kf <= f < kf + 2) or any(b <= f < b + 2 for b in BLINKS)
    face_kid("hero", "blink" if blink else face)
    flare = ease((f - 82) / 4) * (0.75 + 0.25 * math.sin(f * 1.9))
    S["jar_em"].inputs[1].default_value = 2.0 + 2.2 * flare
    S["jar_light"].data.energy = 22 + 130 * flare
    k = ease(f / (N - 1)); k2 = ease((f - 44) / 8)
    ctx.cam.location = V((-0.95, -1.5, 1.25)).lerp(V((-0.5, -0.95, 1.14)), k) + V((0.05, 0.16, -0.02)) * k2
    ctx.aim.location = V((0.25, 1.5, 0.86)).lerp(V((0.27, 1.45, 0.95)), k)
    ctx.cam.data.lens = 28 + 1 * k + 1 * k2
    ctx.cam.data.dof.aperture_fstop = 4.0
    S["now"] = (pose, "blink" if blink else face)


def report(ctx, f):
    if f not in (0, 15, 26, 50, 57, 73, 86, 87, 90, 99):
        return None
    c = ctx.cam.evaluated_get(bpy.context.evaluated_depsgraph_get())
    rig = t3.RIGS["hero"]
    head = w2c(ctx.sc, c, rig["head"].matrix_world.translation)
    hands = [w2c(ctx.sc, c, h.matrix_world.translation) for h in rig["hands"]]
    feet = w2c(ctx.sc, c, rig["shoes"][0].matrix_world.translation)
    return (f"pose={S['now'][0]:6s} face={S['now'][1]:9s} head=({head.x:.2f},{head.y:.2f}) handL=({hands[0].x:.2f},{hands[0].y:.2f}) "
            f"handR=({hands[1].x:.2f},{hands[1].y:.2f}) feet_y={feet.y:.2f} lens={ctx.cam.data.lens:.1f} jar={S['jar_light'].data.energy:.0f}W")


VIEWS = {"S01-V1": dict(set="workshop", state="warm", animate=animate)}
