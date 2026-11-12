"""EP004 render: storyboard v1 (approved 2026-11-11), 30 fps, 1607 frames, cel look (look test approved).
Built scene by scene: each scene's views are added here after the previous scene is approved.
Writes PNG frames; joins, captions, fades and narration are added by scripts/finish_ep004.py.

usage: blender -b -P renderer-blender/ep004_render.py -- OUT_DIR [scale%] [start] [end] [--frames a,b,c]   (frames on the storyboard v2 clock)
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector, Matrix
import papercraft as pc
pc.CEL = True
import ep004_sets as s4

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep004"]
OUT = argv[0]
_pos = []
for _a in argv[1:]:
    if _a.startswith("--"):
        break
    _pos.append(_a)
for _a in _pos:   # a range passed as one argument ("861 917") once made every job render from frame 0
    if not _a.isdigit():
        sys.exit(f"ep004_render: argument {_a!r} is not a whole number (expected: OUT_DIR [scale] [start] [end])")
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
          "LS5i": ("ep4_sky_thin_eq.png", 0.9, "#F1EADC", 1.08),   # LS5 lighting, inland sky card without painted clouds
          "LS5d": ("ep4_sky_dry_eq.png", 0.9, "#F1EADC", 1.08),    # LS5 lighting, BG-DRY-PLAIN's clear day sky
          "LS6": ("ep4_sky_glare_eq.png", 1.0, "#FFF0D8", 1.0),    # harsh noon glare: bleached yellow-white sky
          "LS8": ("space_eq.png", 0.35, "#E6E8FF", 1.1),           # cool deep space: star card (EP003's, reused)
          "LS7": ("ep4_sky_night_eq.png", 1.0, "#B4BEEA", 1.0)}    # cold clear night: deep blue-violet star card
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
stage("plain", s4.dry_plain_set, (0, 4600, 0))
stage("space", s4.space_earth_set, (0, 8000, 0))
Sp = H["space"]; Eo = Sp["O"]
Wn, Sea, Sky, Co, Sh, In, Pl = H["window"], H["sea"], H["sky"], H["coast"], H["shore"], H["inland"], H["plain"]
Wo, So, Ko, Cs, Ho, Io, Po = Wn["O"], Sea["O"], Sky["O"], Co["O"], Sh["O"], In["O"], Pl["O"]
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


def ev_s08(t, f):
    """Inland drying (v1 clock 855-1022). V1: the thinned cloud drifts in and drops only a sparse sprinkle.
    V2 (912-968, 'drier ground' ~943-951): ridges settle, soil and leaves dry, plants droop, the lake shrinks
    to a dry rim, cracks spread from the near edge of the field to the far edge. V3 (968-1022, 'even less
    water to give' ~981-1020): one curl tries to rise and fizzles out; the last clouds clear."""
    ev_s07(t, f, False)                        # same clouds (already thinned), S07 curls hidden by now
    # clouds drift toward the camera; in V3 the side clouds clear and the main one shrinks to a scrap
    drift = V((0, -0.07 * (f - 855), 0))
    clear = ease((f - 972) / 36)
    for p in In["cl_main"]:
        p.location = V(p["base_loc"]) + drift
        p.scale = p.scale * (1 - 0.55 * clear)
    for cs in In["cl_side"]:
        for p in cs:
            p.location = V(p["base_loc"]) + drift
            p.scale = p.scale * (1 - clear)
            p.hide_render = p.hide_render or clear > 0.97
    # sparse sprinkle under the cloud (V1 into early V2)
    for o, p0, ph in In["sprinkle"]:
        age = (f - 852 - ph * 40) % 34
        on = 852 + ph * 40 <= f < 935
        o.hide_render = not on
        if on:
            o.location = p0 + drift + V((0, -0.08 * age, -0.4 * age))
    # drying
    u = ease((f - 914) / 40)
    for k, sock in In["dry"].items():
        if sock is not None:
            sock.default_value = u * {"leaf": 0.85, "stem": 0.85, "crown": 0.45}.get(k, 1.0)
    settle = ease((f - 912) / 16)
    for rg in In["ridges"]:
        rg.scale.z = rg["base_sz"] * (1 - 0.65 * settle)
    from mathutils import Matrix
    for k, (stem, leaf, base, axis, amt, lsc) in enumerate(In["droop"]):
        d = ease((f - 920 - (k % 9) * 2) / 26) * amt
        R = Matrix.Rotation(math.radians(48) * d, 4, axis)          # the stem bends over
        RL = Matrix.Rotation(math.radians(95) * d, 4, axis)         # the leaf hangs further, off the stem tip
        stem.location = base + R @ V((0, 0, 0.12))
        stem.rotation_euler = R.to_euler()
        leaf.location = base + R @ V((0, 0, 0.24)) + RL @ V((0, 0, 0.06)) - V((0, 0, 0.05 * d))
        leaf.rotation_euler = RL.to_euler()
        leaf.scale = (lsc[0] * (1 - 0.3 * d), lsc[1] * (1 - 0.3 * d), lsc[2] * (1 - 0.1 * d))
    for cb in In["crown"]:
        b = cb["base_scale"]; sh = 1 - 0.1 * u
        cb.scale = (b[0] * sh, b[1] * sh, b[2] * sh)
    lk = ease((f - 922) / 40)
    loc0, sc0 = In["lake_base"]
    In["lake"].location = loc0 + V((0, 0, -0.24 * lk))
    In["lake"].scale = (sc0[0] * (1 - 0.32 * lk), sc0[1] * (1 - 0.32 * lk), sc0[2])
    lc = In["O"] + V((s4.LAKE_C.x, s4.LAKE_C.y, 0))
    for g, gb in zip(In["glints"], In["glint_base"]):
        q = lc + (gb - lc) * (1 - 0.32 * lk)
        g.location = V((q.x, q.y, gb.z - 0.24 * lk))
    for segs, t0 in In["cracks"]:
        n_on = int(max(0.0, (f - t0) / 2.0)) + (1 if f >= t0 else 0)
        for i, sg in enumerate(segs):
            sg.hide_render = i >= n_on
    # V3 camera in two parts: a slow push toward the curl while it fizzles, then the crane up to the clear sky
    if 968 <= f < 1022:
        tv = (f - 968) / 53
        pa, pb, pc_ = Io + V((9.0, 9.0, 1.6)), Io + V((9.15, 9.9, 1.45)), Io + V((9.6, 11.5, 3.8))
        aa, ab, ac = Io + V((10.5, 20.0, 0.1)), Io + V((10.0, 17.0, 0.5)), Io + V((11.0, 30.0, 15.0))
        if tv < 0.4:
            e = ease(tv / 0.4); cam.location, aim.location = pa.lerp(pb, e), aa.lerp(ab, e)
        else:
            e = ease((tv - 0.4) / 0.6); cam.location, aim.location = pb.lerp(pc_, e), ab.lerp(ac, e)
    # the fizzle curl: rises slowly, flickers, shrinks and fades out
    (o, m, base, ph), = In["fizzle"]
    age = f - 968
    if 0 <= age < 34:
        o.hide_render = False
        fade = min(1.0, age / 8) * max(0.0, 1 - max(0, age - 14) / 16)
        o.location = base + V((0.06 * math.sin(age * 0.2), 0, 0.012 * age))
        o.scale = (1 + 0.2 * math.sin(age * 0.5), 1, max(0.25, 1 - max(0, age - 16) / 30))
        flick = 1 + 0.35 * math.sin(age * 1.3)
        next(nd for nd in m.node_tree.nodes if nd.bl_idname == "ShaderNodeMixShader").inputs[0].default_value = 0.4 * fade * flick
    else:
        o.hide_render = True


def face_cam(o):
    """Turn a billboard (normal local -Y) fully toward the camera."""
    o.rotation_euler = (cam.location - o.location).to_track_quat("-Y", "Z").to_euler()


def ev_s09(t, f):
    """BG-DRY-PLAIN, S09 (v1 clock 1022-1136; 'calmer' ~1069, 'But' ~1089, 'second job' ~1114-1127).
    V1: slow push-in on the kid standing deadpan under a calm clear sky while a thin cloud slides over the sun and
    the ground dims; from ~1068 the camera starts tilting up toward the sun.
    V2 (LS6): on 'But' the cloud slides off and the glare snaps back; the tilt settles on the sun, flare ghosts sweep
    across the frame; from ~1110 a push into the glare (zoom plus a growing bloom) that S10 leaves from."""
    P = Pl
    plain_day("stand")
    plain_s10_off()                                             # S10's layer, beams and shimmer stay hidden here
    show(P["veil"], True)
    P["sun"].rotation_euler = s4.SUN_DIR.to_track_quat("Z", "Y").to_euler()
    P["sun_disc"].location, P["glow"].location = Po + s4.SUN_DIR * 400, Po + s4.SUN_DIR * 430
    k = ease((f - 1022) / 58)
    pos = (Po + V((0.55, 1.0, 0.78))).lerp(Po + V((0.25, 2.7, 0.82)), k)
    w = ease((f - 1068) / 40)                                   # tilt from the kid up to the sun
    d = (Po + V((0.0, 6.0, 0.8)) - pos).normalized().lerp(s4.SUN_DIR, w).normalized()
    push = ease((f - 1110) / 26) ** 1.6
    cam.location = pos + s4.SUN_DIR * 2.0 * push
    aim.location = cam.location + d * lerp(3.3, 60.0, w)
    cam.data.lens = lerp(26.0, 28.0, k) + 55.0 * push
    # the thin cloud: from the right over the sun (1040-1080), then off to the left on 'But' (1086-1095)
    u = 1 - ease((f - 1040) / 40) if f < 1086 else -1.4 * ease((f - 1086) / 9)
    side = s4.SUN_DIR.cross(V((0, 0, 1))).normalized()
    for p in P["veil"]:
        p.location = V(p["base_loc"]) + side * 16.0 * u
    vc = P["veil_c"] + side * 16.0 * u
    ang = math.degrees((vc - cam.location).angle(s4.SUN_DIR))
    cover = 1 - ease((ang - 3.0) / 7.0)
    glare = ease((f - 1087) / 3) if f >= 1086 else 0.0
    # light: dims under the cloud, snaps brighter for the glare
    P["sun"].data.energy = (4.2 + 1.3 * glare) * (1 - 0.5 * cover)
    g0 = pc.hexcol(STATES["LS6" if f >= 1086 else "LS5d"][2])
    dim = 1 - 0.13 * cover
    pc.G_RGB.outputs[0].default_value = (g0[0] * dim, g0[1] * dim, g0[2] * dim, 1)
    s = (1 + 0.5 * glare) * (1 - 0.45 * cover) * (1 + 6.0 * push)
    P["glow"].scale = (s, s, s)
    face_cam(P["sun_disc"]); face_cam(P["glow"])
    # flare ghosts on the line from the sun through the frame centre, only while the sun is near the frame
    fwd = (aim.location - cam.location).normalized()
    rt = fwd.cross(V((0, 0, 1))).normalized(); up = rt.cross(fwd)
    cz = max(1e-3, s4.SUN_DIR.dot(fwd))
    sx, sy = s4.SUN_DIR.dot(rt) / cz, s4.SUN_DIR.dot(up) / cz
    th = 12.0 / cam.data.lens
    near = max(abs(sx) / (th * 0.5625), abs(sy) / th) if s4.SUN_DIR.dot(fwd) > 0 else 9.0
    off = math.hypot(sx / (th * 0.5625), sy / th)             # 0 when the sun sits in the frame centre
    fade = max(0.0, min(1.0, 1.6 - near)) * min(1.0, off / 0.35) * (1 - cover) * (1 - push) * (0.6 + 0.4 * glare)
    for o, em, s0, gk in P["ghosts"]:
        o.location = cam.location + (fwd + rt * sx * gk + up * sy * gk).normalized() * 8.0
        em.inputs[1].default_value = s0 * fade
        o.hide_render = fade < 0.02
        face_cam(o)


SUN_HIGH = V((0.25, 0.30, 0.92)).normalized()      # S10 V2-V4: a high noon sun over the plain


def kid_pose(key):
    """Show one of the plain's kid cards (stand, shield, fan, shiver) and its contact shadow; hide the rest."""
    for k, (o, sh) in Pl["kids"].items():
        show((o, sh), k == key)


def plain_day(key):
    """Day setup on the plain (as built): warm sun, sun disc and glow on, no night pieces; one kid card."""
    P = Pl
    kid_pose(key)
    P["sun"].data.color = pc.hexcol("#FFF4E2")[:3]
    show((P["sun_disc"], P["glow"]), True)
    show([g for g, *_ in P["frost"]] + [st for st, _ in P["stars"]], False)


def plain_s10_off():
    P = Pl
    for c, puffs in P["layer"]:
        show(puffs, False)
    for a_in, a_out, *_ in P["bounce"]:
        a_in.hide_render = a_out.hide_render = True
    for a_dn, hit, spot, *_ in P["pour"]:
        a_dn.hide_render = spot.hide_render = True
    for o, *_ in P["shimmer"]:
        o.hide_render = True


def put_arrow(o, tip, d, frac):
    """Place a beam arrow (tip at origin, pointing local +X) at `tip` along `d`, flat side to the camera, length x frac."""
    if frac <= 0.02:
        o.hide_render = True
        return
    o.hide_render = False
    x = d.normalized(); zz = cam.location - tip
    zz = (zz - x * zz.dot(x)).normalized(); y = zz.cross(x)
    o.matrix_world = Matrix(((x.x, y.x, zz.x, tip.x), (x.y, y.y, zz.y, tip.y), (x.z, y.z, zz.z, tip.z), (0, 0, 0, 1))) @ Matrix.Diagonal((frac, 1, 1, 1))


def fly_beam(a_in, a_out, hit, din, dout, f, t0, D, v, L):
    """An arrow travels D along din to `hit` and slides into it; the bounce arrow (if any) slides out along dout.
    Returns how far past the hit the beam has gone (negative before it lands)."""
    s = v * (f - t0)
    q = s - D
    if s <= 0:
        a_in.hide_render = True
    elif s <= D:
        put_arrow(a_in, hit - din * (D - s), din, min(s, L) / L)
    else:
        put_arrow(a_in, hit, din, (L - q) / L)
    if a_out is not None:
        put_arrow(a_out, hit + dout * max(q, 0), dout, min(q, L) / L if q > 0 else 0)
    return q


def reflect(d, n):
    return d - 2 * d.dot(n) * n


def ev_s10(t, f):
    """S10 (v1 clock 1136-1398; 'sunshade' ~1186, 'bouncing sunlight back to space' ~1202-1246, 'before it lands'
    ~1253-1275, 'so with fewer of them' ~1286-1317, 'more sun would pour onto the bare ground' ~1326-1387).
    V1 (space, LS8): slow orbit around Earth; arrows of sunlight hit bright cloud tops and bounce back out; push in.
    V2 (plain, LS8): above the cloud layer, arrows bounce off its tops; push down through it to the shaded land.
    V3 (LS6): the layer thins; arrows pour through the gaps to the ground and warm spots spread; follow them down.
    V4 (LS6): low push across the bare cracked ground, heat shimmer rising, arrows still landing; end on the kid."""
    global F
    F = f
    if f < 1200:
        S = Sp
        k = ease((f - 1136) / 64)
        a = math.radians(lerp(-7.0, 6.0, k))
        base = V((math.sin(a), -math.cos(a), 0.28)).normalized()
        push = ease((f - 1172) / 28)
        cam.location = Eo + base * lerp(185.0, 125.0, push)
        aim.location = Eo.lerp(Eo + (base + V((0, 0, -0.45))).normalized() * s4.EARTH_R, 0.7 * push)
        cam.data.lens = lerp(35.0, 40.0, push)
        for o in (S["sun_disc"], S["sun_glow"], S["halo"]):
            face_cam(o)
        din = -s4.SPACE_BEAM
        for a_in, a_out, hit, n, t0 in S["bounce"]:
            fly_beam(a_in, a_out, hit, din, reflect(din, n), f, t0, 50.0, 2.6, 11.0)
        fwd = (aim.location - cam.location).normalized()
        rt = fwd.cross(V((0, 0, 1))).normalized(); up = rt.cross(fwd)
        for o, off, ph in S["dust"]:
            o.location = cam.location + fwd * off.y + rt * (off.x + 0.012 * (f - 1136)) + up * (off.z + 0.15 * math.sin(f * 0.05 + ph))
        return
    P = Pl
    plain_day("stand")
    show(P["veil"], False)
    for o, *_ in P["ghosts"]:
        o.hide_render = True
    P["sun"].rotation_euler = SUN_HIGH.to_track_quat("Z", "Y").to_euler()
    P["sun"].data.energy = 4.6 if f < 1265 else 5.5
    P["sun_disc"].location, P["glow"].location = Po + SUN_HIGH * 400, Po + SUN_HIGH * 430
    P["glow"].scale = (1.5, 1.5, 1.5)
    if f < 1265:
        k = ease((f - 1200) / 65)
        pos, tgt, lens = (Po + V((8, -38, 78))).lerp(Po + V((1, 6, 15)), k), (Po + V((0, 18, 24))).lerp(Po + V((0, 40, 9)), k), 24.0
    elif f < 1332:
        k = ease((f - 1265) / 67)
        pos, tgt, lens = (Po + V((1, 6, 15))).lerp(Po + V((0.6, -1.5, 1.4)), k), (Po + V((0, 40, 9))).lerp(Po + V((0, 12, 0.9)), k), lerp(24.0, 26.0, k)
    else:
        k = ease((f - 1332) / 66)
        pos, tgt, lens = (Po + V((0.6, -1.5, 1.4))).lerp(Po + V((0.3, 2.6, 0.8)), k), (Po + V((0, 12, 0.9))).lerp(Po + V((0, 6, 0.8)), k), 26.0
    cam.location, aim.location, cam.data.lens = pos, tgt, lens
    face_cam(P["sun_disc"]); face_cam(P["glow"])
    # the cloud layer: whole in V2, thinning from 1268 (a fifth of the puffs stay at 70%, so a few wisps remain)
    allp = [p for c, puffs in P["layer"] for p in puffs]
    n = len(allp)
    puff_pop(allp, lambda k, n: -1000, lambda k, n: 1268 + 50 * ((k * 7) % n) / n, keep=set(range(0, n, 5)))
    din = -SUN_HIGH
    for a_in, a_out, hit, nrm, t0 in P["bounce"]:
        if f < 1265:
            fly_beam(a_in, a_out, hit, din, reflect(din, nrm), f, t0, 35.0, 1.7, 7.0)
        else:
            a_in.hide_render = a_out.hide_render = True
    for a_dn, hit, spot, sz, t0 in P["pour"]:
        if f < 1265:
            a_dn.hide_render = spot.hide_render = True
            continue
        q = fly_beam(a_dn, None, hit, din, None, f, t0, 14.0, 1.0, 3.4)
        r = sz * ease(q / 18.0)
        spot.hide_render = r < 0.03
        spot.scale = (r, r, 1)
    for o, m, base, ph in P["shimmer"]:
        a = max(0.0, min(1.0, (f - 1300) / 15))
        o.hide_render = a < 0.02
        o.location = base + V((0.04 * math.sin(f * 0.3 + ph * 6), 0, 0.05 * math.sin(f * 0.21 + ph * 4)))
        o.scale = (math.sin(f * 0.45 + ph * 6), 1, 1 + 0.12 * math.sin(f * 0.17 + ph * 5))
        next(nd for nd in m.node_tree.nodes if nd.bl_idname == "ShaderNodeMixShader").inputs[0].default_value = \
            0.22 * a * (0.7 + 0.3 * math.sin(f * 0.5 + ph * 9))


def ev_s11(t, f):
    """S11 (v1 clock 1398-1522; 'Hot' ~1401, 'days' ~1420, 'cold' ~1434, 'nights' ~1455, 'desert' ~1494).
    V1 (LS6): harsh glare, push in on the kid shielding the eyes (squint), then fanning (from 'days'); S10's wisps,
    warm spots and heat shimmer carry on. V2 (LS7, after the whip): night; the kid in winter clothes shivers; quick
    pull back. V3 (LS7): slow pull back to a wide of the plain under stars, frost glinting on the cracks."""
    global F
    F = f
    P = Pl
    show(P["veil"], False)
    for o, *_ in P["ghosts"]:
        o.hide_render = True
    for a_in, a_out, *_ in P["bounce"]:
        a_in.hide_render = a_out.hide_render = True
    allp = [p for c, puffs in P["layer"] for p in puffs]
    if f < 1446:
        plain_day("shield" if f < 1419 else "fan")
        P["sun"].rotation_euler = SUN_HIGH.to_track_quat("Z", "Y").to_euler()
        P["sun"].data.energy = 5.5
        P["sun_disc"].location, P["glow"].location = Po + SUN_HIGH * 400, Po + SUN_HIGH * 430
        n = len(allp)      # the layer as S10 left it: a few thin wisps
        puff_pop(allp, lambda k, n: -1000, lambda k, n: 1268 + 50 * ((k * 7) % n) / n, keep=set(range(0, n, 5)))
        for a_dn, hit, spot, sz, t0 in P["pour"]:
            a_dn.hide_render = True
            spot.hide_render = False; spot.scale = (sz, sz, 1)
        for o, m, base, ph in P["shimmer"]:
            o.hide_render = False
            o.location = base + V((0.04 * math.sin(f * 0.3 + ph * 6), 0, 0.05 * math.sin(f * 0.21 + ph * 4)))
            o.scale = (math.sin(f * 0.45 + ph * 6), 1, 1 + 0.12 * math.sin(f * 0.17 + ph * 5))
            next(nd for nd in m.node_tree.nodes if nd.bl_idname == "ShaderNodeMixShader").inputs[0].default_value = \
                0.22 * (0.7 + 0.3 * math.sin(f * 0.5 + ph * 9))
        k = ease((f - 1398) / 48)
        pos, tgt, lens = (Po + V((0.3, 2.6, 0.8))).lerp(Po + V((0.15, 4.0, 0.95)), k), (Po + V((0, 6, 0.8))).lerp(Po + V((0, 6, 0.95)), k), lerp(26.0, 28.0, k)
        face_cam(P["sun_disc"]); face_cam(P["glow"])
    else:
        kid_pose("shiver")
        show(allp, False)
        show((P["sun_disc"], P["glow"]), False)
        for a_dn, hit, spot, *_ in P["pour"]:
            a_dn.hide_render = spot.hide_render = True
        for o, *_ in P["shimmer"]:
            o.hide_render = True
        moon = V((-0.3, 0.45, 0.84)).normalized()      # cool moonlight from above, a little behind the plain
        P["sun"].rotation_euler = moon.to_track_quat("Z", "Y").to_euler()
        P["sun"].data.energy = 1.8
        P["sun"].data.color = pc.hexcol("#B8C6FF")[:3]
        for g, sc0, ph in P["frost"]:
            tw = 0.35 + 0.9 * max(0.0, math.sin(f * 0.55 + ph * 40)) ** 4
            g.hide_render = False; g.scale = (sc0[0] * tw, sc0[1] * tw, sc0[2] * tw)
        for st, ph in P["stars"]:
            tw = 0.5 + 0.6 * max(0.0, math.sin(f * 0.4 + ph * 30)) ** 3
            st.hide_render = False; st.scale = (tw, tw, tw)
        kid = Pl["kids"]["shiver"][0]      # the shiver: a small side-to-side shake, held 2 frames each
        kid.location = Po + V((s4.KID_PLAIN[0] + (0.012 if (int(f) // 2) % 2 else -0.012), s4.KID_PLAIN[1], s4.plain_height(*s4.KID_PLAIN)))
        if f < 1484:
            u = max(0.0, min(1.0, (f - 1446) / 38)); k = 1 - (1 - u) ** 2
            pos, tgt, lens = (Po + V((0.15, 4.0, 0.95))).lerp(Po + V((0.4, 1.6, 1.0)), k), (Po + V((0, 6, 0.95))).lerp(Po + V((0, 6, 0.9)), k), lerp(28.0, 26.0, k)
        else:
            k = ease((f - 1484) / 38)
            pos, tgt, lens = (Po + V((0.4, 1.6, 1.0))).lerp(Po + V((1.4, -7.0, 2.8)), k), (Po + V((0, 6, 0.9))).lerp(Po + V((0, 10, 0.6)), k), lerp(26.0, 24.0, k)
    cam.location, aim.location, cam.data.lens = pos, tgt, lens


def ev_s12(t, f):
    """S12 (v1 clock 1522-1607; 'The sky was running on the ocean all along.' ~1525-1590). The kid's window again, now
    dry, under LS5's thin bright sky. V1: slow push-in on the kid (wistful) behind the dry pane. V2: pull back from the
    window to the house front under the bright sky, through the fade-out (added by finish_ep004.py)."""
    show(Wn["rain"], False)
    for o, base in Wn["streaks"]:
        o.hide_render = True
    show(Wn["kid_curious"], False); show(Wn["kid_wistful"], True)
    Wn["lamp"].data.energy = 40                       # daytime: the lamp barely adds anything
    Wn["sun"].data.energy, Wn["sun"].data.color = 4.8, pc.hexcol("#FFF4E2")[:3]
    face = Wo + V((0.36, 0.72, 1.08))
    if f < 1566:
        k = ease((f - 1522) / 44)
        pos, tgt, lens = (Wo + V((0.25, -1.7, 1.25))).lerp(Wo + V((0.3, -1.15, 1.18)), k), face, lerp(38.0, 44.0, k)
    else:
        k = ease((f - 1566) / 41)
        pos = (Wo + V((0.3, -1.15, 1.18))).lerp(Wo + V((0.8, -9.5, 2.4)), k)
        tgt, lens = face.lerp(Wo + V((0.1, 0.0, 1.9)), k), lerp(44.0, 28.0, k)
    cam.location, aim.location, cam.data.lens = pos, tgt, lens


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
    # S08 V1: the thinned cloud drops only a sparse sprinkle; follow a few drops down to the ground
    (855, 912, "inland", "LS5i", (Io + V((5.5, 15.5, 3.5)), Io + V((7.0, 31.0, 12.5)), 24), (Io + V((6.0, 17.0, 3.0)), Io + V((7.5, 27.5, 0.3)), 26), ev_s08, 11.0),
    # S08 V2: the ground dries; cracks spread across the field; plants droop; low push across the field
    (912, 968, "inland", "LS5i", (Io + V((8.0, 2.5, 2.1)), Io + V((9.5, 14.0, 0.0)), 24), (Io + V((9.0, 9.0, 1.6)), Io + V((10.5, 20.0, 0.1)), 24), ev_s08, 11.0),
    # S08 V3: one faint curl tries to rise from the cracked ground and fizzles; crane up past it to a nearly clear sky
    (968, 1022, "inland", "LS5i", (Io + V((9.0, 9.0, 1.6)), Io + V((10.5, 20.0, 0.1)), 24), (Io + V((9.6, 12.0, 3.8)), Io + V((11.0, 30.0, 15.0)), 24), ev_s08, 11.0),
    # S09 V1: a calm clear sky over a baked, cracked plain; the kid stands deadpan in sun clothes; slow push-in,
    # a thin cloud slides over the sun and the ground dims; the camera starts tilting up to the sun
    (1022, 1086, "plain", "LS5d", None, None, ev_s09, 11.0),
    # S09 V2: on 'But' the cloud slides off and the glare snaps back; tilt onto the sun, flare across the lens,
    # push into the glare
    (1086, 1136, "plain", "LS6", None, None, ev_s09, 11.0),
    # S10 V1: Earth from space; arrows of sunlight hit bright cloud tops and bounce back out; slow orbit, push toward the clouds
    (1136, 1200, "space", "LS8", None, None, ev_s10, 11.0),
    # S10 V2: closer, the cloud layer as a parasol over the land; arrows bounce off its tops; push down through it
    (1200, 1265, "plain", "LS8", None, None, ev_s10, 11.0),
    # S10 V3: the clouds thin; arrows pour through the gaps and warm the ground; follow them down
    (1265, 1332, "plain", "LS6", None, None, ev_s10, 11.0),
    # S10 V4: bare cracked ground under a blazing sky, heat shimmer rising; low push across the ground to the kid
    (1332, 1398, "plain", "LS6", None, None, ev_s10, 11.0),
    # S11 V1: harsh glare; push in on the kid shielding the eyes (squinting), then fanning; whip the sun down
    (1398, 1446, "plain", "LS6", None, None, ev_s11, 11.0),
    # S11 V2: the sky snaps to a starry night; the kid in winter clothes shivers; quick pull back as the light flips
    (1446, 1484, "plain", "LS7", None, None, ev_s11, 11.0),
    # S11 V3: wide: the desert-like plain under stars, frost glinting on the cracks, the kid small; dissolve to the window
    (1484, 1522, "plain", "LS7", None, None, ev_s11, 11.0),
    # S12 V1: the kid's window again, dry, a thin bright sky outside; slow push-in on the kid (wistful)
    (1522, 1566, "window", "LS5", None, None, ev_s12, 2.8),
    # S12 V2: pull back from the window to the house front under the bright sky, through the fade-out
    (1566, 1607, "window", "LS5", None, None, ev_s12, 8.0),
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
print("RANGE", f"frames {list(frames)}" if ONLY else f"{START}-{min(END, LAST2) - 1}", flush=True)
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
