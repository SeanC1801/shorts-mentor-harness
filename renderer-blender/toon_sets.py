"""Shared sets for the flat two-tone 3D look (look test v2, 2026-11-13): the workshop interior and the night street,
and the lighting states that go with them. Built once here, used by lookdev_3d_style_v2.py and motion_test_3d.py.
"""
import math, random
import bpy
from mathutils import Vector
import papercraft as pc
import toon3d as t3
from toon3d import flat, lathe, ball, tube, sign

V = Vector


def B(name, c, size, color, bevel=0.0, rot=(0, 0, 0)):
    return pc.box(name, V(c), size, flat(color), bevel, rot)


def E(name, c, size, color, strength=1.0, rot=(0, 0, 0)):
    return pc.box(name, V(c), size, pc.emit(color, strength), 0.0, rot)


def lamp(name, c, watts, color, soft=0.12):
    o = pc.light(name, "POINT", V(c), watts, color)
    o.data.shadow_soft_size = soft
    return o


def to_dir(v):
    return tuple(V(v).normalized().to_track_quat("Z", "Y").to_euler())


def workshop():
    """Set A: a dense workshop interior (warm). Returns its collection."""
    WS = pc.collection("WORKSHOP")
    B("floor", (0, -1.5, -0.05), (5.6, 9.2, 0.1), "#C98B4E")
    for k in range(9):
        B("plank_seam", (-2.4 + k * 0.6, -1.5, 0.002), (0.02, 9.0, 0.004), "#A8733C")
    B("wall_back", (0, 3.05, 1.5), (5.6, 0.1, 3.1), "#8FCFC2")
    B("wainscot", (0, 2.99, 0.5), (5.4, 0.04, 1.0), "#5FA79B")
    B("wall_right", (2.75, -1.5, 1.5), (0.1, 9.2, 3.1), "#84C5B8")
    B("wall_front", (0, -6.1, 1.5), (5.6, 0.1, 3.1), "#84C5B8")
    B("ceiling", (0, -1.5, 3.05), (5.6, 9.2, 0.1), "#EDE6D6")
    WY0, WY1, WZ0, WZ1 = 0.5, 2.3, 1.05, 2.35                      # the window opening in the left wall
    B("wall_left_low", (-2.75, -1.5, WZ0 / 2), (0.1, 9.2, WZ0), "#84C5B8")
    B("wall_left_high", (-2.75, -1.5, (WZ1 + 3.05) / 2), (0.1, 9.2, 3.05 - WZ1), "#84C5B8")
    B("wall_left_front", (-2.75, (-6.1 + WY0) / 2, (WZ0 + WZ1) / 2), (0.1, WY0 + 6.1, WZ1 - WZ0), "#84C5B8")
    B("wall_left_back", (-2.75, (WY1 + 3.1) / 2, (WZ0 + WZ1) / 2), (0.1, 3.1 - WY1, WZ1 - WZ0), "#84C5B8")
    for zz in (WZ0 - 0.03, WZ1 + 0.03):
        B("window_trim", (-2.69, (WY0 + WY1) / 2, zz), (0.08, WY1 - WY0 + 0.16, 0.08), "#FFFFFF")
    for yy in (WY0 - 0.03, WY1 + 0.03):
        B("window_trim", (-2.69, yy, (WZ0 + WZ1) / 2), (0.08, 0.08, WZ1 - WZ0 + 0.12), "#FFFFFF")
    for k in range(7):                                              # blinds: the sun draws stripes across the room
        B("blind", (-2.72, (WY0 + WY1) / 2, WZ0 + 0.1 + k * 0.19), (0.15, WY1 - WY0, 0.025), "#F3EDE0", rot=(0, math.radians(32), 0))
    # workbench with drawers along the back wall
    B("bench", (0.3, 2.62, 0.45), (3.4, 0.72, 0.9), "#D9A066", 0.02)
    B("bench_top", (0.3, 2.6, 0.93), (3.56, 0.8, 0.07), "#B9763E", 0.02)
    for r in range(2):
        for k in range(3):
            c = V((-0.82 + k * 1.12, 2.25, 0.26 + r * 0.38))
            B("drawer", c, (1.0, 0.03, 0.3), "#E9BD86", 0.015)
            B("drawer_handle", c + V((0, -0.03, 0)), (0.28, 0.03, 0.04), "#FFFFFF", 0.01)
    # pegboard and tools
    B("pegboard", (0.2, 2.985, 1.82), (2.3, 0.04, 1.1), "#E3B576", 0.01)
    for i in range(11):
        for j in range(5):
            ball("peg_hole", V((-0.8 + i * 0.2, 2.96, 1.4 + j * 0.21)), 0.012, flat("#B98A4E"), scale=(1, 0.3, 1))
    B("hammer_handle", (-0.62, 2.95, 1.75), (0.05, 0.03, 0.5), "#8A5A35", 0.01, rot=(0, math.radians(-12), 0))
    B("hammer_head", (-0.57, 2.94, 2.0), (0.24, 0.06, 0.1), "#8D97A6", 0.02, rot=(0, math.radians(-12), 0))
    B("saw_blade", (0.12, 2.95, 1.95), (0.62, 0.02, 0.15), "#C9D2DC", rot=(0, math.radians(8), 0))
    B("saw_handle", (-0.24, 2.94, 1.9), (0.2, 0.04, 0.2), "#D8503F", 0.03, rot=(0, math.radians(8), 0))
    tube("wrench", [(0.72, 2.95, 1.55), (0.74, 2.95, 1.8), (0.72, 2.95, 2.02)], 0.03, flat("#8D97A6"))
    ball("wrench_head", V((0.72, 2.95, 2.06)), 0.07, flat("#8D97A6"), scale=(1, 0.4, 1))
    for k, col in enumerate(("#F2C84B", "#3FA58C", "#D8503F")):
        B("screwdriver_grip", (1.0 + k * 0.12, 2.95, 2.05), (0.06, 0.05, 0.2), col, 0.02)
        B("screwdriver_shaft", (1.0 + k * 0.12, 2.95, 1.83), (0.02, 0.02, 0.26), "#C9D2DC")
    ball("tape_roll", V((0.2, 2.94, 1.52)), 0.11, flat("#F2C84B"), scale=(1, 0.35, 1))
    ball("tape_hole", V((0.2, 2.92, 1.52)), 0.05, flat("#E3B576"), scale=(1, 0.3, 1))
    # shelf with jars and books above the pegboard, a sign above that
    B("shelf", (0.2, 2.9, 2.48), (2.5, 0.24, 0.05), "#B9763E", 0.01)
    for k, (col, h) in enumerate((("#D8503F", 0.22), ("#F2C84B", 0.3), ("#3D7BE0", 0.18), ("#3FA58C", 0.26), ("#B56FE0", 0.2))):
        pc.cyl("jar", V((-0.8 + k * 0.24, 2.9, 2.505 + h / 2)), 0.09, h, flat(col), verts=20)
        pc.cyl("jar_lid", V((-0.8 + k * 0.24, 2.9, 2.52 + h)), 0.095, 0.03, flat("#2B2B33"), verts=20)
    for k, col in enumerate(("#D8503F", "#3D7BE0", "#F6DFA6", "#3FA58C", "#F2B10C", "#7C5CD6")):
        B("book", (0.55 + k * 0.105, 2.9, 2.67 + 0.02 * (k % 2)), (0.09, 0.2, 0.32 + 0.04 * (k % 2)), col, 0.008)
    sign("FOO LAB", (-1.05, 2.985, 2.78), 0.24, "#FFFFFF")
    B("poster", (2.05, 2.985, 1.85), (0.75, 0.02, 1.0), "#FFF8E8", 0.01)
    sign("PLAN A", (2.05, 2.96, 2.15), 0.14, "#D8503F")
    for k in range(3):
        B("poster_line", (2.05, 2.97, 1.92 - k * 0.14), (0.52, 0.01, 0.035), "#9FB4C8")
    ball("poster_dot", V((1.86, 2.965, 1.52)), 0.07, flat("#3FA58C"), scale=(1, 0.2, 1))
    ball("poster_dot", V((2.2, 2.965, 1.52)), 0.07, flat("#F2B10C"), scale=(1, 0.2, 1))
    lathe("clock", [(0, 0), (0.24, 0), (0.24, 0.03), (0, 0.03)], flat("#FFFFFF"), segs=32).location = (-1.55, 2.99, 2.1)
    bpy.data.objects["clock"].rotation_euler = (math.radians(90), 0, 0)
    B("clock_hand", (-1.55, 2.94, 2.17), (0.025, 0.02, 0.16), "#2B2B33")
    B("clock_hand", (-1.49, 2.94, 2.1), (0.13, 0.02, 0.025), "#D8503F")
    # on the bench: a desk lamp, a glowing jar with a label, papers, a mug, a globe
    ball("lamp_base", V((-1.05, 2.6, 0.985)), 0.12, flat("#3D7BE0"), scale=(1, 1, 0.3))
    tube("lamp_arm", [(-1.05, 2.6, 1.0), (-1.18, 2.62, 1.3), (-0.9, 2.55, 1.52)], 0.018, flat("#2B2B33"))
    lathe("lamp_shade", [(0.05, 0.0), (0.17, -0.2), (0.16, -0.21), (0.04, -0.01)], flat("#3D7BE0"), segs=24).location = (-0.86, 2.53, 1.58)
    bpy.data.objects["lamp_shade"].rotation_euler = (math.radians(-25), math.radians(-20), 0)
    ball("lamp_bulb", V((-0.8, 2.47, 1.43)), 0.055, pc.emit("#FFF1C2", 3.2))
    lamp("desk_light", (-0.78, 2.4, 1.36), 55, "#FFD9A0")
    pc.cyl("glow_jar", V((0.55, 2.52, 1.16)), 0.17, 0.36, pc.emit("#FFB23C", 2.0), verts=28)
    pc.cyl("glow_jar_lid", V((0.55, 2.52, 1.36)), 0.18, 0.04, flat("#8D97A6"), verts=28)
    B("jar_label", (0.55, 2.345, 1.14), (0.2, 0.01, 0.1), "#FFF8E8")
    sign("DO NOT", (0.55, 2.335, 1.165), 0.04, "#D8503F")
    sign("TOUCH", (0.55, 2.335, 1.118), 0.04, "#D8503F")
    lamp("jar_light", (0.55, 2.2, 1.2), 22, "#FFA43C", soft=0.2)
    for k in range(3):
        B("paper", (-0.2 + k * 0.05, 2.45 + k * 0.03, 0.968 + k * 0.004), (0.3, 0.4, 0.004), "#FFF8E8", rot=(0, 0, math.radians(-12 + 14 * k)))
    pc.cyl("mug", V((1.25, 2.45, 1.02)), 0.055, 0.11, flat("#D8503F"), verts=20)
    ball("globe", V((1.65, 2.6, 1.2)), 0.16, flat("#3D7BE0"))
    for dx, dz in ((0.03, 0.06), (-0.08, -0.03), (0.1, -0.06)):
        ball("globe_land", V((1.65 + dx, 2.47, 1.2 + dz)), 0.06, flat("#57B85E"), scale=(1, 0.5, 0.8))
    pc.cyl("globe_stand", V((1.65, 2.6, 1.0)), 0.07, 0.06, flat("#8A5A35"), verts=16)
    # right wall: shelves of boxes and books
    B("unit", (2.52, 1.2, 1.1), (0.36, 1.5, 2.2), "#B9763E", 0.02)
    for k in range(4):
        B("unit_shelf", (2.42, 1.2, 0.3 + k * 0.55), (0.34, 1.42, 0.04), "#D9A066")
        for j in range(4):
            col = ("#D8503F", "#3FA58C", "#F2B10C", "#7C5CD6", "#3D7BE0", "#F6DFA6")[(k * 3 + j) % 6]
            B("unit_box", (2.36, 0.68 + j * 0.34, 0.45 + k * 0.55 + 0.03 * (j % 2)), (0.24, 0.26, 0.24 + 0.06 * (j % 2)), col, 0.015)
    # floor: rug, stool, crate, plant; a pendant lamp overhead
    lathe("rug", [(0, 0.006), (1.15, 0.006), (1.15, 0.012), (0, 0.012)], flat("#D8503F"), segs=40).location = (0.2, 0.9, 0)
    lathe("rug_ring", [(0, 0.013), (0.85, 0.013), (0.85, 0.018), (0, 0.018)], flat("#F2C84B"), segs=40).location = (0.2, 0.9, 0)
    lathe("rug_centre", [(0, 0.019), (0.5, 0.019), (0.5, 0.024), (0, 0.024)], flat("#3FA58C"), segs=40).location = (0.2, 0.9, 0)
    pc.cyl("stool_seat", V((-1.5, 1.9, 0.5)), 0.2, 0.06, flat("#D8503F"), verts=24)
    for a in range(3):
        tube("stool_leg", [(-1.5 + 0.1 * math.cos(a * 2.1), 1.9 + 0.1 * math.sin(a * 2.1), 0.48), (-1.5 + 0.2 * math.cos(a * 2.1), 1.9 + 0.2 * math.sin(a * 2.1), 0.0)], 0.018, flat("#8D97A6"))
    B("crate", (1.7, 0.6, 0.22), (0.5, 0.5, 0.44), "#D9A066", 0.02, rot=(0, 0, math.radians(18)))
    B("crate_band", (1.7, 0.6, 0.22), (0.52, 0.52, 0.08), "#B9763E", rot=(0, 0, math.radians(18)))
    pc.cyl("pot", V((-2.2, 2.55, 0.2)), 0.2, 0.4, flat("#B9684A"), verts=20, r2=0.25)
    for k in range(6):
        a = k * 1.05
        ball("leaf", V((-2.2 + 0.2 * math.cos(a), 2.55 + 0.16 * math.sin(a), 0.62 + 0.14 * (k % 3))), 0.17, flat(("#3F9E52", "#57B85E")[k % 2]), scale=(1, 1, 1.25))
    tube("pendant_cord", [(0.2, 1.1, 3.0), (0.2, 1.1, 2.5)], 0.01, flat("#2B2B33"))
    lathe("pendant_shade", [(0.04, 0.0), (0.3, -0.2), (0.29, -0.215), (0.03, -0.01)], flat("#F2B10C"), segs=28).location = (0.2, 1.1, 2.5)
    ball("pendant_bulb", V((0.2, 1.1, 2.33)), 0.07, pc.emit("#FFF1C2", 3.4))
    lamp("pendant_light", (0.2, 1.1, 2.2), 150, "#FFE2B0", soft=0.25)
    return WS


def street(seed=9):
    """Set B: a street at night with shopfronts, neon signs and a street lamp. Returns its collection."""
    rnd = random.Random(seed)
    NEON = []
    SR = pc.collection("STREET")
    pc.plane("road", V((0, 0, 0)), (120, 120), (0, 0, 0), flat("#3B4166"))
    B("sidewalk", (0, 7.2, 0.07), (40, 4.4, 0.14), "#7A7FA0", 0.01)
    B("curb", (0, 4.96, 0.07), (40, 0.12, 0.16), "#A7ABC6")
    for k in range(6):
        B("crossing", (-2.4 + k * 0.95, 2.4, 0.004), (0.5, 3.0, 0.008), "#C9CCE0")
    SHOPS = [(-6.6, "#C8483B", 4.4, "ARCADE", "#FF5FB0"), (-2.2, "#2F9480", 5.2, "NOODLES", "#FFD23C"), (2.2, "#D9960E", 4.0, "BOOKS", "#5FE3FF"), (6.6, "#6A4FC4", 4.8, "OPEN 24H", "#7CFF9B")]
    for sx, col, h, word, ncol in SHOPS:
        B("shop", (sx, 11.4, h / 2), (4.2, 4.0, h), col, 0.03)
        B("shop_base", (sx, 9.38, 0.3), (4.2, 0.06, 0.6), "#2B2F4F")
        B("shop_door", (sx - 1.35, 9.37, 1.15), (0.95, 0.08, 2.1), "#2B2F4F", 0.02)
        E("door_glass", (sx - 1.35, 9.32, 1.45), (0.6, 0.02, 1.1), "#FFD98A", 1.6)
        B("shopwindow_frame", (sx + 0.55, 9.37, 1.45), (2.5, 0.08, 1.7), "#FFFFFF", 0.02)
        E("shopwindow", (sx + 0.55, 9.32, 1.45), (2.3, 0.02, 1.5), "#FFE2A0", 1.5)
        for k in range(4):                                         # things on display, as dark shapes against the light
            B("display", (sx - 0.3 + k * 0.56, 9.29, 0.95 + 0.12 * (k % 2)), (0.3, 0.02, 0.4 + 0.24 * (k % 2)), ("#2B2F4F", "#C8483B", "#2F9480", "#6A4FC4")[k % 4])
        B("awning", (sx + 0.55, 9.0, 2.55), (2.8, 0.9, 0.06), ("#FFFFFF", "#F2C84B")[int(sx) % 2], rot=(math.radians(18), 0, 0))
        B("signboard", (sx, 9.33, 3.25), (3.5, 0.1, 0.7), "#1B1F3D", 0.02)
        sign(word, (sx, 9.26, 3.25), 0.4, ncol, strength=3.4)
        NEON.append(lamp("neon_light", (sx, 8.6, 3.2), 30, ncol, soft=0.3))
        lamp("window_light", (sx + 0.55, 8.6, 1.4), 60, "#FFD08A", soft=0.3)
        for k in range(2):                                         # upstairs windows, some lit
            lit = rnd.random() < 0.6
            if h > 4.3:
                (E if lit else B)("upstairs_window", (sx - 0.9 + k * 1.8, 9.37, h - 0.75), (0.8, 0.06, 0.7), "#FFD98A" if lit else "#1B1F3D", *((1.8,) if lit else ()))
    # street furniture
    tube("lamp_post", [(-4.3, 6.0, 0.14), (-4.3, 6.0, 3.6), (-3.9, 5.8, 3.9), (-3.5, 5.6, 3.8)], 0.06, flat("#2B2F4F"), r_end=0.045)
    ball("lamp_head", V((-3.45, 5.58, 3.74)), 0.2, flat("#2B2F4F"), scale=(1.3, 1, 0.5))
    ball("lamp_glow", V((-3.45, 5.58, 3.66)), 0.14, pc.emit("#FFF1C2", 3.6), scale=(1.2, 1, 0.5))
    lamp("street_light", (-3.45, 5.55, 3.4), 420, "#FFE2B0", soft=0.3)
    B("vending", (0.25, 8.9, 1.0), (0.95, 0.7, 1.72), "#3D7BE0", 0.04)
    E("vending_panel", (0.13, 8.53, 1.25), (0.55, 0.02, 0.9), "#CFF3FF", 1.3)
    for r in range(3):
        for k in range(4):
            B("can", (-0.08 + k * 0.14, 8.51, 0.95 + r * 0.28), (0.08, 0.02, 0.18), ("#D8503F", "#F2C84B", "#3FA58C", "#B56FE0")[(r + k) % 4])
    sign("DRINKS", (0.25, 8.54, 1.78), 0.11, "#FFFFFF", strength=2.4)
    lamp("vending_light", (0.2, 7.9, 1.3), 45, "#BFEFFF", soft=0.25)
    lamp("neon_spill", (-1.55, 4.5, 1.6), 26, "#FF9FCB", soft=0.4)      # pink light from the sign across the street (lights the close-up)
    pc.cyl("hydrant", V((3.3, 5.6, 0.4)), 0.13, 0.5, flat("#D8503F"), verts=16)
    ball("hydrant_cap", V((3.3, 5.6, 0.68)), 0.14, flat("#D8503F"))
    B("bench_seat", (5.0, 8.7, 0.5), (1.6, 0.4, 0.07), "#8A5A35", 0.02)
    B("bench_back", (5.0, 8.88, 0.82), (1.6, 0.06, 0.4), "#8A5A35", 0.02)
    for s in (-1, 1):
        B("bench_leg", (5.0 + s * 0.65, 8.7, 0.3), (0.07, 0.36, 0.36), "#2B2F4F")
    pc.cyl("bin", V((-0.9, 8.9, 0.5)), 0.24, 0.75, flat("#4A4E6A"), verts=18, r2=0.28)
    # skyline behind, power lines, moon and stars
    for k in range(11):
        x = -24 + k * 4.8 + rnd.uniform(-1, 1); hh = rnd.uniform(7, 15)
        B("tower", (x, 22 + rnd.uniform(0, 6), hh / 2), (rnd.uniform(3, 4.4), 3, hh), ("#232A55", "#1E2450", "#2A3163")[k % 3])
        for j in range(rnd.randint(3, 7)):
            E("tower_window", (x + rnd.uniform(-1.3, 1.3), 20.4, rnd.uniform(5.5, hh - 0.8)), (0.34, 0.05, 0.42), "#FFD98A", 1.4)
    tube("power_pole", [(8.9, 6.3, 0.14), (8.9, 6.3, 6.2)], 0.09, flat("#2B2F4F"))
    B("power_arm", (8.9, 6.3, 5.8), (1.4, 0.08, 0.08), "#2B2F4F")
    for dz in (0.0, 0.25):
        tube("power_line", [(8.9, 6.3, 5.8 + dz), (0, 6.6, 5.0 + dz), (-12, 7.0, 5.9 + dz)], 0.012, flat("#1B1F3D"))
    MOON = ball("moon", V((40, 330, 150)), 12, pc.emit("#F6F2DC", 1.5))
    for k in range(110):
        a, el = rnd.uniform(-1.2, 1.2), rnd.uniform(0.15, 1.2)
        ball("star", V((math.sin(a) * math.cos(el), math.cos(a) * math.cos(el), math.sin(el))) * 420, rnd.uniform(0.5, 1.1), pc.emit("#FFFFFF", 2.4))
    return SR


def state(name, SUN):
    """Lighting and colour for each kind of shot."""
    if name == "studio":
        t3.sky("#EFE9DC", "#EFE9DC", "#E7DFCF")
        SUN.rotation_euler, SUN.data.energy, SUN.data.color = to_dir((-0.30, -0.62, 0.72)), 4.0, (1, 1, 1)
        t3.set_shade((0.62, 0.62, 0.86), t3.AMBIENT + 0.2 * 4.0 / math.pi, hi=t3.AMBIENT + 1.05 * 4.0 / math.pi)
        pc.G_RGB.outputs[0].default_value = (1, 1, 1, 1)
    elif name == "warm":      # workshop: late sun through the blinds, lamps on
        t3.sky("#FFC98A", "#FFE2B8", "#C98B4E", ambient="#FFE6CC", level=0.24)
        SUN.rotation_euler, SUN.data.energy, SUN.data.color = to_dir((-0.70, -0.42, 0.42)), 5.5, pc.hexcol("#FFD9A8")[:3]
        t3.set_shade((0.60, 0.50, 0.68), 0.24 + 0.34, hi=0.24 + 1.25, light=0.65)
        pc.G_RGB.outputs[0].default_value = pc.hexcol("#FFF3E4")
    else:                     # night street: only lamps, windows and signs reach the "lit" tone
        t3.sky("#060A26", "#22357E", "#3B4166", ambient="#8FA0FF", level=0.16)
        SUN.rotation_euler, SUN.data.energy, SUN.data.color = to_dir((0.4, -0.5, 0.75)), 0.5, pc.hexcol("#AFC0FF")[:3]
        t3.set_shade((0.36, 0.40, 0.78), 0.16 + 0.42, hi=0.16 + 2.2, light=0.8)
        pc.G_RGB.outputs[0].default_value = pc.hexcol("#F1F0FF")
    pc.G_SAT.outputs[0].default_value = 1.0
