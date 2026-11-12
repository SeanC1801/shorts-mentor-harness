"""EP004 render: storyboard v1 (approved 2026-11-11), 30 fps, 1607 frames, cel look (look test approved).
Built scene by scene: each scene's views are added here after the previous scene is approved.
Writes PNG frames; joins, captions, fades and narration are added by scripts/finish_ep004.py.

usage: blender -b -P renderer-blender/ep004_render.py -- OUT_DIR [scale%] [start] [end] [--frames a,b,c]   (frames on the storyboard v2 clock)
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import papercraft as pc
pc.CEL = True
import ep004_sets as s4

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep004"]
OUT = argv[0]
SCALE = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 100
START = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 0
END = int(argv[3]) if len(argv) > 3 and argv[3].isdigit() else 1607
CHECK = "--views" in argv
ONLY = [int(a) for a in argv[argv.index("--frames") + 1].split(",")] if "--frames" in argv else None
random.seed(11)
sc = pc.setup(SCALE, samples=32)
sc.render.use_persistent_data = True
cam, aim = pc.camera()
V = Vector


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def lerp(a, b, t): return a + (b - a) * t


def deg(*a): return tuple(math.radians(x) for x in a)


# lighting states: world texture, strength, grade, saturation (sun energy is set per stage)
STATES = {"LS1": ("ep4_sky_rain_eq.png", 1.8, "#F2F4F9", 1.15), "LS5": ("ep4_sky_bright_eq.png", 0.9, "#F1EADC", 1.08),
          "LS2": ("sky_day_eq.png", 1.0, "#F6EBD8", 1.1), "LS3": ("ep4_sky_high_eq.png", 1.0, "#E9EFF8", 1.08),
          "LS4": ("sky_dawn_eq.png", 0.85, "#F6E0D4", 1.1),
          "LS5i": ("ep4_sky_thin_eq.png", 0.9, "#F1EADC", 1.08)}   # LS5 lighting, inland sky card without painted clouds
COL, H = {}, {}


def stage(name, fn, O):
    COL[name] = pc.collection("ST-" + name)
    H[name] = fn(V(O)) or {}
    H[name]["O"] = V(O)


def show(objs, on):
    for o in objs:
        if o is not None:
            o.hide_render = not on


# ---------------- stages ----------------
def st_window(O):
    W = s4.window_set(O)
    W["sun"] = pc.light("sun", "SUN", O + V((0, 0, 10)), 4.8, "#E8EDF6", rot=deg(35, -40, 0), angle=8)
    show(W["kid_wistful"], False)
    W["lamp"].data.energy = 260
    return W


stage("window", st_window, (0, 0, 0))
stage("sea", s4.sea_set, (0, 600, 0))
stage("sky", s4.high_sky_set, (0, 1400, 0))
stage("coast", s4.coast_town_set, (0, 2200, 0))
stage("shore", s4.shore_set, (0, 3000, 0))
stage("inland", s4.inland_set, (0, 3800, 0))
Wn, Sea, Sky, Co, Sh, In = H["window"], H["sea"], H["sky"], H["coast"], H["shore"], H["inland"]
Wo, So, Ko, Cs, Ho, Io = Wn["O"], Sea["O"], Sky["O"], Co["O"], Sh["O"], In["O"]
Kc = Sky["C"]


def rain_fall(f):
    """Rain streaks fall continuously (wrapping inside their band)."""
    for o, base in Wn["streaks"]:
        span = 4.4
        z = base.z - ((f * 0.32 + (base.x * 7.13 % 1.0) * span) % span)
        o.location = V((base.x, base.y, z if z > Wo.z - 0.9 else z + span))


# hero drop path on the window set (S01 V1 slides down, V2 rewinds up and flies to the grey cloud)
GLASS_Y = 0.045
P_TOP = V((0.12, GLASS_Y, 1.30))      # where it starts in V1
P_LOW = V((0.12, GLASS_Y, 1.12))      # where V1 ends (slid down)
P_EDGE = V((0.14, GLASS_Y, 1.80))     # top of the glass (V2 rewinds to here)
PATH = [P_EDGE, V((0.2, -0.6, 2.2)), V((0.3, -1.25, 3.1)), V((0.4, -1.9, 5.2)), V((0.5, -2.8, 8.2)), V((0.6, -3.4, 10.4))]


def along(path, u):
    u = max(0.0, min(1.0, u)) * (len(path) - 1)
    i = min(int(u), len(path) - 2)
    return path[i].lerp(path[i + 1], u - i)


def ev_s01v1(t, f):
    rain_fall(f)
    body, hl = Wn["hero"]
    p = P_TOP.lerp(P_LOW, ease(t))
    body.location, hl.location = p, p + V((-0.015, -0.02, 0.03))
    aim.location = p
    show(Wn["kid_curious"], True)


def drop_v2(t):
    if t < 0.3:
        return P_LOW.lerp(P_EDGE, ease(t / 0.3)), 1.0
    u = (t - 0.3) / 0.7
    return along(PATH, ease(u) * 0.85 + u * 0.15), 1.0 + 3.0 * u   # grows as it flies, so it keeps its size on screen


def ev_s01v2(t, f):
    rain_fall(f)
    body, hl = Wn["hero"]
    p, s = drop_v2(t)
    body.location, hl.location = p, p + V((-0.015 * s, -0.02 * s, 0.03 * s))
    body.scale = (0.9 * s, 0.35 + 0.55 * min(1, max(0, (t - 0.3) / 0.2)), 1.25 * s) if False else (0.9 * s, 0.35 * s if t < 0.3 else 0.9 * s, 1.25 * s)
    hl.scale = (s, 0.3 * s, 1.4 * s)
    # camera: in front of the glass, then below and behind the drop, looking up as it climbs
    u = ease(max(0.0, (t - 0.2) / 0.8))
    off = V((0.06, -0.80, 0.02)).lerp(V((0.15, -1.6, -1.5)), u)
    cam.location = p + off
    aim.location = p
    cam.data.lens = lerp(50, 30, u)


def ev_s01v3(t, f):
    """Sea: the drop falls out of the white cloud and lands in the sea; the camera dives with it."""
    body, hl = Sea["drop"]
    land = 0.82
    if t < land:
        z = lerp(28.5, 0.05, ease(t / land) * 0.7 + (t / land) * 0.3)
        p = So + V((0, 0, z))
    else:
        p = So + V((0, 0, -1.0))
    body.location, hl.location = p, p + V((-0.05, -0.06, 0.08))
    body.hide_render = hl.hide_render = t >= land
    for k, r in enumerate(Sea["ripples"]):
        u = (t - land - 0.04 * k) / (1 - land)
        r.hide_render = u <= 0
        if u > 0:
            s = 0.2 + 1.2 * u
            r.scale = (s, s, 1)
    c = min(t / land, 1.0)
    # camera rides beside the drop looking ahead and a little down: sky, sun and sea stay in frame
    dz = max(p.z - So.z, 0.0) if t < land else 0.0
    cam_z = max(dz + lerp(0.7, 1.3, ease(c)), 1.4)
    cam.location = So + V((0.2, lerp(-2.0, -3.2, ease(c)), cam_z))
    aim.location = So + V((0, lerp(5.0, 3.0, ease(c)), max(dz - 1.4, 0.15)))
    cam.data.lens = lerp(24, 26, c)
    for w, base, ph in Sea["waves"]:
        w.location = base + V((0, 0, 0.06 * math.sin(f * 0.18 + ph)))
    for k, g in enumerate(Sea["glints"]):
        g.hide_render = ((f // 3 + k) % 5) == 0


def sea_life(f):
    for w, base, ph in Sea["waves"]:
        w.location = base + V((0, 0, 0.06 * math.sin(f * 0.18 + ph)))
    for k, g in enumerate(Sea["glints"]):
        g.hide_render = ((f // 3 + k) % 5) == 0


def ripples_after(f):
    """S01's landing rings keep spreading into S02, then vanish."""
    for k, r in enumerate(Sea["ripples"]):
        u = ((f - 86) / 40 - 0.82 - 0.04 * k) / 0.18
        r.hide_render = u <= 0 or u > 2.2
        if 0 < u <= 2.2:
            s = 0.2 + 1.2 * u
            r.scale = (s, s, 1)


def ev_s02(t, f):
    sea_life(f)
    ripples_after(f)
    s4.curl_step(Sea["curls"], f, 176, 300, rise=0.06, alpha=0.17, stagger=35)


def sky_life(f):
    for w, base, v in Sky["wisps"]:
        w.location = base + V((v * (f - 259), 0, 0))


def droplets(f):
    """Droplets pop on at the curl tops (275-300), drift together and clump (306-356), then fade into the cloud (356-380)."""
    for d, a, b, ph in Sky["drops"]:
        on = 272 + ph * 30
        d.hide_render = f < on or f >= 384
        if d.hide_render:
            continue
        g = ease((f - 306 - ph * 8) / 46)
        d.location = a.lerp(b, g) + V((0, 0, 0.03 * math.sin(f * 0.3 + ph * 20)))
        tw = 1 + 0.35 * math.sin(f * 0.9 + ph * 40)
        pop = min(1.0, (f - on) / 4)
        fade = 1 - ease((f - 360) / 22)
        d.scale = [pop * tw * fade] * 3


def cloud_grow(f):
    for k, p in enumerate(Sky["puffs"]):
        g = ease((f - 352 - 1.6 * k) / 22)
        p.hide_render = g <= 0
        bs = p["base_scale"]
        p.scale = (bs[0] * g, bs[1] * g, bs[2] * g)


def ev_s03(t, f):
    sky_life(f)
    s4.curl_step(Sky["curls"], f, 252, 300, rise=0.028, alpha=0.2, stagger=14)
    droplets(f)
    cloud_grow(f)


def clouds_drift(f):
    for puffs, base in Co["clouds"]:
        d = V((0, 1.0 * min(f - 406, 64) + 0.12 * max(0, f - 470), 0))
        for p in puffs:
            if "b" not in p:
                p["b"] = tuple(p.location)
            p.location = V(p["b"]) + d


def wind_blow(f):
    for o, base in Co["wind"]:
        y = (base.y - Cs.y + 60 + (f - 406) * 2.2) % 100 - 60
        o.location = V((base.x, Cs.y + y, base.z))
        o.hide_render = f >= 470


def coast_rain(f, on):
    for o, base in Co["rain"]:
        o.hide_render = not on
        if on:
            z = (base.z - Cs.z - (f * 0.9 + (base.x * 3.7 % 1) * 18)) % 18
            o.location = V((base.x, base.y, Cs.z + z))


KID_WIN = Cs + s4.KID_HOUSE + V((0.4, -2.12, 1.6))


def ev_s04v1(t, f):
    clouds_drift(f); wind_blow(f); coast_rain(f, False)
    Co["drop"][0].hide_render = Co["drop"][1].hide_render = True


def ev_s04v2a(t, f):
    clouds_drift(f); wind_blow(f); coast_rain(f, True)
    body, hl = Co["drop"]
    body.hide_render = hl.hide_render = False
    a = Cs + V((3.0, 14.0, 17.0))
    p = a.lerp(KID_WIN + V((0, -0.7, 0.15)), ease(t) * 0.8 + t * 0.2)
    body.location, hl.location = p, p + V((-0.08, -0.1, 0.12))
    off = V((-3.0, -8.0, 2.6)).lerp(V((0.1, -3.4, 0.0)), ease(t))
    cam.location = p + off
    aim.location = p.lerp(KID_WIN, ease(t))
    cam.data.lens = lerp(24, 32, ease(t))


def ev_s04v2b(t, f):
    rain_fall(f)
    show(Wn["kid_curious"], True)
    body, hl = Wn["hero"]
    land = 0.25
    if t < land:
        p = V((0.1, -0.6, 1.95)).lerp(V((0.12, GLASS_Y, 1.22)), ease(t / land))
        body.scale, hl.scale = (0.9, 0.9, 1.25), (1, 0.3, 1.4)
    else:
        p = V((0.12, GLASS_Y, 1.22)).lerp(V((0.12, GLASS_Y, 1.16)), ease((t - land) / (1 - land)))
        sq = max(0.0, 1 - (t - land) / 0.08)   # a small squash as it hits the glass
        body.scale, hl.scale = (0.9 * (1 + 0.3 * sq), 0.35, 1.25 * (1 - 0.2 * sq)), (1, 0.3, 1.4)
    body.location, hl.location = Wo + p, Wo + p + V((-0.015, -0.02, 0.03))


def waterline_y(zw):
    """Where the draining water meets the seabed along the bay's centre line."""
    y = 6.0
    while y < 300 and Sh["z"](0, y) > zw:
        y += 0.5
    return y


def drain(f):
    u = max(0.0, min(1.0, (f - 538) / 28))
    zw = -0.3 - 40 * (u ** 1.8)
    Sh["water"].location = Sh["water_base"] + V((0, 30 * u, zw + 0.3))
    Sh["water"].hide_render = u >= 1
    Sh["foam"].location = V((Ho.x, Ho.y + waterline_y(zw) - 0.3, Ho.z + zw + 0.03))
    Sh["foam"].hide_render = u >= 0.98
    return u


def dawn(f):
    """Night to dawn in a fast time-lapse (S05 V1), then hold dawn."""
    u = ease((f - 536) / 30)
    night, day = pc.hexcol("#5C6898"), pc.hexcol("#F6E0D4")
    pc.G_RGB.outputs[0].default_value = tuple(lerp(night[i], day[i], u) for i in range(3)) + (1,)
    pc.WORLD.node_tree.nodes["Background"].inputs[1].default_value = lerp(0.35, 0.85, u)
    Sh["sun"].data.energy = lerp(0.6, 3.0, u)
    Sh["sun_card"].location = Sh["sun_base"] + V((0, 0, lerp(-4, 9, u)))


def ev_s05(t, f):
    drain(f)
    dawn(f)
    show(BOAT, True); show(Sh["boat_side"], False)
    near = (cam.location - Sh["kid"][0].location).length < 5.0 and f < 570   # no pop past the lens in V1
    show(Sh["kid"], not near); show(Sh["kid_back"], False)


BOAT = [o for o in COL["shore"].objects if o.name.startswith("rowboat")]
BOAT_ROT = {o.name: tuple(o.rotation_euler) for o in BOAT}


def ev_s06(t, f, kid=False):
    drain(f)                                   # past the drain: no water left
    Sh["sun"].data.energy = 4.2
    Sh["sun_card"].hide_render = True
    show(BOAT, False); show(Sh["boat_side"], True)   # S06 only: the open hull lying on its side
    show(Sh["kid"], False); show(Sh["kid_back"], kid)


def puff_pop(puffs, appear, vanish, keep=()):
    """Each puff pops in at appear(k) (0.5 -> 1 of its size over 6 frames) and shrinks away from vanish(k)
    over 5 frames; puffs in `keep` only shrink to 70%, so the cloud thins rather than disappears."""
    n = len(puffs)
    for k, p in enumerate(puffs):
        a, v = appear(k, n), vanish(k, n)
        s = 0.0 if a is None or F < a else 0.5 + 0.5 * ease((F - a) / 6)
        if v is not None:
            g = ease((F - v) / 5)
            s *= 1 - 0.3 * g if k in keep else 1 - g
        p.hide_render = s < 0.05
        b = p["base_scale"]
        p.scale = (b[0] * s, b[1] * s, b[2] * s)


F = 0


def ev_s07(t, f, kid=False):
    """Inland (v1 clock): curls lift off the lake, then the soil (~742), then the plants one by one (~757);
    a small patchy cloud forms (V3, 768-812); the clouds thin and gaps open (V4, 'thin out' ~829-850)."""
    global F
    F = f
    s4.curl_step(In["c_lake"], f, 668, 800, rise=0.035, alpha=0.32, stagger=36)
    s4.curl_step(In["c_soil"], f, 739, 800, rise=0.03, alpha=0.34, stagger=12)
    s4.curl_step(In["c_plant"], f, 754, 800, rise=0.025, alpha=0.36, stagger=14)
    order = lambda k, n: (k * 7) % n
    n_main = len(In["cl_main"])
    puff_pop(In["cl_main"], lambda k, n: None if (k % 3 == 1 and k != n - 1) else 772 + 26 * k / n,
             lambda k, n: 820 + 26 * order(k, n) / n, keep=(n_main - 1, 0, 6))
    for cs in In["cl_side"]:
        puff_pop(cs, lambda k, n: -1, lambda k, n: 818 + 30 * order(k, n) / n, keep=(len(cs) - 1, 2))
    show(In["kid"], kid)


def ev_none(t, f):
    pass


# (start, end, stage, state, (pos0, tgt0, lens0), (pos1, tgt1, lens1), event, f-stop) -- events may override the camera
VIEWS = [
    # S01 V1: slow push-in on the drop sliding down the glass; the kid behind it is softly out of focus
    (0, 44, "window", "LS1", (Wo + V((0.22, -1.15, 1.26)), P_TOP, 44), (Wo + V((0.17, -0.82, 1.15)), P_LOW, 50), ev_s01v1, 1.4),
    # S01 V2: the drop rewinds up the glass and lifts off over the gutter into the grey cloud; the camera tilts up with it
    (44, 86, "window", "LS1", None, None, ev_s01v2, 5.6),
    # S01 V3: out of a white cloud, the drop falls to a sunny sea; the camera dives with it to the surface
    (86, 127, "sea", "LS2", None, None, ev_s01v3, 8.0),
    # S02 V1: low glide over the waves toward the sun; glints flicker as the sea warms
    (127, 190, "sea", "LS2", (So + V((0.2, -3.2, 1.4)), So + V((0, 3.0, 0.15)), 26), (So + V((0.2, 7.0, 1.0)), So + V((0, 40, 0.9)), 24), ev_s02, 8.0),
    # S02 V2: faint vapor curls rise off the surface; the camera cranes up with them
    (190, 259, "sea", "LS2", (So + V((0.2, 7.0, 1.0)), So + V((0, 40, 0.9)), 24), (So + V((0.2, 8.6, 5.0)), So + V((0, 15, 9.5)), 24), ev_s02, 8.0),
    # S03 V1: high up, the curls slow and turn into sparkling droplets; the camera keeps rising, slow orbit
    (259, 306, "sky", "LS3", (Ko + V((0.0, -0.5, -3.2)), Kc + V((0, 0, -1.2)), 24), (Ko + V((1.3, 0.2, -0.6)), Kc + V((0, 0, -0.4)), 24), ev_s03, 8.0),
    # S03 V2: the droplets drift together and clump; push in
    (306, 356, "sky", "LS3", (Ko + V((1.3, 0.2, -0.6)), Kc + V((0, 0, -0.4)), 24), (Ko + V((0.7, 4.2, -0.1)), Kc + V((0, 0, 0.05)), 30), ev_s03, 8.0),
    # S03 V3: pull back to a wide: a fluffy white cloud has formed over the sea
    (356, 406, "sky", "LS3", (Ko + V((0.7, 4.2, -0.1)), Kc + V((0, 0, 0.05)), 30), (Ko + V((-1.4, -0.6, 1.5)), Kc + V((0, 0, -0.3)), 24), ev_s03, 8.0),
    # S04 V1: wind pushes the clouds off the sea, over the coast toward the town; track alongside
    (406, 470, "coast", "LS3", (Cs + V((-26, -52, 24)), Cs + V((2, -40, 18)), 24), (Cs + V((-24, 8, 22)), Cs + V((4, 26, 6)), 24), ev_s04v1, 11.0),
    # S04 V2a: rain over the town; follow one drop down toward the kid's window
    (470, 505, "coast", "LS1", None, None, ev_s04v2a, 11.0),
    # S04 V2b: the drop lands on the kid's window; settle on the kid behind the glass
    (505, 536, "window", "LS1", (Wo + V((0.3, -2.1, 1.2)), Wo + V((0.26, 0.045, 0.98)), 36), (Wo + V((0.34, -1.5, 1.1)), Wo + V((0.3, 0.3, 0.84)), 38), ev_s04v2b, 2.8),
    # S05 V1: night to dawn in a fast time-lapse while the whole sea drains away; whip in, then a fast pull up and back
    (536, 570, "shore", "LS4", (Ho + V((2.6, 3.4, 0.9)), Ho + V((0, 30, -0.5)), 24), (Ho + V((1.2, -6.5, 5.5)), Ho + V((0, 35, -7)), 22), ev_s05, 11.0),
    # S05 V2: the kid on the shore flings both arms up (shocked); quick push-in
    (570, 600, "shore", "LS4", (Ho + V((0.5, -1.5, 1.25)), Ho + V((0, 2.6, 0.95)), 30), (Ho + V((0.45, -0.6, 1.05)), Ho + V((0, 2.6, 0.95)), 32), ev_s05, 11.0),
    # S06 V1: low drift across the empty seafloor (damp sand, shells, the rowboat on its side); nothing rises
    (600, 633, "shore", "LS5", (Ho + V((-3.0, 11.0, 0.4)), Ho + V((5.0, 19, -2.2)), 24), (Ho + V((0.0, 13.0, 0.2)), Ho + V((5.0, 21, -2.5)), 24), lambda t, f: ev_s06(t, f, False), 11.0),
    # S06 V2: the kid from behind at the shore, the empty bowl ahead; slow crane up, dissolve inland
    (633, 665, "shore", "LS5", (Ho + V((0.6, 1.8, 0.9)), Ho + V((0.4, 20, -1.2)), 24), (Ho + V((0.6, 1.0, 3.2)), Ho + V((0.4, 26, -0.6)), 24), lambda t, f: ev_s06(t, f, True), 11.0),
    # S07 V1: inland, a lake; a few faint curls lift off it; pan across the lake
    (665, 720, "inland", "LS5i", (Io + V((-6.5, 3.5, 1.5)), Io + V((-9.5, 14.0, -0.4)), 24), (Io + V((-5.0, 3.5, 1.5)), Io + V((-6.0, 15.0, -0.2)), 24), ev_s07, 11.0),
    # S07 V2: the pan continues onto the field and the tree; curls from the soil, then the plants; slight push-in
    (720, 768, "inland", "LS5i", (Io + V((-5.0, 3.5, 1.5)), Io + V((-6.0, 15.0, -0.2)), 24), (Io + V((-3.0, 4.0, 1.7)), Io + V((8.0, 16.0, 0.4)), 24), ev_s07, 11.0),
    # S07 V3: tilt up and push toward the sky: a cloud still forms, but small and patchy
    (768, 812, "inland", "LS5i", (Io + V((-3.0, 4.0, 1.7)), Io + V((8.0, 16.0, 0.4)), 24), (Io + V((1.0, 4.0, 2.6)), Io + V((7.0, 36.0, 13.0)), 24), ev_s07, 11.0),
    # S07 V4: low angle on the kid pointing up (worried) as the clouds thin and gaps open; slow push-in
    (812, 855, "inland", "LS5i", (Io + V((3.5, 1.2, 0.35)), Io + V((3.95, 8.2, 1.0)), 24), (Io + V((3.5, 1.9, 0.42)), Io + V((4.05, 9.0, 1.15)), 24), lambda t, f: ev_s07(t, f, True), 11.0),
]
LAST = VIEWS[-1][1]

# Storyboard v2 (2026-11-11) re-timed every view to the script v2 narration. VIEWS keep the v1 clock (their
# events were tuned on it); each output frame f maps linearly, view by view, onto that clock.
V1_STARTS = [0, 44, 86, 127, 190, 259, 306, 356, 406, 470, 536, 570, 600, 633, 665, 720, 768, 812, 855, 912, 968, 1022, 1086, 1136, 1200, 1265, 1332, 1398, 1446, 1484, 1522, 1566, 1607]
V2_STARTS = [0, 42, 81, 120, 184, 254, 301, 351, 401, 471, 543, 576, 606, 640, 672, 727, 774, 818, 861, 918, 975, 1029, 1091, 1140, 1204, 1269, 1335, 1401, 1449, 1488, 1526, 1568, 1607]


def to_v1(f):
    i = max(k for k in range(len(V2_STARTS) - 1) if V2_STARTS[k] <= f)
    a2, b2, a1, b1 = V2_STARTS[i], V2_STARTS[i + 1], V1_STARTS[i], V1_STARTS[i + 1]
    return a1 + (f - a2) * (b1 - a1) / (b2 - a2)


LAST2 = V2_STARTS[V1_STARTS.index(LAST)]

pc.cel_ink(sc)
os.makedirs(OUT, exist_ok=True)
frames = ONLY or range(START, min(END, LAST2))
current = None
for f2 in frames:
    f = to_v1(f2)
    vi = next(i for i, v in enumerate(VIEWS) if v[0] <= f < v[1])
    a, b, st, state, k0, k1, ev, fstop = VIEWS[vi]
    if current != vi:
        for nm, col in COL.items():
            col.hide_render = nm != st
        pc.set_world(*STATES[state])
        current = vi
    t = (f - a) / max(1, b - a - 1)
    if k0:
        e = ease(t)
        cam.location = k0[0].lerp(k1[0], e)
        aim.location = k0[1].lerp(k1[1], e)
        cam.data.lens = k0[2] + (k1[2] - k0[2]) * e
    cam.data.dof.aperture_fstop = fstop
    ev(t, f)
    pc.face_cards(cam.location)
    sc.render.filepath = os.path.join(OUT, f"f_{f2:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f2, flush=True)
