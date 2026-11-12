"""EP003 sets (set-specs v1, look approved on the bedroom test): rooftops, beach, city rooftop,
north town, space, seafloor, dawn plain. Each set is its own collection far from the others.
The rock ring is real geometry in Earth's equatorial plane, so its look changes with latitude.

usage: blender -b -P renderer-blender/ep003_sets.py -- OUT_DIR [scale%] [set,set,...]
"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import papercraft as pc
from papercraft import painted, flatcard, box, plane, cyl, blob, sphere, wedge, strip, ring, card, light

R, RIN, ROUT = 3000.0, 1.8, 2.4          # Earth radius (scene units) and ring radii in Earth radii
cam = RING = RING_RIM = None


def init(camera_obj):
    """Call after papercraft.setup(): shared camera and ring materials for the builders."""
    global cam, RING, RING_RIM
    cam = camera_obj
    RING, RING_RIM = pc.ring_mat(), pc.ring_mat(haze="#FFF4E0", haze_amt=0.35, strength=1.5, opaque=True)
STATES = {"LS1": ("sky_day_eq.png", 0.9, "#E2D5C1", 1.35), "LS5": ("sky_cool_eq.png", 0.7, "#B4BED6", 1.45),
          "LS2": ("space_eq.png", 0.3, "#E6E8FF", 1.1), "LS7": ("water_eq.png", 0.85, "#A3CDC9", 1.25), "LS8": ("sky_dawn_eq.png", 0.7, "#C9B9DA", 1.4)}
SETS = {}


def deg(*a): return tuple(math.radians(x) for x in a)


def add_ring(O, lat):
    o = ring("ring", O, lat, R, RIN, ROUT, RING, thick=0.02, rim_mat=RING_RIM)
    o.visible_shadow = False
    return o


def house(O, c, w, d, h, wall, roof, roof_h=1.6, chimney=True, door="trim.png"):
    p = Vector(O) + Vector(c)
    box("walls", p + Vector((0, 0, h / 2)), (w, d, h), painted(wall, 0.5), 0.05)
    wedge("roof", p + Vector((0, 0, h)), d + 0.5, roof_h, w + 0.5, painted(roof, 0.6))
    front = p.y + d / 2
    for k in range(int(w // 1.6)):
        x = p.x - w / 2 + 0.9 + k * 1.6
        if abs(x - p.x) < 0.5 and door:
            box("door", (x, front + 0.03, 0.9), (0.8, 0.08, 1.8), painted(door, 1.5), 0.03)
            continue
        box("win_frame", (x, front + 0.03, h * 0.6), (0.85, 0.08, 0.95), painted("trim.png", 1.5), 0.03)
        box("win_glass", (x, front + 0.06, h * 0.6), (0.62, 0.06, 0.72), painted("glass.png", 2.0))
    if chimney:
        box("chimney", p + Vector((w * 0.25, 0, h + roof_h * 0.7)), (0.5, 0.5, 1.4), painted("brick.png", 1.2), 0.03)


def palm(O, base, height, lean, fronds=8, s=1.0):
    p0 = Vector(O) + Vector(base)
    pts = [p0 + Vector((lean[0] * t * t, lean[1] * t * t, height * t)) for t in (i / 8 for i in range(9))]
    for a, b in zip(pts, pts[1:]):
        d = b - a
        o = cyl("trunk", (a + b) / 2, 0.16 * s, d.length * 1.08, painted("bark.png", 2.0), r2=0.13 * s)
        o.rotation_mode = "QUATERNION"; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    top = pts[-1]
    for k in range(fronds):
        a = k / fronds * 2 * math.pi + random.uniform(-0.2, 0.2)
        L = random.uniform(2.2, 2.9) * s
        fp = [top + Vector((math.cos(a) * L * t, math.sin(a) * L * t, 0.6 * s * t - 1.6 * s * t * t)) for t in (i / 10 for i in range(11))]
        strip("frond", fp, [0.06 + 0.55 * s * math.sin(math.pi * t) ** 0.6 for t in (i / 10 for i in range(11))], painted("palm_leaf.png", 1.0, "UV"))
    for k in range(3):
        blob("coconut", top + Vector((0.18 * math.cos(k * 2.1), 0.18 * math.sin(k * 2.1), -0.15)), 0.13 * s, painted("bark.png", 3.0))


def pine(O, base, h, snow=True):
    p = Vector(O) + Vector(base)
    cyl("pine_trunk", p + Vector((0, 0, 0.4)), 0.12, 0.8, painted("bark.png", 2.0))
    for k, (r, z) in enumerate(((1.1, 0.9), (0.85, 1.6), (0.6, 2.25))):
        cyl("pine", p + Vector((0, 0, z * h / 3 + 0.5)), r * h / 3, h / 3 * 0.9, painted("pine.png", 1.5), r2=0.05, verts=24, bevel=0.03)
        if snow:
            cyl("pine_snow", p + Vector((0, 0, z * h / 3 + 0.5 + h / 3 * 0.18)), r * h / 3 * 0.62, h / 3 * 0.5, painted("snow.png", 2.0), r2=0.04, verts=24, bevel=0.03)


def fence(O, x0, x1, y, h=1.0):
    n = int((x1 - x0) / 0.9)
    for k in range(n + 1):
        box("post", Vector(O) + Vector((x0 + k * 0.9, y, h / 2)), (0.1, 0.1, h), painted("trim.png", 2.0), 0.02)
    for z in (0.35, 0.75):
        box("rail", Vector(O) + Vector(((x0 + x1) / 2, y, z * h)), (x1 - x0, 0.07, 0.09), painted("trim.png", 2.0), 0.015)


# ---------------- sets ----------------
def set_rooftops(O):
    plane("ground", O, (200, 200), (0, 0, 0), painted("concrete.png", 0.3))
    for i, (x, w) in enumerate(((-9, 4.2), (-4.5, 3.8), (-0.5, 3.6), (3.6, 4.0), (8, 4.4))):
        house(O, (x, -12, 0), w, 5, random.uniform(4.5, 6.5), random.choice(["plaster_cream.png", "plaster_blue.png", "plaster_pink.png", "plaster_green.png"]),
              random.choice(["roof_red.png", "roof_blue.png"]))
    for i, x in enumerate((-12, -6, 0, 6, 12)):
        house(O, (x + 2, -22, 0), 5, 5, random.uniform(7, 10), random.choice(["plaster_cream.png", "plaster_pink.png", "plaster_blue.png"]), "roof_red.png", door=None)
    # foreground: our own roof edge and a chunky chimney
    wedge("near_roof", Vector(O) + Vector((0, -0.5, 2.0)), 3.0, 1.2, 8, painted("roof_red.png", 0.6))
    box("near_chimney", Vector(O) + Vector((-1.7, -1.1, 3.4)), (0.8, 0.8, 2.2), painted("brick.png", 1.2), 0.04)
    add_ring(O, 40)
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 3.4, "#FFE7C2", rot=deg(50, 0, 30), angle=18)
    light("fill", "AREA", Vector(O) + Vector((0, 4, 5)), 600, "#FFF6EA", rot=deg(-60, 0, 0), size=8)
    return "LS1", (Vector(O) + Vector((0.6, 1.2, 3.6)), Vector(O) + Vector((-0.5, -30, 13)), 18, 8.0)


def set_beach(O):
    plane("sand", Vector(O) + Vector((-20, 0, 0)), (60, 80), (0, 0, 0), painted("sand.png", 0.35))
    plane("sea", Vector(O) + Vector((1510, 0, -0.02)), (3000, 4000), (0, 0, 0), painted("sea.png", 0.06, lift=1.05))
    for k in range(10):
        blob("shell", Vector(O) + Vector((random.uniform(1, 9), random.uniform(-6, 6), 0.03)), random.uniform(0.06, 0.12), painted("plaster_pink.png", 4.0), scale=(1, 0.8, 0.4))
    for k in range(4):
        blob("rock", Vector(O) + Vector((random.uniform(4, 9), random.uniform(-7, 7), 0.1)), random.uniform(0.3, 0.6), painted("rock.png", 1.5), scale=(1.3, 1, 0.6), sub=1)
    palm(O, (2.0, 3.4, 0), 5.5, (0.6, 0.4), s=1.1)
    palm(O, (9.0, -5.0, 0), 6.5, (0.4, -0.6), s=1.2)
    palm(O, (1.2, -2.6, 0), 3.2, (0.2, -0.2), s=0.9)
    card("kid", "KID-BEACH-LOOKUP.png", 1.18, Vector(O) + Vector((5.2, 0.4, 0)), cam)
    add_ring(O, 0)
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 3.4, "#FFE9C7", rot=deg(25, 50, 0), angle=18)
    light("fill", "AREA", Vector(O) + Vector((-3, 0, 4)), 500, "#FFF6EA", rot=deg(0, -70, 0), size=8)
    for k in range(7):   # dune grass clumps: thin painted blades
        x, y = random.uniform(1.0, 3.0), random.uniform(-2.5, 2.5)
        for j in range(9):
            a = random.uniform(0, 2 * math.pi); h = random.uniform(0.35, 0.7)
            fp = [Vector(O) + Vector((x + math.cos(a) * 0.25 * t * t, y + math.sin(a) * 0.25 * t * t, h * t)) for t in (i / 5 for i in range(6))]
            strip("dune_grass", fp, [0.05 * (1 - t) + 0.01 for t in (i / 5 for i in range(6))], painted("palm_leaf.png", 1.0, "UV"), up=(math.cos(a), math.sin(a), 0))
    return "LS1", (Vector(O) + Vector((0, -0.4, 1.3)), Vector(O) + Vector((30, 0.5, 6)), 16, 8.0)


def set_city(O):
    box("roof_floor", Vector(O) + Vector((0, -2, -0.2)), (16, 12, 0.4), painted("concrete.png", 0.4))
    box("parapet", Vector(O) + Vector((0, -7.8, 0.25)), (16, 0.4, 0.5), painted("brick.png", 1.0), 0.03)
    for k in range(17):
        cyl("rail_post", Vector(O) + Vector((-8 + k, -7.8, 0.95)), 0.04, 0.9, painted("metal.png", 2.0), verts=12)
    for z in (1.0, 1.38):
        cyl("rail", Vector(O) + Vector((0, -7.8, z)), 0.035, 16, painted("metal.png", 2.0), rot=deg(0, 90, 0), verts=12)
    for x in (-3.2, 2.6, 5.4):
        cyl("pot", Vector(O) + Vector((x, -6.8, 0.3)), 0.3, 0.6, painted("pot.png", 2.0), verts=24, bevel=0.03)
        for k in range(7):
            blob("plant", Vector(O) + Vector((x + random.uniform(-0.25, 0.25), -6.8 + random.uniform(-0.25, 0.25), 0.75 + random.uniform(0, 0.4))), 0.25, painted("leaf.png", 3.0), scale=(1, 1, 1.2))
    T = Vector(O) + Vector((-5.2, -3.5, 0))
    for dx, dy in ((-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
        box("tank_leg", T + Vector((dx, dy, 0.9)), (0.12, 0.12, 1.8), painted("trim.png", 2.0))
    cyl("tank", T + Vector((0, 0, 2.8)), 1.1, 2.0, painted("trim.png", 0.8), verts=32, bevel=0.04)
    cyl("tank_roof", T + Vector((0, 0, 4.15)), 1.2, 0.7, painted("roof_blue.png", 0.8), r2=0.1, verts=32)
    box("vent", Vector(O) + Vector((3.5, -2.5, 0.5)), (1.0, 1.0, 1.0), painted("metal.png", 1.5), 0.05)
    for k in range(26):
        x = -120 + k * 9.5 + random.uniform(-2, 2)
        y = -30 - random.uniform(0, 90)
        h = random.uniform(10, 40)
        box("bldg", Vector(O) + Vector((x, y, h / 2 - 12)), (random.uniform(6, 9), 8, h), painted(random.choice(["bldg_a.png", "bldg_b.png", "bldg_c.png"]), 0.08))
    card("kid", "KID-ARM-SWEEP.png", 1.18, Vector(O) + Vector((1.2, -4.6, 0)), cam)
    add_ring(O, 40)
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 3.4, "#FFE7C2", rot=deg(50, 0, 30), angle=18)
    light("fill", "AREA", Vector(O) + Vector((0, 4, 5)), 600, "#FFF6EA", rot=deg(-60, 0, 0), size=8)
    return "LS1", (Vector(O) + Vector((0.4, 2.0, 1.7)), Vector(O) + Vector((-1, -30, 12)), 18, 8.0)


def set_north(O):
    plane("snow_ground", O, (200, 200), (0, 0, 0), painted("snow.png", 0.3))
    house(O, (-5, -11, 0), 4.5, 4, 3.4, "siding_red.png", "roof_snow.png", roof_h=2.0)
    house(O, (1.5, -14, 0), 4.0, 4, 3.0, "siding_yellow.png", "roof_snow.png", roof_h=1.8)
    house(O, (7, -10, 0), 3.6, 4, 3.2, "siding_red.png", "roof_snow.png", roof_h=1.8)
    for x, y, h in ((-9, -16, 6), (-2, -20, 7), (4, -22, 6.5), (11, -17, 7), (-12, -9, 5)):
        pine(O, (x, y, 0), h)
    for k in range(7):
        blob("snowbank", Vector(O) + Vector((random.uniform(-4, 4), random.uniform(-3.5, -2.0), 0)), random.uniform(0.6, 1.0), painted("snow.png", 1.0), scale=(1.6, 1, 0.55))
    fence(O, -4.5, 4.5, -1.6)
    for k in range(8):
        blob("hill", Vector(O) + Vector((-120 + k * 35, -160 - random.uniform(0, 40), -8)), random.uniform(25, 40), painted("snow.png", 0.2), scale=(1.6, 1, 0.5))
    card("kid", "KID-NORTH-SHRUG.png", 1.18, Vector(O) + Vector((0.6, -5.5, 0)), cam)
    add_ring(O, 70)   # should stay below the horizon at this latitude
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 2.6, "#FFD9B8", rot=deg(78, 0, 0), angle=12)
    light("fill", "AREA", Vector(O) + Vector((0, 6, 5)), 600, "#E6EEFF", rot=deg(-60, 0, 0), size=8)
    return "LS5", (Vector(O) + Vector((0.3, 3.0, 1.6)), Vector(O) + Vector((0, -30, 6)), 18, 8.0)


def set_space(O):
    g = sphere("globe", Vector(O) + Vector((0, 10, 0)), 3.0, painted("globe.png", 1.0, "UV", lift=1.1))
    g.rotation_euler = deg(23, 0, 40)
    for k in range(14):
        a = random.uniform(0, 2 * math.pi)
        blob("fragment", Vector(O) + Vector((random.uniform(-3.5, 3.5), random.uniform(0.5, 4), random.uniform(-4, 4))), random.uniform(0.08, 0.3), painted("rock.png", 2.0), scale=(1.3, 1, 0.8), sub=1, smooth=False)
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 4.0, "#FFF4E2", rot=deg(20, -60, 0), angle=8)
    return "LS2", (Vector(O) + Vector((0.5, -2, 0.6)), Vector(O) + Vector((0, 10, 0)), 30, 11.0)


def set_seafloor(O):
    plane("seabed", O, (200, 200), (0, 0, 0), painted("seabed.png", 0.3))
    for k in range(12):
        blob("rock", Vector(O) + Vector((random.uniform(-7, 7), random.uniform(-14, -2), 0.1)), random.uniform(0.3, 0.9), painted("rock.png", 1.2), scale=(1.4, 1.1, 0.6), sub=1)
    for k in range(9):
        x, y = random.uniform(-6, 6), random.uniform(-12, -2)
        cyl("sponge", Vector(O) + Vector((x, y, 0.5)), random.uniform(0.15, 0.3), random.uniform(0.8, 1.6), painted(random.choice(["sponge_orange.png", "sponge_purple.png"]), 2.0), r2=0.32, verts=18, bevel=0.03)
    for k in range(14):
        x, y = random.uniform(-6, 6), random.uniform(-10, -1)
        a = random.uniform(0, 2 * math.pi)
        hgt = random.uniform(1.0, 2.2)
        fp = [Vector(O) + Vector((x + math.cos(a) * 0.5 * t * t, y + math.sin(a) * 0.5 * t * t, hgt * t)) for t in (i / 8 for i in range(9))]
        strip("fern", fp, [0.05 + 0.35 * math.sin(math.pi * t) ** 0.7 for t in (i / 8 for i in range(9))], painted("fern.png", 1.0, "UV"), up=(math.cos(a), math.sin(a), 0))
    plane("water_surface", Vector(O) + Vector((0, -20, 9)), (200, 200), (math.pi, 0, 0), flatcard("water_surface.png", 0.8))
    card("trilobite", "TRILOBITE-LOOKUP.png", 0.42, Vector(O) + Vector((0.4, -3.0, 0)), cam, shadow_w=1.1)
    add_ring(O, 20)
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 3.0, "#E8FFF8", rot=deg(15, 0, 10), angle=25)
    light("fill", "AREA", Vector(O) + Vector((0, 3, 3)), 400, "#D8FFF6", rot=deg(-60, 0, 0), size=8)
    return "LS7", (Vector(O) + Vector((0.3, 0.8, 0.45)), Vector(O) + Vector((0, -14, 7.5)), 13, 6.0)


def set_dawn(O):
    plane("grass", O, (300, 300), (0, 0, 0), painted("grass.png", 0.3))
    for k in range(40):
        x, y = random.uniform(-3, 14), random.uniform(-8, 8)
        for j in range(6):
            cyl("blade", Vector(O) + Vector((x + random.uniform(-0.2, 0.2), y + random.uniform(-0.2, 0.2), 0.35)), 0.05, random.uniform(0.5, 0.9), painted("grass.png", 3.0), r2=0.0, verts=6)
    blob("rock", Vector(O) + Vector((3.0, 2.2, 0.2)), 0.7, painted("rock.png", 1.2), scale=(1.4, 1.1, 0.7), sub=1)
    for k in range(10):
        blob("rock_s", Vector(O) + Vector((random.uniform(2, 12), random.uniform(-6, 6), 0.05)), random.uniform(0.15, 0.4), painted("rock.png", 1.5), scale=(1.3, 1, 0.6), sub=1)
    for k in range(10):
        x, y = random.uniform(1.5, 12), random.uniform(-6, 6)
        for j in range(6):
            a = j / 6 * 2 * math.pi + random.uniform(-0.3, 0.3)
            hgt = random.uniform(0.6, 1.2)
            fp = [Vector(O) + Vector((x + math.cos(a) * 0.6 * t, y + math.sin(a) * 0.6 * t, hgt * (t - 0.6 * t * t))) for t in (i / 8 for i in range(9))]
            strip("fern", fp, [0.04 + 0.22 * math.sin(math.pi * t) ** 0.7 for t in (i / 8 for i in range(9))], painted("fern.png", 1.0, "UV"))
    for k in range(5):
        x, y = random.uniform(25, 60), random.uniform(-25, 25)
        cyl("tree_trunk", Vector(O) + Vector((x, y, 2)), 0.3, 4, painted("bark.png", 1.0))
        blob("tree_top", Vector(O) + Vector((x, y, 5)), 2.2, painted("pine.png", 0.8), scale=(1, 1, 0.8))
    for k in range(9):
        blob("hill", Vector(O) + Vector((90 + random.uniform(0, 40), -160 + k * 40, -10)), random.uniform(25, 45), painted("hills.png", 0.15), scale=(1, 1.6, 0.45))
    card("dino", "DINO-LOOKUP.png", 1.0, Vector(O) + Vector((4.0, -0.3, 0)), cam)
    light("sun", "SUN", Vector(O) + Vector((0, 0, 20)), 1.8, "#FFE2C0", rot=deg(0, 78, 0), angle=15)
    light("fill", "AREA", Vector(O) + Vector((-3, 0, 4)), 400, "#F0E6FF", rot=deg(0, -70, 0), size=8)
    return "LS8", (Vector(O) + Vector((0, 0.3, 0.9)), Vector(O) + Vector((30, -2.0, 4)), 22, 8.0)


def bx(name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0, O=(0, 0, 0)):
    return box(name, Vector(O) + Vector(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)), (x1 - x0, y1 - y0, z1 - z0), mat, bevel)


def set_bedroom(O):
    """BG-BEDROOM-MORNING, ported from the approved look test (ep003_lookdev_bedroom.py)."""
    import bmesh
    O = Vector(O)
    WALL, FLOOR, TRIM = painted("wallpaper.png", 0.7), painted("floor.png", 0.55), painted("trim.png", 1.2)
    CEIL, CURTAIN, CUSHION = painted("ceiling.png", 0.5), painted("curtain.png", 1.0, "UV"), painted("cushion.png", 1.5)
    BRASS, ROCK, GLOBE = painted("brass.png", 2.0), painted("rock.png", 6.0), painted("earth_map.png", 1.0, "UV", lift=1.05)
    WX0, WX1, WZ0, WZ1, WY = 0.0, 1.6, 0.9, 2.4, 3.2
    plane("floor", O + Vector((0, 0.1, 0)), (6.4, 6.4), (0, 0, 0), FLOOR)
    plane("ceiling", O + Vector((0, 0.1, 3.2)), (6.4, 6.4), (math.pi, 0, 0), CEIL)
    bx("wall_L", -3.2, WX0, WY, WY + 0.25, 0, 3.2, WALL, O=O); bx("wall_R", WX1, 3.2, WY, WY + 0.25, 0, 3.2, WALL, O=O)
    bx("wall_low", WX0, WX1, WY, WY + 0.25, 0, WZ0, WALL, O=O); bx("wall_top", WX0, WX1, WY, WY + 0.25, WZ1, 3.2, WALL, O=O)
    bx("reveal_top", WX0, WX1, WY, WY + 0.3, WZ1 - 0.02, WZ1 + 0.02, TRIM, O=O)
    bx("wall_side", -2.7, -2.45, -3, WY, 0, 3.2, WALL, O=O)
    bx("baseboard_back", -2.45, 3.2, WY - 0.04, WY, 0, 0.16, TRIM, 0.01, O=O); bx("baseboard_side", -2.45, -2.41, -3, WY, 0, 0.16, TRIM, 0.01, O=O)
    bx("crown", -2.45, 3.2, WY - 0.08, WY, 3.05, 3.2, TRIM, 0.02, O=O)
    F = 0.12
    for nm, a in (("fr_L", (WX0 - F, WX0, WZ0 - F, WZ1 + F)), ("fr_R", (WX1, WX1 + F, WZ0 - F, WZ1 + F)), ("fr_B", (WX0 - F, WX1 + F, WZ0 - F, WZ0)),
                  ("fr_T", (WX0 - F, WX1 + F, WZ1, WZ1 + F))):   # one open pane: no bars across the ring (creator, 2026-11-03)
        bx(nm, a[0], a[1], WY - 0.06, WY + 0.3, a[2], a[3], TRIM, 0.025, O=O)
    bx("seat", WX0 - 0.3, WX1 + 0.3, WY - 0.55, WY, 0, 0.5, TRIM, 0.03, O=O)
    bx("cushion", WX0 - 0.25, WX1 + 0.25, WY - 0.52, WY - 0.02, 0.5, 0.62, CUSHION, 0.05, O=O)
    cyl("rod", O + Vector((0.8, WY - 0.12, 2.62)), 0.025, 2.9, BRASS, rot=(0, math.radians(90), 0))
    for x in (-0.65, 2.25):
        sphere("rod_knob", O + Vector((x, WY - 0.12, 2.62)), 0.05, BRASS)
    curtains = []
    for name, x0, x1, gather in (("curtain_L", -0.7, 0.22, 1.0), ("curtain_R", 1.38, 2.3, -1.0)):
        bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=60, y_segments=8, size=0.5, calc_uvs=True)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
        w, h = x1 - x0, 2.5
        for v in me.vertices:
            u, t = v.co.x + 0.5, v.co.y + 0.5
            depth = 0.05 * (1 + gather * (1 - t)) * math.sin(u * math.pi * 10)
            v.co = Vector((x0 + u * w * (1 - 0.25 * gather * (1 - t)) + (0.25 * gather * (1 - t) * w if gather < 0 else 0), WY - 0.16 + depth, 0.12 + t * h))
        me.materials.append(CURTAIN)
        for p in me.polygons: p.use_smooth = True
        o.location = O
        curtains.append(o)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=0.012, location=O + Vector((0.55, 1.6, 0.006)))
    rug = bpy.context.active_object; rug.scale = (1.25, 0.85, 1); rug.data.materials.append(painted("rug.png", 1.0, "UV"))
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.uv.cylinder_project(); bpy.ops.object.mode_set(mode="OBJECT")
    bx("shelf", -2.45, -2.05, 0.8, 2.2, 1.72, 1.78, TRIM, 0.01, O=O)
    x = 0.85
    for i in range(9):
        h, w = random.uniform(0.22, 0.32), random.uniform(0.06, 0.1)
        bx(f"book{i}", -2.43, -2.12, x, x + w, 1.78, 1.78 + h, painted(random.choice(["toy_red.png", "toy_cream.png", "rug.png", "curtain.png", "brass.png"]), 3.0), 0.008, O=O)
        x += w + 0.01
    bx("table_top", -1.75, -0.85, 0.25, 0.95, 0.72, 0.78, TRIM, 0.02, O=O)
    for lx, ly in ((-1.68, 0.32), (-0.92, 0.32), (-1.68, 0.88), (-0.92, 0.88)):
        bx("leg", lx - 0.03, lx + 0.03, ly - 0.03, ly + 0.03, 0, 0.72, TRIM, 0.01, O=O)
    G = O + Vector((-1.35, 0.62, 1.08))
    cyl("globe_base", Vector((G.x, G.y, O.z + 0.80)), 0.09, 0.04, BRASS); cyl("globe_stem", Vector((G.x, G.y, O.z + 0.86)), 0.015, 0.1, BRASS)
    g = sphere("desk_globe", G, 0.17, GLOBE); g.rotation_euler = (math.radians(23), 0, math.radians(30))
    rocks, tilt = [], math.radians(23)
    for i in range(46):
        a = i / 46 * 2 * math.pi + random.uniform(-0.04, 0.04)
        r = random.uniform(0.26, 0.31)
        p = Vector((r * math.cos(a), r * math.sin(a), random.uniform(-0.006, 0.006)))
        p = Vector((p.x, p.y * math.cos(tilt) - p.z * math.sin(tilt), p.y * math.sin(tilt) + p.z * math.cos(tilt)))
        rk = blob("desk_rock", G + p, random.uniform(0.010, 0.018), ROCK, scale=(random.uniform(0.8, 1.3), random.uniform(0.8, 1.3), random.uniform(0.7, 1.1)), sub=1, smooth=False)
        rocks.append((rk, p))
    cyl("rocket_body", O + Vector((-1.0, 0.45, 0.88)), 0.04, 0.2, painted("toy_cream.png", 3.0), verts=24)
    cyl("rocket_tip", O + Vector((-1.0, 0.45, 1.02)), 0.04, 0.08, painted("toy_red.png", 3.0), r2=0.0, verts=24)
    bx("frame", -1.75, -0.55, WY - 0.05, WY, 1.35, 2.25, TRIM, 0.02, O=O)
    plane("picture", O + Vector((-1.15, WY - 0.056, 1.8)), (1.0, 0.75), (math.radians(90), 0, 0), painted("picture.png", 1.0, "UV", lift=1.05))
    plane("saturn_poster", O + Vector((2.0, WY - 0.02, 1.62)), (0.6, 0.6 * 1466 / 1120), (math.radians(90), 0, 0), flatcard("PROP-SATURN-POSTER.png"))
    cyl("pot", O + Vector((1.45, WY - 0.3, 0.74)), 0.11, 0.2, painted("pot.png", 3.0), verts=24)
    for k in range(9):
        a = k * 2 * math.pi / 9
        sphere("leaf", O + Vector((1.45 + 0.1 * math.cos(a), WY - 0.3 + 0.1 * math.sin(a), 0.92 + 0.08 * (k % 3))), 0.09, painted("leaf.png", 4.0), scale=(0.6, 0.6, 1.3))
    for k, (bxx, byy, c) in enumerate(((0.1, 1.2, "toy_red.png"), (0.24, 1.15, "curtain.png"), (0.16, 1.3, "brass.png"))):
        o = bx("block", bxx - 0.06, bxx + 0.06, byy - 0.06, byy + 0.06, 0.012, 0.132, painted(c, 4.0), 0.012, O=O)
        o.rotation_euler.z = random.uniform(-0.5, 0.5)
    add_ring(O, -40)   # window faces +y; mirrored latitude puts the arch in the window's sky
    light("sun", "SUN", O + Vector((0, 5, 5)), 3.2, "#FFE7C2", rot=deg(-58, 0, -12), angle=18)
    light("win", "AREA", O + Vector((0.8, WY - 0.3, 1.65)), 160, "#FFF0D8", rot=deg(90, 0, 0), size=1.6)
    light("fill", "AREA", O + Vector((0.4, -2.6, 2.4)), 260, "#FFF6EA", rot=deg(70, 0, 180), size=4)
    return dict(globe=g, G=G, rocks=rocks, curtains=curtains, window=O + Vector((0.8, WY, 1.65)))


BUILD = [("rooftops", set_rooftops), ("beach", set_beach), ("city", set_city), ("north", set_north),
         ("space", set_space), ("seafloor", set_seafloor), ("dawn", set_dawn)]

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep003_sets"]
    OUT = argv[0]
    SCALE = int(argv[1]) if len(argv) > 1 else 100
    ONLY = argv[2].split(",") if len(argv) > 2 else None
    random.seed(11)
    sc = pc.setup(SCALE)
    camera_obj, aim = pc.camera()
    init(camera_obj)
    STATES = {"LS1": ("sky_day_eq.png", 0.9, "#E2D5C1", 1.35), "LS5": ("sky_cool_eq.png", 0.7, "#B4BED6", 1.45),
              "LS2": ("space_eq.png", 0.3, "#E6E8FF", 1.1), "LS7": ("water_eq.png", 0.85, "#A3CDC9", 1.25), "LS8": ("sky_dawn_eq.png", 0.7, "#C9B9DA", 1.4)}
    for i, (name, fn) in enumerate(BUILD):
        if ONLY and name not in ONLY:
            continue
        col = pc.collection("SET-" + name)
        SETS[name] = (col, *fn(Vector((i * 400.0, 0, 0))))
    os.makedirs(OUT, exist_ok=True)
    for name, (col, state, shot) in SETS.items():
        for other, (c2, *_r) in SETS.items():
            c2.hide_render = other != name
        tex, strength, grade, sat = STATES[state]
        pc.set_world(tex, strength, grade, sat)
        pos, tgt, lens, fstop = shot
        camera_obj.location, aim.location = pos, tgt
        camera_obj.data.lens, camera_obj.data.dof.aperture_fstop = lens, fstop
        pc.face_cards(pos)
        sc.render.filepath = os.path.join(OUT, f"{name}.png")
        bpy.ops.render.render(write_still=True)
        print("WROTE", sc.render.filepath)
