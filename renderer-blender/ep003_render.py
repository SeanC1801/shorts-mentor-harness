"""EP003 render: storyboard v3 (S01 V1 opens on Earth in space; otherwise v2), 30 fps, 1575 frames, 31 views on the approved sets,
characters and props. Writes PNG frames; transitions, captions, fades and narration are added by
scripts/finish_ep003.py.

usage: blender -b -P renderer-blender/ep003_render.py -- OUT_DIR [scale%] [start] [end] [--views] [--frames a,b,c] [--cel]
  --views renders one frame (the middle) of each view only, for checking.
  --frames renders only the listed frames.
  --cel uses the cel look (hard light bands + ink outlines; draft visual-style v3).
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Euler, Vector
import papercraft as pc
from papercraft import painted, flatcard, emit, card, light, blob, strip, cyl, sphere
import ep003_sets as sets
import ep003_props as props

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep003"]
OUT = argv[0]
SCALE = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 100
START = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 0
END = int(argv[3]) if len(argv) > 3 and argv[3].isdigit() else 1575
CHECK = "--views" in argv
ONLY = [int(a) for a in argv[argv.index("--frames") + 1].split(",")] if "--frames" in argv else None
pc.CEL = "--cel" in argv
random.seed(11)
sc = pc.setup(SCALE, samples=32)
sc.render.use_persistent_data = True
try:
    sc.eevee.shadow_pool_size = "1024"
except Exception:
    pass
cam, aim = pc.camera()
sets.init(cam)
V = Vector


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def ease_out(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


def deg(*a): return tuple(math.radians(x) for x in a)


STATES = {"BED": ("sky_day_eq.png", 0.9, "#F4E8D6", 1.0), "BED_DAWN": ("sky_dawn_eq.png", 0.7, "#D8C9E6", 1.0),
          "LS1": ("sky_day_eq.png", 0.9, "#E2D5C1", 1.35), "LS5": ("sky_cool_eq.png", 0.7, "#B4BED6", 1.45),
          "LS2": ("space_eq.png", 0.3, "#E6E8FF", 1.15), "LS6": ("space_eq.png", 0.3, "#FFE6CC", 1.2),
          "LS3": ("space_eq.png", 0.35, "#FFF2E0", 1.15), "LS7": ("water_eq.png", 0.85, "#A3CDC9", 1.25),
          "LS8": ("sky_dawn_eq.png", 0.7, "#C9B9DA", 1.4)}
COL, H = {}, {}   # collections and handles per stage


def stage(name, fn, O):
    COL[name] = pc.collection("ST-" + name)
    H[name] = fn(V(O)) or {}
    H[name]["O"] = V(O)


def by_name(col, prefix):
    return [o for o in COL[col].objects if o.name.startswith(prefix)]


def alt_cards(stage_name, base, poses, height):
    """Extra pose cards at the same spot as the set's card; returns {pose: card}."""
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["ST-" + stage_name]
    out = {}
    for pose in poses:
        o, sh = card("pose_" + pose, pose, height, base, cam, shadow=False)
        out[pose] = o
    return out


# ---------------- stages ----------------
stage("bedroom", sets.set_bedroom, (2800, 0, 0))
B = H["bedroom"]; BO = B["O"]
B["kid"] = alt_cards("bedroom", BO + V((0.8, 2.35, 0)), ["KID-CURTAINS.png", "KID-LOOK-UP.png"], 1.18)
B["kid_back"] = alt_cards("bedroom", BO + V((0.8, 2.25, 0)), ["KID-BACK-LOOK-UP.png"], 1.18)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["ST-bedroom"]
pc.plane("kid_shadow", BO + V((0.8, 2.3, 0.016)), (1.2, 0.36), (0, 0, 0), pc.shadow_mat())
for nm, fn, x in (("rooftops", sets.set_rooftops, 0), ("beach", sets.set_beach, 400), ("city", sets.set_city, 800),
                  ("north", sets.set_north, 1200), ("seafloor", sets.set_seafloor, 2000), ("dawn", sets.set_dawn, 2400)):
    stage(nm, lambda O, fn=fn: {"shot": fn(O)}, (x, 0, 0))
# beach: the edge-on ring is a hairline; a slightly thicker bright copy makes "a thin line straight overhead" read
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["ST-beach"]
pc.ring("ring_line", H["beach"]["O"], 0, sets.R, sets.RIN, sets.ROUT, emit("#FFF6E6", 1.5), thick=0.035).visible_shadow = False
for o in COL["beach"].objects:
    if o.name.split(".")[0] == "ring":
        o.hide_render = True   # the bright copy replaces it here (avoids flicker where the two overlap)
# north: faint dotted line where the ring sits below the horizon
NO = H["north"]["O"]
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["ST-north"]
H["north"]["dots"] = [blob("below_dot", NO + V((-28 + k * 2.0, -60, 1.0 + 0.004 * (k - 14) ** 2)), 0.18, emit("#FFF1D6", 1.4, alpha=0.7), sub=1) for k in range(29)]
dawn_cards = alt_cards("dawn", H["dawn"]["O"] + V((4.0, -0.3, 0)), ["DINO-STEP-A.png", "DINO-STEP-B.png"], 1.0)
for o in COL["seafloor"].objects:
    if o.name.startswith("trilobite"):
        o.location.x += 0.4; o.location.y += 0.6   # clear of the rock beside it, so the crane starts on the trilobite
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["ST-dawn"]
H["dawn"]["ring_mat"] = pc.ring_mat()
pc.ring("ring_dawn", H["dawn"]["O"], 20, sets.R, sets.RIN, sets.ROUT, H["dawn"]["ring_mat"], thick=0.02)


def st_ice(O):
    C = O + V((0, 9, 0.5))
    sun = card("sun_disc", "sun_disc.png", 4.0, C + V((2.2, 4, -1.5)), shadow=False)[0]; sun.data.materials[0] = flatcard("sun_disc.png", 2.2)
    props.glow_card("sun_glow", C + V((2.2, 3.9, 0.5)), 9.0, 1.4)
    ice = blob("ice_chunk", C + V((-0.6, -1.5, 0.2)), 0.55, painted("ice.png", 2.0, lift=1.15), scale=(1.1, 1, 0.9), sub=1, smooth=False)
    rock = blob("rock_chunk", C + V((-1.0, -2.6, -0.7)), 0.4, painted("rock.png", 2.0), scale=(1.2, 1, 0.85), sub=1, smooth=False)
    vapor = []
    for k in range(10):
        a = random.uniform(-0.6, 0.6)
        pts = [C + V((-0.6 + 0.3 * t * math.sin(a * 3), -1.5 - 0.1 * t, 0.7 + 1.4 * t)) for t in (0, 0.33, 0.66, 1)]
        vapor.append(strip("vapor", pts, [0.25, 0.3, 0.22, 0.05], emit("#F4FBFF", 1.2, alpha=0.35)))
    sparks = [blob("sparkle", C + V((-0.6 + random.uniform(-0.8, 0.8), -1.6 + random.uniform(-0.3, 0.3), 0.2 + random.uniform(-0.4, 1.4))), 0.03, emit("#FFFFFF", 3.0), sub=1) for _ in range(14)]
    light("sun", "SUN", O + V((0, 0, 10)), 4.5, "#FFF2D6", rot=deg(10, 60, 0), angle=8)
    return dict(C=C, ice=ice, rock=rock, vapor=vapor, sparks=sparks)


def st_pins(O):
    C = O + V((0, 9, 0))
    g = props.globe("globe_pins", C, 2.6, "earth_map.png", tilt=0); g.rotation_euler = deg(-15, 0, -100)
    heads = props.pins(g, 2.6, (0, 40, 70))
    stems = by_name("pins", "pin_stem")
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return dict(C=C, heads=heads, stems=stems)


def st_ghost(O):
    C = O + V((0, 10, 0))
    props.globe("globe", C, 2.6, "earth_map.png", spin=150)
    m = pc.ring_mat(haze="#DDE8FF", haze_amt=0.55, strength=1.2, alpha_mul=0.0)
    pc.ring_around("ghost_ring", C, 2.6, 1.7, 2.4, m, tilt_deg=-14)
    # S05 V2: a question mark glints beside the ghost ring
    cu = bpy.data.curves.new("qmark", "FONT"); cu.body = "?"
    cu.font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Arial Black.ttf")
    cu.align_x, cu.align_y, cu.extrude, cu.size = "CENTER", "CENTER", 0.06, 1.3
    q = bpy.data.objects.new("qmark", cu); bpy.context.collection.objects.link(q)
    q.data.materials.append(emit("#FFF1D6", 1.8))
    q.location, q.rotation_euler = C + V((1.7, -2.6, 2.3)), deg(90, 0, -12)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return dict(C=C, ring_mat=m, q=q)


def st_paper(O):
    props.globe("globe", O + V((1.2, 10, 0.4)), 2.6, "earth_map.png", spin=120)
    card("paper", "PROP-PAPER-STAMP.png", 2.6, O + V((-0.2, 4.5, -1.3)), shadow=False)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)


def st_timeline(O):
    props.globe("globe_ancient", O + V((0, 11, -0.6)), 3.0, "ancient_map.png", tilt=-25, spin=-90)
    c, _ = card("timeline", "PROP-TIMELINE-CARD.png", 1.15, O + V((0, 4.5, 0.4)), shadow=False)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return dict(card=c, base=O + V((0, 4.5, 0.4)))


def st_asteroid(O):
    props.globe("globe_ancient", O + V((2.5, 16, -1.5)), 4.0, "ancient_map.png", tilt=-25, spin=-90)
    a = props.asteroid(O + V((-0.6, 6, 0.6)), 0.8)
    frags = props.chunks_arc(O + V((-0.6, 3, 0.6)), 1.0, 2.0, 1.2, 0, 360, 10, size=0.04)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(10, -70, 0), angle=8)
    return dict(ast=a)


def st_ringform(O):
    C = O + V((0, 12, 0))
    props.globe("globe_ancient", C, 2.5, "ancient_map.png", tilt=-25, spin=-90)
    a = props.asteroid(C + V((-3.6, -1.0, 0.9)), 0.55)
    a.rotation_euler = deg(0, 0, -25)
    # pieces stream out from the break (about 190 deg) and wrap a full turn around Earth
    rot = Euler((math.radians(12), 0, 0)).to_matrix()
    chunks = [(o, a, rot.inverted() @ (o.location - C)) for o, a in props.chunks_arc(C, 2.5, 1.95, 0.14, 190, 550, 480, tilt=12, size=0.05)]
    chunks.sort(key=lambda c: c[1])
    glow = props.glow_card("break_glow", C + V((-3.4, -1.3, 0.9)), 2.6, 1.8)
    light("break", "POINT", C + V((-3.6, -1.6, 1.0)), 400, "#FFB066")
    light("sun", "SUN", O + V((0, 0, 10)), 3.5, "#FFE2C0", rot=deg(20, -60, 0), angle=8)
    return dict(C=C, rot=rot, ast=a, chunks=chunks, glow=glow)


def equator_band(name, g, r, lat, color, alpha_key):
    """A sphere shell between +-lat on globe g's own equator; it glows by fading in its mix factor."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=48, radius=r)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if abs(v.co.z) > r * math.sin(math.radians(lat))], context="VERTS")
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    band = bpy.data.objects.new(name, me); g.users_collection[0].objects.link(band)
    band.rotation_mode, band.location, band.rotation_euler = g.rotation_mode, g.location.copy(), g.rotation_euler
    m = emit(color, 2.6, alpha=alpha_key); me.materials.append(m)
    band.visible_shadow = False
    return m


def set_mix(m, a):
    next(x for x in m.node_tree.nodes if x.bl_idname == "ShaderNodeMixShader").inputs[0].default_value = a


def st_craters(O):
    C = O + V((0, 9, 0))
    g = props.globe("globe_ancient", C, 2.6, "ancient_map.png", tilt=0); g.rotation_euler = deg(-12, 0, -90)
    dots = props.crater_dots(g, 2.6, size=0.03, max_lon=55)   # within 30 deg of the equator (C8), on the camera side
    eq = cyl("equator_line", C, 2.62, 0.02, emit("#FFF1D6", 1.5, alpha=0.6), rot=deg(-12, 0, 0), verts=96)
    eq.rotation_euler = g.rotation_euler   # the globe's own equator, so the dots sit around the line
    band = equator_band("crater_band", g, 2.615, 30, "#FF8A3A", 0.0011)   # the 30-degree belt that glows in V3
    counters = {}
    for k in range(1, 22):
        counters[k], _ = card(f"counter{k}", f"PROP-COUNTER-{k:02d}.png", 0.7, O + V((0.45, 5, 1.1)), shadow=False)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return dict(C=C, dots=dots, counters=counters, eq=eq, band=band)


FALL0, FALL_N, FALL_DUR = 1150, 16, 38   # S08: first launch frame, falling pieces, frames per fall


def st_fade(O):
    """S08: the ring thins and dims; pieces spiral down and land in a band along the equator."""
    state = random.getstate()
    rng = random.Random(8)
    C, Rg, tilt = O + V((0, 12, 0)), 2.5, 22   # ring and globe share one equatorial plane, near side tipped down
    rot = Euler((math.radians(tilt), 0, 0)).to_matrix()
    g = props.globe("globe_ancient", C, Rg, "ancient_map.png", tilt=0)
    g.rotation_mode, g.rotation_euler = "ZXY", (math.radians(tilt), 0, math.radians(-90))   # spin the map, then tilt the axis
    m = pc.ring_mat(haze="#AFC2E6", haze_amt=0.25, alpha_mul=0.45)
    pc.ring_around("ring_fading", C, Rg, 1.7, 2.3, m, tilt_deg=tilt)
    ring_chunks = [o for o, a in props.chunks_arc(C, Rg, 2.0, 0.22, 0, 360, 420, tilt=tilt, size=0.03)]
    rng.shuffle(ring_chunks)
    falls = []
    for k in range(FALL_N):
        a0 = math.radians(-150 + 120 * (k + rng.random()) / FALL_N)   # camera side of the ring
        lat = math.radians(rng.uniform(-22, 22))
        path = []
        for u in (i / 8 for i in range(9)):
            r = Rg * (1.75 + (1.012 - 1.75) * (u ** 1.6))
            a = a0 + math.radians(35) * u
            path.append(C + rot @ V((r * math.cos(a) * math.cos(lat * u), r * math.sin(a) * math.cos(lat * u), r * math.sin(lat * u))))
        st = strip("streak", path, [0.0] + [0.012 + 0.05 * i / 8 for i in range(1, 9)], emit("#FFD9A0", 1.6, alpha=0.75), up=tuple(rot @ V((0, 0, 1))))
        ch = blob("chunk", path[0], 0.07, painted("rock.png", 6.0), sub=1, smooth=False)
        fl = blob("crater_dot", path[-1], Rg * 0.035, emit("#FF9B4A", 2.5), sub=2)
        falls.append((st, ch, fl, path))
    fg = [blob("chunk", O, 0.13 * s, painted("rock.png", 6.0), scale=(1.6, 1, 0.75), sub=2, smooth=False) for s in (1.0, 0.7, 1.2)]
    band = equator_band("fall_band", g, Rg * 1.006, 25, "#FF8A3A", 0.0012)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    random.setstate(state)
    for _ in range(28):   # the old S08 build drew 28 values; keep later stages (and the S01 opener) unchanged
        random.uniform(0, 1)
    return dict(C=C, ring_mat=m, ring_chunks=ring_chunks, falls=falls, fg=fg, band=band)


def qmark(name, size):
    """A small glowing question mark (Arial Black), standing upright and facing -y."""
    cu = bpy.data.curves.new(name, "FONT"); cu.body = "?"
    cu.font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Arial Black.ttf")
    cu.align_x, cu.align_y, cu.extrude, cu.size = "CENTER", "CENTER", 0.03, size
    q = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(q)
    q.data.materials.append(emit("#FFF1D6", 1.8))
    q.rotation_euler = deg(90, 0, 0)
    return q


def st_tags(O):
    pc.plane("ground", O + V((0, 6, -0.2)), (40, 40), (0, 0, 0), painted("rock.png", 0.4))
    tags = []
    for k, (x, y) in enumerate(((-1.1, 5.0), (0.3, 6.0), (1.3, 4.6))):
        p = O + V((x, y, -0.2))
        cyl("crater_rim", p, 0.7, 0.32, painted("asteroid.png", 2.0, lift=1.1), verts=40, r2=0.55, bevel=0.08)
        cyl("crater_floor", p + V((0, 0, 0.12)), 0.5, 0.1, painted("asteroid.png", 3.0, lift=0.6), verts=40)
        tags.append(card(f"tag{k}", "PROP-AGE-TAG.png", 0.42, p + V((0.35, -0.6, 0.1)), shadow=False)[0])
    qs = [(qmark(f"qmark{k}", 0.6), O + V((x, y, -0.05))) for k, (x, y) in enumerate(((-1.1, 5.0), (0.3, 6.0), (1.3, 4.6)))]
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(40, -40, 0), angle=8)
    return dict(tags=tags, qs=qs)


def st_ringstamp(O):
    state = random.getstate()
    C, Rg, tilt = O + V((0, 11, 0)), 2.5, 22   # the same view of the ring as S08: near side tipped down
    g = props.globe("globe_ancient", C, Rg, "ancient_map.png", tilt=0)
    g.rotation_mode, g.rotation_euler = "ZXY", (math.radians(tilt), 0, math.radians(-90))
    m = pc.ring_mat(haze="#AFC2E6", haze_amt=0.15, alpha_mul=0.0)
    pc.ring_around("ring_new", C, Rg, 1.7, 2.3, m, tilt_deg=tilt)
    chunks = [o for o, a in props.chunks_arc(C, Rg, 2.0, 0.22, 0, 360, 420, tilt=tilt, size=0.03)]
    random.Random(4).shuffle(chunks)
    random.setstate(state)   # keep later stages (the S01 opener) unchanged
    stamp, _ = card("stamp", "PROP-PAPER-STAMP.png", 1.15, O + V((-0.75, 5.2, -1.45)), shadow=False)
    glint = blob("glint", O + V((-0.35, 5.0, -0.55)), 0.05, emit("#FFFFFF", 3.0), scale=(1, 1, 1), sub=1)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return dict(C=C, ring_mat=m, chunks=chunks, stamp=stamp, glint=glint)


def st_opener(O):
    """S01 V1 (storyboard v3): today's Earth in space; a ring of rocks settles around it."""
    C = O + V((0, 14, 0))
    g = props.globe("globe_opener", C, 2.6, "earth_map.png", tilt=0); g.rotation_euler = deg(-15, 0, -100)
    tilt = 18
    rot = Euler((math.radians(tilt), 0, 0)).to_matrix()
    chunks = [(o, rot.inverted() @ (o.location - C)) for o, a in props.chunks_arc(C, 2.6, 2.05, 0.26, 0, 360, 650, tilt=tilt, size=0.032)]
    m = pc.ring_mat(haze="#AFC2E6", haze_amt=0.35, alpha_mul=0.0)
    pc.ring_around("ring_opener", C, 2.6, 1.75, 2.35, m, tilt_deg=tilt)
    light("sun", "SUN", O + V((0, 0, 10)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return dict(C=C, rot=rot, chunks=chunks, ring_mat=m)


for i, (nm, fn) in enumerate((("ice", st_ice), ("pins", st_pins), ("ghost", st_ghost), ("paper", st_paper), ("timeline", st_timeline),
                              ("asteroid", st_asteroid), ("ringform", st_ringform), ("craters", st_craters), ("fade", st_fade),
                              ("tags", st_tags), ("ringstamp", st_ringstamp), ("opener", st_opener))):
    stage(nm, fn, (i * 60.0, 5000, 0))

# ---------------- views (frames from approved storyboard v2) ----------------
def mathnode(m):
    return next(n for n in m.node_tree.nodes if n.bl_idname == "ShaderNodeMath")


def set_alpha(m, a):
    mathnode(m).inputs[1].default_value = a


def show(objs, on):
    for o in objs:
        o.hide_render = not on


def pose(cards, which):
    for k, o in cards.items():
        o.hide_render = k != which


def ev_bed_globe(t, f):
    k = 1 + 0.9 * (1 - ease_out(t * 1.5))
    for rk, p in B["rocks"]:
        rk.location = B["G"] + p * k
    pose(B["kid"], None); pose(B["kid_back"], None)


def ev_opener(t, f):
    Op = H["opener"]
    k = 1 + 0.8 * (1 - ease_out(t / 0.75))   # rocks fall in from a wider orbit and settle
    sp = Euler((0, 0, math.radians(-25 * t))).to_matrix()   # and keep circling
    for o, p in Op["chunks"]:
        o.location = Op["C"] + Op["rot"] @ (sp @ p) * k
    set_alpha(Op["ring_mat"], 0.4 * ease((t - 0.35) / 0.5))


# S10: the bedroom ring gets its own fading copy; S01 keeps the shared ring material
BED_RINGS = [o for o in COL["bedroom"].objects if o.name.split(".")[0] == "ring"]
BED_MATS = {o.name: [sl.material for sl in o.material_slots] for o in BED_RINGS}
BED_FADE = pc.ring_mat()


def bed_ring(fade):
    """fade None: the ring as approved in S01; otherwise every slot uses the fading copy at that alpha."""
    for o in BED_RINGS:
        for sl, m in zip(o.material_slots, BED_MATS[o.name]):
            sl.material = m if fade is None else BED_FADE
    if fade is not None:
        set_alpha(BED_FADE, fade)


def ev_bed_curtains(t, f):
    bed_ring(None)
    for rk, p in B["rocks"]:
        rk.location = B["G"] + p
    o = 0.55 * (1 - ease(t / 0.5))
    B["curtains"][0].location.x = BO.x + o
    B["curtains"][1].location.x = BO.x - o
    pose(B["kid"], "KID-CURTAINS.png" if t < 0.7 else "KID-LOOK-UP.png"); pose(B["kid_back"], None)


def ev_bed_window(t, f):
    bed_ring(None)
    for c in B["curtains"]: c.location.x = BO.x
    pose(B["kid"], "KID-LOOK-UP.png"); pose(B["kid_back"], None)


def ev_bed_dawn(t, f):
    for c in B["curtains"]: c.location.x = BO.x
    pose(B["kid"], None); pose(B["kid_back"], "KID-BACK-LOOK-UP.png")
    bed_ring(0.3 * (1 - ease(t / 0.75)))   # the faintest stripe, fading to an empty sky


def ev_ice(shrink0, shrink1, vapor_on):
    def ev(t, f):
        I = H["ice"]
        s = max(0.001, shrink0 + (shrink1 - shrink0) * t)
        I["ice"].scale = (1.1 * s, s, 0.9 * s)
        I["ice"].hide_render = s < 0.02
        for k, v in enumerate(I["vapor"]): v.hide_render = not (vapor_on(t) and (f + k) % 3 != 0)
        for k, sp in enumerate(I["sparks"]): sp.hide_render = not (vapor_on(t) and (f * 7 + k * 3) % 5 < 3)
    return ev


def ev_pins(pop):
    def ev(t, f):
        P = H["pins"]
        for k, (hd, stm) in enumerate(zip(P["heads"], P["stems"])):
            on = pop and t > k * 0.28
            hd.hide_render = stm.hide_render = not on
            if on:
                hd.scale = (1, 1, 1) * (0.4 + 0.6 * ease_out((t - k * 0.28) / 0.15)) if False else [0.4 + 0.6 * ease_out((t - k * 0.28) / 0.15)] * 3
    return ev


def ev_none(t, f):
    pass


def ev_north(kid_on):
    def ev(t, f):
        for o in COL["north"].objects:
            if o.name.startswith("kid"):
                o.hide_render = not kid_on
        show(H["north"]["dots"], kid_on and t > 0.15)
    return ev


def ev_ghost(a0, a1, shimmer, qmark=False):
    def ev(t, f):
        a = a0 + (a1 - a0) * ease(t)
        if shimmer:
            a *= 0.75 + 0.25 * math.sin(f * 0.6)
        set_alpha(H["ghost"]["ring_mat"], a)
        q = H["ghost"]["q"]
        q.hide_render = not (qmark and t > 0.3)
        if qmark:
            s = ease_out((t - 0.3) / 0.25)
            q.scale = [max(0.01, s * (1.0 + 0.12 * math.sin(f * 0.9)))] * 3   # pop in, then a gentle glint pulse
    return ev


def ev_timeline(t, f):
    T = H["timeline"]
    T["card"].location = T["base"] + V((-3.0 * (1 - ease_out(t / 0.35)), 0, 0))


def ev_asteroid(t, f):
    A = H["asteroid"]; O = A["O"]
    A["ast"].location = (O + V((-7, 9, 3.2))).lerp(O + V((-0.6, 6, 0.6)), ease(t))
    A["ast"].rotation_euler.z = t * 1.5


def ev_ringform(t, f):
    R = H["ringform"]
    R["ast"].scale.x = 1.0 + 0.9 * ease(t / 0.4)
    R["ast"].hide_render = t > 0.55
    head = math.radians(190 + 360 * ease((t - 0.12) / 0.72))   # the stream's leading edge closes the loop by t = 0.84
    sp = Euler((0, 0, math.radians(40 * t))).to_matrix()        # and the whole ring keeps orbiting
    for o, a, p in R["chunks"]:
        o.hide_render = a > head
        o.location = R["C"] + R["rot"] @ (sp @ p)
    R["glow"].scale = [0.6 + 0.6 * math.sin(min(1, t / 0.5) * math.pi)] * 3


def ev_craters(c0, c1, f0, f1, band=False):
    def ev(t, f):
        Cr = H["craters"]
        n = int(round(21 * max(0, min(1, (f - f0) / (f1 - f0))))) if f1 > f0 else 21
        for k, d in enumerate(Cr["dots"]):
            d.hide_render = k >= n
            fk = f0 + (k + 0.5) / 21 * (f1 - f0)   # frame this dot appears: pop in with a small overshoot
            p = max(0.0, min(1.0, (f - fk) / 5)) if f1 > f0 else 1.0
            d.scale = [ease_out(p) * (1 + 0.5 * math.sin(p * math.pi))] * 3
        for k, o in Cr["counters"].items():
            o.hide_render = k != n
        Cr["eq"].hide_render = False
        set_mix(Cr["band"], 0.18 * ease(t / 0.5) if band else 0.0)
    return ev


def ev_fade(t, f):
    """S08 on one clock (frames 1122-1306): thin and dim the ring, drop the pieces, glow the band."""
    Fd = H["fade"]
    u = max(0.0, min(1.0, (f - 1122) / (1306 - 1122)))
    set_alpha(Fd["ring_mat"], 0.45 - 0.37 * ease(u))
    keep = 1 - 0.65 * ease(u)
    for k, o in enumerate(Fd["ring_chunks"]):
        o.hide_render = k >= keep * len(Fd["ring_chunks"])
    for k, (st, ch, fl, path) in enumerate(Fd["falls"]):
        # the first pair drifts off the ring edge slowly in V1; the rest follow in V2
        L, D = (1135 + 12 * k, 70) if k < 2 else (FALL0 + 40 + (k - 2) * 4, FALL_DUR)
        p = (f - L) / D
        flying = 0 <= p < 1
        st.hide_render = not flying
        ch.hide_render = not flying
        if flying:
            q = (p ** 1.4) * (len(path) - 1)
            i = min(int(q), len(path) - 2)
            ch.location = path[i].lerp(path[i + 1], q - i)
        landed = (f - L - D)
        fl.hide_render = landed < 0
        fp = max(0.0, min(1.0, landed / 6))
        fl.scale = [ease_out(fp) * (1 + 1.2 * math.sin(fp * math.pi))] * 3
    # foreground fragments cross the lens during V2
    for k, o in enumerate(Fd["fg"]):
        w = (f - 1189 - 14 * k) / 34
        o.hide_render = not (0 <= w <= 1)
        o.location = Fd["C"] + V((-1.4 + 2.8 * w, -7.5 + 0.6 * k, 1.25 - 0.25 * k + 0.15 * w))   # just ahead of the V2 camera
        o.rotation_euler = (f * 0.05 + k, f * 0.03, 0)
    set_mix(Fd["band"], 0.2 * ease((f - 1262) / 30))
    return None


def ev_tags(t, f):
    Tg = H["tags"]
    for k, tg in enumerate(Tg["tags"]):
        tg.hide_render = ((f // 3 + 2 * k) % 7 == 0)   # each tag blinks off briefly, out of step
    for k, (q, base) in enumerate(Tg["qs"]):
        u = max(0.0, min(1.0, (t - 0.25 - 0.12 * k) / 0.45))
        q.hide_render = u <= 0
        q.location = base + V((0, 0, 0.15 + 0.75 * ease_out(u)))
        q.scale = [ease_out(min(1, u * 3)) * (1 + 0.1 * math.sin(f * 0.8 + k))] * 3


def ev_ringstamp(t, f):
    R = H["ringstamp"]
    set_alpha(R["ring_mat"], 0.65 * ease(t / 0.7))
    for k, o in enumerate(R["chunks"]):
        o.hide_render = k >= ease(t / 0.6) * len(R["chunks"])
    R["stamp"].hide_render = t < 0.3
    g = max(0.0, 1 - abs(t - 0.62) / 0.12)   # one glint across the stamp
    R["glint"].hide_render = g <= 0
    R["glint"].scale = [0.5 + 3.5 * g] * 3


def ev_dawn(t, f):
    D = H["dawn"]; O = D["O"]
    dino = [o for o in COL["dawn"].objects if o.name == "dino"][0]
    walking = t < 0.6
    x = 6.8 + (4.0 - 6.8) * ease(t / 0.6)
    for o in [dino] + list(dawn_cards.values()) + by_name("dawn", "dino_shadow"):
        o.location = O + V((x, -0.3, o.location.z - O.z))   # the contact shadow walks with the dinosaur
    step = "DINO-STEP-A.png" if (f // 4) % 2 == 0 else "DINO-STEP-B.png"
    for k, o in dawn_cards.items():
        o.hide_render = not (walking and k == step)
    dino.hide_render = walking
    set_alpha(D["ring_mat"], 0.7 * (1 - ease(t / 0.4)))   # the ring fades out before the dinosaur arrives


Bo, Ro, Be, Ci, No, Se, Da = (H[k]["O"] for k in ("bedroom", "rooftops", "beach", "city", "north", "seafloor", "dawn"))
Ic, Pi, Gh, Pa, Ti, As, Rf, Cr, Fd, Tg, Rs, Op = (H[k]["O"] for k in ("ice", "pins", "ghost", "paper", "timeline", "asteroid", "ringform", "craters", "fade", "tags", "ringstamp", "opener"))
G = B["G"]
# (start, end, stage, state, (pos0, tgt0, lens0), (pos1, tgt1, lens1), event, join_out)
VIEWS = [
    (0, 60, "opener", "LS2", (Op + V((0.8, -4.5, 3.6)), Op + V((0, 14, 0)), 18), (Op + V((0.2, 0.0, 2.6)), Op + V((0, 14, -0.1)), 20), ev_opener, "push"),
    (60, 112, "bedroom", "BED", (Bo + V((0.1, -1.4, 1.3)), Bo + V((0.8, 2.6, 1.25)), 24), (Bo + V((0.45, 0.6, 1.35)), Bo + V((0.8, 3.0, 1.5)), 24), ev_bed_curtains, "push"),
    (112, 162, "bedroom", "BED", (Bo + V((0.6, 1.4, 1.5)), Bo + V((0.8, 3.2, 1.7)), 22), (Bo + V((0.8, 4.0, 1.7)), Bo + V((0.6, 30, 16)), 18), ev_bed_window, "follow"),
    (162, 215, "rooftops", "LS1", (Ro + V((0.6, 1.2, 3.6)), Ro + V((-0.5, -30, 11)), 18), (Ro + V((0.2, 1.4, 3.8)), Ro + V((-1.5, -30, 18)), 18), ev_none, "whip"),
    (215, 265, "ice", "LS3", (Ic + V((-0.4, 0, 0.6)), Ic + V((-0.1, 9, 0.9)), 30), (Ic + V((-0.5, 0.9, 0.55)), Ic + V((-0.6, 7.5, 0.7)), 30), ev_ice(1.0, 0.55, lambda t: True), "follow"),
    (265, 313, "ice", "LS3", (Ic + V((-0.5, 0.9, 0.55)), Ic + V((-0.6, 7.5, 0.7)), 30), (Ic + V((-0.9, 3.4, 0.2)), Ic + V((-1.0, 6.4, -0.2)), 30), ev_ice(0.55, 0.0, lambda t: t < 0.5), "whip"),
    (313, 350, "pins", "LS2", (Pi + V((0.3, 0, 0.8)), Pi + V((0, 9, 0.6)), 20), (Pi + V((1.4, 0.6, 1.0)), Pi + V((0, 9, 0.6)), 20), ev_pins(False), "follow"),
    (350, 385, "pins", "LS2", (Pi + V((1.4, 0.6, 1.0)), Pi + V((0, 9, 0.6)), 20), (Pi + V((0.6, 4.2, 0.2)), Pi + V((0.4, 9, 0)), 24), ev_pins(True), "push"),
    # beach: face north so the edge-on equatorial ring crosses the frame left to right as the camera tilts up to the zenith
    (385, 435, "beach", "LS1", (Be + V((5.0, -3.6, 1.2)), Be + V((5.2, 12, 2.5)), 16), (Be + V((5.1, -3.2, 1.0)), Be + V((5.2, 3, 16)), 16), ev_none, "follow"),
    (435, 487, "beach", "LS1", (Be + V((5.3, -1.6, 0.3)), Be + V((5.2, 1.4, 4.9)), 10.5), (Be + V((5.25, -1.4, 0.28)), Be + V((5.2, 1.5, 5.2)), 10.5), ev_none, "whip"),
    (487, 530, "city", "LS1", (Ci + V((0.4, 2.0, 1.7)), Ci + V((-12, -30, 12)), 18), (Ci + V((0.4, 2.0, 1.7)), Ci + V((10, -30, 12)), 18), ev_none, "follow"),
    (530, 573, "city", "LS1", (Ci + V((0.4, 2.0, 1.7)), Ci + V((10, -30, 12)), 18), (Ci + V((0.6, 1.8, 1.6)), Ci + V((16, -40, 3)), 18), ev_none, "whip"),
    (573, 620, "north", "LS5", (No + V((0.3, 3.0, 1.0)), No + V((0, -30, 3)), 18), (No + V((0.3, 3.0, 2.4)), No + V((0, -30, 9)), 18), ev_north(False), "push"),
    # north: start on the dotted line at the horizon, then push over the fence in close on the shrug (kid at y -5.5)
    (620, 671, "north", "LS5", (No + V((0.5, 0.6, 1.45)), No + V((0.4, -30, 1.3)), 22), (No + V((0.9, -3.0, 1.05)), No + V((0.4, -30, 0.2)), 24), ev_north(True), "follow"),   # face above the caption band
    # S05 V1: pull back from close to the surface; the ring that was there fades away, leaving plain Earth
    (671, 705, "ghost", "LS2", (Gh + V((0, 2.6, 1.8)), Gh + V((0, 10, 0)), 32), (Gh + V((0, -1.5, 2.2)), Gh + V((0, 10, 0)), 24), ev_ghost(0.7, 0.0, False), "dissolve"),
    (705, 737, "ghost", "LS2", (Gh + V((0, -1.5, 2.2)), Gh + V((0, 10, 0)), 24), (Gh + V((1.6, -0.6, 3.0)), Gh + V((0.4, 10, 0.3)), 24), ev_ghost(0.0, 0.3, True, qmark=True), "dissolve"),
    # stamp held above the caption band ("466" is spoken over the end of this view)
    (737, 800, "paper", "LS2", (Pa + V((0, -1.0, -0.1)), Pa + V((-0.2, 4.5, -0.2)), 32), (Pa + V((-0.1, 1.6, -0.45)), Pa + V((-0.2, 4.5, -0.45)), 32), ev_none, "whip"),
    # keep the whole "466 MILLION YEARS AGO" card inside the frame width while pushing in
    (800, 849, "timeline", "LS2", (Ti + V((0, -1.0, 0.4)), Ti + V((0, 6, 0.4)), 24), (Ti + V((0, 0.6, 0.4)), Ti + V((0, 6, 0.4)), 24), ev_timeline, "whip"),
    (849, 905, "asteroid", "LS2", (As + V((-1.5, -1, 1.0)), As + V((-6, 9, 3)), 24), (As + V((0.2, 0, 0.2)), As + V((0, 8, 0.4)), 26), ev_asteroid, "follow"),
    (905, 983, "ringform", "LS6", (Rf + V((-0.8, -2, 2.4)), Rf + V((-1.2, 12, 0)), 20), (Rf + V((2.0, -2.5, 1.6)), Rf + V((-0.4, 12, 0)), 20), ev_ringform, "follow"),
    (983, 1035, "craters", "LS2", (Cr + V((0, -1.0, 0.6)), Cr + V((0, 9, 0.2)), 30), (Cr + V((0, 1.0, 0.6)), Cr + V((0, 9, 0.2)), 30), ev_craters(0, 0, 983, 1075), "follow"),
    (1035, 1080, "craters", "LS2", (Cr + V((0, 1.0, 0.6)), Cr + V((0, 9, 0.2)), 30), (Cr + V((1.2, 1.2, 1.0)), Cr + V((0, 9, 0.2)), 30), ev_craters(0, 0, 983, 1075), "push"),
    (1080, 1122, "craters", "LS2", (Cr + V((1.2, 1.2, 1.0)), Cr + V((0, 9, 0.2)), 30), (Cr + V((0.4, -1.5, 1.2)), Cr + V((0, 9, 0.2)), 22), ev_craters(0, 0, 0, 0, band=True), "dissolve"),
    (1122, 1189, "fade", "LS2", (Fd + V((0, 0, 1.6)), Fd + V((0, 12, -0.2)), 28), (Fd + V((0.8, 0.6, 1.8)), Fd + V((0, 12, -0.2)), 28), ev_fade, "follow"),
    (1189, 1250, "fade", "LS2", (Fd + V((0.8, 0.6, 1.8)), Fd + V((0, 12, -0.2)), 28), (Fd + V((0.2, 3.0, 1.2)), Fd + V((0, 12, -0.6)), 28), ev_fade, "follow"),
    (1250, 1306, "fade", "LS2", (Fd + V((0.2, 3.0, 1.2)), Fd + V((0, 12, -0.6)), 28), (Fd + V((0, -1.0, 1.4)), Fd + V((0, 12, -0.2)), 26), ev_fade, "dissolve"),
    (1306, 1371, "tags", "LS2", (Tg + V((0.1, 1.0, 3.6)), Tg + V((0.15, 5.2, -0.1)), 20), (Tg + V((0.15, 1.9, 2.9)), Tg + V((0.15, 5.2, 0.0)), 23), ev_tags, "dissolve"),
    (1371, 1414, "ringstamp", "LS2", (Rs + V((0.6, -1.0, 0.9)), Rs + V((0, 11, -0.3)), 22), (Rs + V((1.1, 0.4, 1.3)), Rs + V((0, 11, -0.3)), 22), ev_ringstamp, "dissolve"),
    (1414, 1460, "seafloor", "LS7", (Se + V((0.4, 0.8, 0.35)), Se + V((0.8, -2.4, 0.18)), 26), (Se + V((0.4, 0.8, 0.5)), Se + V((0.4, -14, 7.5)), 13), ev_none, "dissolve"),
    (1460, 1511, "dawn", "LS8", (Da + V((0, 0.3, 0.9)), Da + V((30, -2.0, 8)), 22), (Da + V((-1.4, 0.4, 1.1)), Da + V((30, -2.0, 8)), 22), ev_dawn, "whip"),
    (1511, 1575, "bedroom", "BED_DAWN", (Bo + V((0.55, 0.15, 1.05)), Bo + V((0.8, 3.2, 1.6)), 28), (Bo + V((0.6, 0.6, 1.1)), Bo + V((0.8, 3.2, 1.75)), 28), ev_bed_dawn, "fade"),
]
assert len(VIEWS) == 31 and VIEWS[-1][1] == 1575

if pc.CEL:
    pc.cel_ink(sc)
os.makedirs(OUT, exist_ok=True)
frames = ONLY or ([int((v[0] + v[1]) / 2) for v in VIEWS if START <= int((v[0] + v[1]) / 2) < END] if CHECK else range(START, END))
current = None
for f in frames:
    vi = next(i for i, v in enumerate(VIEWS) if v[0] <= f < v[1])
    a, b, st, state, (p0, t0, l0), (p1, t1, l1), ev, join = VIEWS[vi]
    if current != vi:
        for nm, col in COL.items():
            col.hide_render = nm != st
        pc.set_world(*STATES[state])
        current = vi
    t = (f - a) / max(1, b - a - 1)
    e = ease(t)
    cam.location = p0.lerp(p1, e)
    aim.location = t0.lerp(t1, e)
    cam.data.lens = l0 + (l1 - l0) * e
    cam.data.dof.aperture_fstop = 11
    ev(t, f)
    pc.face_cards(cam.location)
    sc.render.filepath = os.path.join(OUT, f"f_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f, flush=True)
