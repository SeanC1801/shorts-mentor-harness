"""EP003 props and effects (set-specs v1): globes, pins, asteroid, ring forming and fading, falling debris,
crater dots and counter, ghost ring, ice-and-sun insert, and the printed cutouts (stamp, timeline card, age tags).
Builders are reusable by the episode render; this script renders one review still per prop.

usage: blender -b -P renderer-blender/ep003_props.py -- OUT_DIR [scale%] [still,still,...]
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector, Euler
import papercraft as pc
from papercraft import painted, flatcard, emit, box, cyl, blob, sphere, strip, card, light

random.seed(21)


def deg(*a): return tuple(math.radians(x) for x in a)


def globe(name, c, r, tex="earth_map.png", tilt=23.4, spin=0.0):
    g = sphere(name, c, r, painted(tex, 1.0, "UV", lift=1.1))
    g.rotation_euler = (math.radians(tilt), 0, math.radians(spin))
    return g


def surface_point(g, r, lat, lon):
    """World point on a globe's surface (UV sphere: lat about its local z, lon around it)."""
    la, lo = math.radians(lat), math.radians(lon)
    local = Vector((math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))) * r
    return g.matrix_world @ (local / max(g.scale))


def pins(g, r, lats, lon=None, colors=("#F28C28", "#F2B84B", "#7FD6D0"), face=(0.25, -1.0)):
    """Pins at the given latitudes on the meridian facing direction `face` (x, y)."""
    out = []
    for lat, col in zip(lats, colors):
        la = math.radians(lat)
        up = Vector((face[0] * math.cos(la), face[1] * math.cos(la), math.sin(la))).normalized()
        base = g.location + up * r
        st = cyl("pin_stem", base + up * r * 0.08, r * 0.012, r * 0.16, painted("metal.png", 4.0), verts=12)
        st.rotation_mode = "QUATERNION"; st.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(up)
        out.append(sphere("pin_head", base + up * r * 0.18, r * 0.045, emit(col, 2.2)))
    return out


def asteroid(c, r, stretch=1.0):
    a = blob("asteroid", c, r, painted("asteroid.png", 1.5), scale=(1.35 * stretch, 1.0, 0.85), sub=3)
    tex = bpy.data.textures.new("lumps", "CLOUDS"); tex.noise_scale = 0.6
    d = a.modifiers.new("lumps", "DISPLACE"); d.texture, d.strength = tex, r * 0.35
    return a


def crater_dots(g, r, n=21, max_lat=30, seed=3, size=0.05, max_lon=80):
    rr = random.Random(seed)
    bpy.context.view_layer.update()
    dots = []
    for k in range(n):
        p = surface_point(g, r * 1.004, rr.uniform(-max_lat, max_lat), rr.uniform(-max_lon, max_lon))
        dots.append(blob("crater_dot", p, r * size, emit("#FF9B4A", 2.5), scale=(1, 1, 1), sub=2))
    return dots


def chunks_arc(center, Rg, r_mid, spread, a0, a1, n, tilt=0.0, size=0.03, z_jit=0.02):
    """Rock pieces along an arc around a globe (ring forming or thinning)."""
    rot = Euler((math.radians(tilt), 0, 0)).to_matrix()
    out = []
    for k in range(n):
        a = math.radians(random.uniform(a0, a1))
        rad = Rg * (r_mid + random.uniform(-spread, spread))
        p = rot @ Vector((rad * math.cos(a), rad * math.sin(a), random.uniform(-z_jit, z_jit) * Rg))
        o = blob("chunk", Vector(center) + p, Rg * size * random.uniform(0.5, 1.4), painted("rock.png", 6.0), scale=(1.3, 1, 0.8), sub=1, smooth=False)
        o.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3))
        out.append((o, a))
    return out


def glow_card(name, c, size, strength=1.6):
    o, _ = card(name, "glow.png", size, (c[0], c[1], c[2] - size / 2), shadow=False)
    o.data.materials[0] = flatcard("glow.png", strength)
    return o


# ---------------- review stills ----------------
if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep003_props"]
    OUT, SCALE = argv[0], int(argv[1]) if len(argv) > 1 else 100
    ONLY = argv[2].split(",") if len(argv) > 2 else None
    sc = pc.setup(SCALE)
    cam, aim = pc.camera()
    RING = pc.ring_mat(haze="#AFC2E6", haze_amt=0.15)
    RIM = pc.ring_mat(haze="#FFF4E0", haze_amt=0.3, strength=1.4, opaque=True)
    STILLS = {}

    def stage(name, i):
        col = pc.collection("P-" + name)
        O = Vector((i * 60.0, 0, 0))
        return col, O

    def key_light(O, energy=4.0, rot=(20, -60, 0), color="#FFF4E2"):
        light("sun", "SUN", O + Vector((0, 0, 10)), energy, color, rot=deg(*rot), angle=8)

    def S_globe_pins(O):
        g = globe("globe_pins", O + Vector((0, 9, 0)), 2.6, "earth_map.png", tilt=0, spin=-100)
        g.rotation_euler = deg(-15, 0, -100)
        pins(g, 2.6, (0, 40, 70))
        key_light(O)
        return "LS2", (O + Vector((0.3, 0, 0.8)), O + Vector((0, 9, 0.6)), 20, 11)

    def S_paper(O):
        globe("globe", O + Vector((1.2, 10, 0.4)), 2.6, "earth_map.png", spin=120)
        card("paper", "PROP-PAPER-STAMP.png", 2.6, O + Vector((-0.2, 4.5, -1.3)), shadow=False)
        key_light(O)
        return "LS2", (O + Vector((0, 0, 0)), O + Vector((0, 6, 0)), 32, 11)

    def S_timeline(O):
        globe("globe_ancient", O + Vector((0, 11, -0.6)), 3.0, "ancient_map.png", tilt=-25, spin=-90)
        card("timeline", "PROP-TIMELINE-CARD.png", 1.15, O + Vector((0, 4.5, 0.4)), shadow=False)
        key_light(O)
        return "LS2", (O + Vector((0, 0, 0.4)), O + Vector((0, 6, 0.4)), 30, 11)

    def S_asteroid(O):
        globe("globe_ancient", O + Vector((2.5, 16, -1.5)), 4.0, "ancient_map.png", tilt=-25, spin=-90)
        asteroid(O + Vector((-0.6, 6, 0.6)), 0.8)
        chunks_arc(O + Vector((-0.6, 3, 0.6)), 1.0, 2.0, 1.2, 0, 360, 10, size=0.04)
        key_light(O, rot=(10, -70, 0))
        return "LS2", (O + Vector((0.2, 0, 0.2)), O + Vector((0, 8, 0.4)), 28, 11)

    def S_ring_form(O):
        C = O + Vector((0, 12, 0))
        globe("globe_ancient", C, 2.5, "ancient_map.png", tilt=-25, spin=-90)
        a = asteroid(C + Vector((-3.6, -1.0, 0.9)), 0.55, stretch=1.9)
        a.rotation_euler = deg(0, 0, -25)
        chunks_arc(C, 2.5, 1.95, 0.14, 120, 340, 320, tilt=12, size=0.05)
        glow_card("break_glow", C + Vector((-3.4, -1.3, 0.9)), 2.6, 1.8)
        light("break", "POINT", C + Vector((-3.6, -1.6, 1.0)), 400, "#FFB066")
        key_light(O, energy=3.5, color="#FFE2C0")
        return "LS6", (O + Vector((-0.8, -2, 2.4)), C + Vector((-1.2, 0, 0)), 20, 11)

    def S_craters(O):
        C = O + Vector((0, 9, 0))
        g = globe("globe_ancient", C, 2.6, "ancient_map.png", tilt=0, spin=0)
        g.rotation_euler = deg(-12, 0, -90)
        crater_dots(g, 2.6, size=0.03)
        cyl("equator_line", C, 2.62, 0.02, emit("#FFF1D6", 1.5, alpha=0.6), rot=deg(-12, 0, 0), verts=96)
        card("counter", "PROP-COUNTER-21.png", 0.55, O + Vector((0.45, 5, 1.25)), shadow=False)
        key_light(O)
        return "LS2", (O + Vector((0, 0, 0.6)), C + Vector((0, 0, 0.2)), 30, 11)

    def S_fade(O):
        C = O + Vector((0, 12, 0))
        g = globe("globe_ancient", C, 2.5, "ancient_map.png", tilt=0, spin=0)
        g.rotation_euler = deg(-25, 0, -90)
        pc.ring_around("ring_fading", C, 2.5, 1.7, 2.3, pc.ring_mat(haze="#AFC2E6", haze_amt=0.25, alpha_mul=0.45), tilt_deg=-10)
        for k in range(14):
            a = math.radians(random.uniform(-150, -30))
            start = C + Vector((2.5 * 1.75 * math.cos(a), 2.5 * 1.75 * math.sin(a) * 0.98, 0))
            end = C + Vector((2.5 * 1.02 * math.cos(a), 2.5 * 1.02 * math.sin(a), random.uniform(-0.3, 0.3)))
            pts = [start.lerp(end, t) for t in (0, 0.33, 0.66, 1)]
            strip("streak", pts, [0.0, 0.04, 0.07, 0.02], emit("#FFD9A0", 1.6, alpha=0.75), up=(0, 0, 1))
            blob("chunk", start.lerp(end, 0.4), 0.06, painted("rock.png", 6.0), sub=1, smooth=False)
        crater_dots(g, 2.5, n=10, max_lat=12, seed=9, size=0.035)
        key_light(O)
        return "LS2", (O + Vector((0, 0, 1.6)), C + Vector((0, 0, -0.2)), 28, 11)

    def S_age_tags(O):
        pc.plane("ground", O + Vector((0, 6, -0.2)), (40, 40), (0, 0, 0), painted("rock.png", 0.4))
        for k, (x, y) in enumerate(((-1.1, 5.0), (0.3, 6.0), (1.3, 4.6))):
            p = O + Vector((x, y, -0.2))
            cyl("crater_rim", p, 0.7, 0.32, painted("asteroid.png", 2.0, lift=1.1), verts=40, r2=0.55, bevel=0.08)
            cyl("crater_floor", p + Vector((0, 0, 0.12)), 0.5, 0.1, painted("asteroid.png", 3.0, lift=0.6), verts=40)
            card(f"tag{k}", "PROP-AGE-TAG.png", 0.42, p + Vector((0.35, -0.6, 0.1)), shadow=False)
        key_light(O, rot=(40, -40, 0))
        return "LS2", (O + Vector((0, 2.2, 1.5)), O + Vector((0.1, 5.4, -0.2)), 22, 8)

    def S_ghost(O):
        C = O + Vector((0, 10, 0))
        globe("globe", C, 2.6, "earth_map.png", spin=150)
        pc.ring_around("ghost_ring", C, 2.6, 1.7, 2.4, pc.ring_mat(haze="#DDE8FF", haze_amt=0.55, strength=1.2, alpha_mul=0.28), tilt_deg=-14)
        key_light(O)
        return "LS2", (O + Vector((0, 0, 1.2)), C, 26, 11)

    def S_ice_sun(O):
        C = O + Vector((0, 9, 0.5))
        sun = card("sun_disc", "sun_disc.png", 4.0, C + Vector((2.2, 4, -1.5)), shadow=False)[0]
        sun.data.materials[0] = flatcard("sun_disc.png", 2.2)
        glow_card("sun_glow", C + Vector((2.2, 3.9, 0.5)), 9.0, 1.4)
        ice = blob("ice_chunk", C + Vector((-0.6, -1.5, 0.2)), 0.55, painted("ice.png", 2.0, lift=1.15), scale=(1.1, 1, 0.9), sub=1, smooth=False)
        rock = blob("rock_chunk", C + Vector((-1.0, -2.6, -0.7)), 0.4, painted("rock.png", 2.0), scale=(1.2, 1, 0.85), sub=1, smooth=False)
        for k in range(10):
            a = random.uniform(-0.6, 0.6)
            pts = [C + Vector((-0.6 + 0.3 * t * math.sin(a * 3), -1.5 - 0.1 * t, 0.7 + 1.4 * t)) for t in (0, 0.33, 0.66, 1)]
            strip("vapor", pts, [0.25, 0.3, 0.22, 0.05], emit("#F4FBFF", 1.2, alpha=0.35))
        for k in range(14):
            blob("sparkle", C + Vector((-0.6 + random.uniform(-0.8, 0.8), -1.6 + random.uniform(-0.3, 0.3), 0.2 + random.uniform(-0.4, 1.4))), 0.03, emit("#FFFFFF", 3.0), sub=1)
        key_light(O, energy=4.5, rot=(10, 60, 0), color="#FFF2D6")
        return "LS3", (O + Vector((-0.4, 0, 0.6)), C + Vector((-0.1, 0, 0.4)), 30, 11)

    BUILD = [("globe_pins", S_globe_pins), ("paper_stamp", S_paper), ("timeline_card", S_timeline), ("asteroid", S_asteroid),
             ("ring_form", S_ring_form), ("crater_dots", S_craters), ("ring_fade_debris", S_fade), ("age_tags", S_age_tags),
             ("ghost_ring", S_ghost), ("ice_sun", S_ice_sun)]
    for i, (name, fn) in enumerate(BUILD):
        if ONLY and name not in ONLY:
            continue
        col, O = stage(name, i)
        STILLS[name] = (col, *fn(O))
    GRADES = {"LS2": ("space_eq.png", 0.3, "#E6E8FF", 1.15), "LS6": ("space_eq.png", 0.3, "#FFE6CC", 1.2), "LS3": ("space_eq.png", 0.35, "#FFF2E0", 1.15)}
    os.makedirs(OUT, exist_ok=True)
    for name, (col, state, shot) in STILLS.items():
        for other, (c2, *_r) in STILLS.items():
            c2.hide_render = other != name
        pc.set_world(*GRADES[state])
        pos, tgt, lens, fstop = shot
        cam.location, aim.location = pos, tgt
        cam.data.lens, cam.data.dof.aperture_fstop = lens, fstop
        pc.face_cards(pos)
        sc.render.filepath = os.path.join(OUT, f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print("WROTE", sc.render.filepath)
