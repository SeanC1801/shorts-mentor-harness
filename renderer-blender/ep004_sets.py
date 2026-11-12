"""EP004 sets (set-specs v1, approved 2026-11-11), cel look (visual-style v3).

New file: EP003's set files are not edited. Shared helpers come from papercraft.py unchanged.
So far: BG-WINDOW-RAINY (look test). Units are metres; the house front wall faces -Y at y=0,
the kid's room floor is z=0 and the outside ground is z=-0.45.
"""
import math, random
import bpy
from mathutils import Vector
import papercraft as pc
from papercraft import painted, box, plane, cyl, blob, wedge, strip, card, light, emit

V = Vector


def deg(*a): return tuple(math.radians(x) for x in a)


def glassy(color, alpha, strength=1.0):
    """See-through, unlit, not inked (emit() with alpha; keyed by alpha so callers get distinct materials)."""
    return emit(color, strength, alpha=alpha)


# ---------------- BG-WINDOW-RAINY ----------------
WIN_W, WIN_H, SILL_Z = 1.40, 1.30, 0.55          # window opening and sill height above the room floor
WALL_X, WALL_TOP, GROUND = 2.4, 2.9, -0.45


def window_set(O, rng_seed=7):
    """Build both states; returns dict(rain=[objs], dry=[objs], kid_curious, kid_wistful, lamp_light)."""
    random.seed(rng_seed)
    O = V(O)
    H = {"rain": [], "dry": []}
    siding, teal, cream = painted("ep4_siding_yellow.png", 0.9), painted("ep4_trim_teal.png", 2.0), painted("ep4_trim_cream.png", 2.0)
    x0, x1, z0, z1 = -WIN_W / 2, WIN_W / 2, SILL_Z, SILL_Z + WIN_H
    T = 0.25  # wall thickness
    # front wall around the opening (foreground of the room, mid stage of the exterior)
    # one wall with the opening cut out (a single mesh, so the ink draws no seams)
    wall = box("wall", O + V((0, T / 2, (GROUND + WALL_TOP) / 2)), (2 * WALL_X, T, WALL_TOP - GROUND), siding)
    cutter = box("wall_cutter", O + V((0, T / 2, (z0 + z1) / 2)), (WIN_W, T * 3, WIN_H), None)
    bo = wall.modifiers.new("opening", "BOOLEAN"); bo.object, bo.operation = cutter, "DIFFERENCE"
    bpy.context.view_layer.objects.active = wall
    bpy.ops.object.modifier_apply(modifier="opening")
    bpy.data.objects.remove(cutter, do_unlink=True)
    # teal frame: four bars and a cross mullion, set slightly proud of the wall
    f, d = 0.10, 0.16
    box("frame_T", O + V((0, -0.03, z1 + f / 2)), (WIN_W + 2 * f, d, f), teal, 0.015)
    box("frame_B", O + V((0, -0.03, z0 - f / 2)), (WIN_W + 2 * f, d, f), teal, 0.015)
    box("frame_L", O + V((x0 - f / 2, -0.03, (z0 + z1) / 2)), (f, d, WIN_H), teal, 0.015)
    box("frame_R", O + V((x1 + f / 2, -0.03, (z0 + z1) / 2)), (f, d, WIN_H), teal, 0.015)
    box("mullion_V", O + V((0, 0.06, (z0 + z1) / 2)), (0.06, 0.06, WIN_H), teal, 0.01)
    box("mullion_H", O + V((0, 0.06, z0 + WIN_H * 0.62)), (WIN_W, 0.06, 0.06), teal, 0.01)
    # cream sill and a planter box with flowers (exterior foreground strip)
    box("sill", O + V((0, -0.16, z0 - f - 0.04)), (WIN_W + 0.5, 0.36, 0.08), cream, 0.02)
    box("planter", O + V((0, -0.30, z0 - f - 0.26)), (WIN_W + 0.2, 0.34, 0.32), painted("ep4_planter.png", 1.5), 0.03)
    box("soil", O + V((0, -0.30, z0 - f - 0.11)), (WIN_W + 0.1, 0.28, 0.03), painted("ep4_soil.png", 2.0))
    for k in range(14):
        x = -WIN_W / 2 + 0.1 + k * (WIN_W - 0.2) / 13 + random.uniform(-0.04, 0.04)
        blob("leaves", O + V((x, -0.30 + random.uniform(-0.08, 0.08), z0 - f - 0.02 + random.uniform(0, 0.08))), 0.10,
             painted("leaf.png", 3.0), scale=(1, 0.8, 0.7), sub=2)
    for k in range(9):
        x = -WIN_W / 2 + 0.15 + k * (WIN_W - 0.3) / 8
        blob("flower", O + V((x, -0.38, z0 - f + 0.10 + random.uniform(0, 0.06))), 0.055,
             painted("ep4_flower_pink.png" if k % 2 else "ep4_flower_white.png", 3.0), scale=(1, 0.7, 1), sub=2)
    # eave, gutter and downpipe at the top of the frame
    box("eave", O + V((0, -0.35, WALL_TOP + 0.08)), (2 * WALL_X + 0.4, 0.9, 0.16), cream, 0.02)
    wedge("roof", O + V((0, 0.6, WALL_TOP + 0.16)), 2.6, 1.5, 2 * WALL_X + 0.6, painted("roof_red.png", 0.6))
    g = cyl("gutter", O + V((0, -0.82, WALL_TOP + 0.02)), 0.08, 2 * WALL_X + 0.4, painted("metal.png", 2.0), rot=deg(0, 90, 0), verts=20)
    cyl("downpipe", O + V((WALL_X - 0.3, -0.09, (GROUND + WALL_TOP) / 2)), 0.055, WALL_TOP - GROUND, painted("metal.png", 2.0), verts=16)
    box("downpipe_elbow", O + V((WALL_X - 0.3, -0.46, WALL_TOP - 0.04)), (0.1, 0.78, 0.1), painted("metal.png", 2.0), 0.03)
    # glass (unlit, see-through) with soft highlight streaks
    plane("glass", O + V((0, 0.08, (z0 + z1) / 2)), (WIN_W, WIN_H), deg(90, 0, 0), glassy("#C9DCEB", 0.07))
    for k, (x, w) in enumerate(((-0.45, 0.10), (-0.28, 0.04), (0.38, 0.07))):
        o = plane("glint", O + V((x, 0.075, (z0 + z1) / 2 + 0.1)), (w, WIN_H * 0.7), deg(90, 0, 25), glassy("#FFFFFF", 0.12 + 0.0011 * k))
    # ---- rainy-only objects: drops on the glass, gutter drips, rain streaks, wet sheen on the sill
    for k in range(34):
        x, z = random.uniform(x0 + 0.05, x1 - 0.05), random.uniform(z0 + 0.05, z1 - 0.05)
        r = random.uniform(0.008, 0.02)
        H["rain"].append(blob("drop", O + V((x, 0.06, z)), r, glassy("#CFE2F0", 0.30), scale=(1, 0.35, 1.3), sub=2))
        H["rain"].append(blob("drop_hl", O + V((x - r * 0.3, 0.05, z + r * 0.4)), r * 0.28, glassy("#F4F8FC", 0.6), scale=(1, 0.3, 1.2), sub=1))
        if random.random() < 0.4:  # a short trail above the drop
            H["rain"].append(plane("trail", O + V((x, 0.065, z + r * 3)), (r * 0.5, r * 5), deg(90, 0, 0), glassy("#CFE2F0", 0.15)))
    hero = blob("PROP-RAINDROP", O + V((0.12, 0.055, 1.12)), 0.05, glassy("#BFD8EC", 0.40), scale=(0.9, 0.35, 1.25), sub=3)
    hl = blob("PROP-RAINDROP_hl", O + V((0.105, 0.035, 1.15)), 0.012, emit("#F4F8FC", 0.95), scale=(1, 0.3, 1.4), sub=2)
    H["rain"] += [hero, hl]
    for k in range(12):
        x = random.uniform(-WALL_X + 0.3, WALL_X - 0.3)
        H["rain"].append(blob("gutter_drip", O + V((x, -0.85, WALL_TOP - 0.15 - random.uniform(0, 0.8))), 0.02, glassy("#DDE7F0", 0.6), scale=(1, 1, 1.8)))
    for k in range(170):
        x, y = random.uniform(-2.6, 2.6), random.uniform(-2.2, -0.6)
        z, L = random.uniform(GROUND - 0.3, WALL_TOP + 0.8), random.uniform(0.15, 0.35)
        H["rain"].append(plane("rain", O + V((x, y, z)), (0.0035, L), deg(90, 0, -6), glassy("#E3EBF3", 0.22)))
    H["rain"].append(plane("sill_wet", O + V((0, -0.16, z0 - f + 0.005)), (WIN_W + 0.4, 0.3), (0, 0, 0), glassy("#FFFFFF", 0.14)))
    # ---- the kid's room behind the glass (warm lamp inside)
    floor, back = painted("floor.png", 0.6), painted("wallpaper.png", 0.8)
    box("room_floor", O + V((0, 2.2, -0.05)), (6.0, 4.2, 0.1), floor)
    box("room_back", O + V((0, 3.6, 1.6)), (6.0, 0.1, 3.4), back)
    box("room_L", O + V((-2.6, 2.2, 1.6)), (0.1, 3.0, 3.4), back)
    box("room_R", O + V((2.6, 2.2, 1.6)), (0.1, 3.0, 3.4), back)
    box("room_ceiling", O + V((0, 2.2, 3.0)), (6.0, 3.0, 0.1), painted("ceiling.png", 0.6))
    for s in (-1, 1):  # striped curtains just inside the frame
        box("curtain", O + V((s * (WIN_W / 2 + 0.05), 0.42, (z0 + z1) / 2 + 0.25)), (0.32, 0.08, WIN_H + 0.7), painted("curtain.png", 1.2), 0.03)
    box("curtain_rod", O + V((0, 0.42, z1 + 0.32)), (WIN_W + 1.0, 0.05, 0.05), painted("brass.png", 2.0))
    # bookshelf (left) and floor lamp (right)
    box("shelf", O + V((-1.25, 3.2, 0.9)), (1.1, 0.5, 1.8), painted("trim.png", 1.0), 0.02)
    for k in range(3):
        box("books", O + V((-1.25, 2.96, 0.35 + k * 0.55)), (0.95, 0.06, 0.38), painted("ep4_books.png", 1.0))
    cyl("lamp_pole", O + V((1.25, 2.9, 0.75)), 0.03, 1.5, painted("brass.png", 2.0))
    cyl("lamp_base", O + V((1.25, 2.9, 0.03)), 0.22, 0.06, painted("brass.png", 2.0))
    shade = cyl("lamp_shade", O + V((1.25, 2.9, 1.55)), 0.34, 0.38, emit("#FFD9A0", 1.5), r2=0.22, verts=32)
    lamp = light("lamp", "POINT", O + V((1.25, 2.9, 1.45)), 220, "#FFC98A")
    lamp.data.shadow_soft_size = 0.6
    # the kid behind the glass (two face cards; the caller shows one)
    kid_c, sh_c = card("kid_curious", "RAINKID-WINDOW-CURIOUS.png", 1.30, O + V((0.36, 0.72, 0.0)))
    kid_w, sh_w = card("kid_wistful", "RAINKID-WINDOW-WISTFUL.png", 1.30, O + V((0.36, 0.72, 0.0)))
    # ---- exterior ground, path, neighbours and a picket fence (foreground for wide views)
    grass = painted("ep4_lawn.png", 0.5)
    box("ground", O + V((0, -9.0, GROUND - 0.05)), (40, 18, 0.1), grass)
    box("path", O + V((-2.2, -4.0, GROUND + 0.005)), (1.0, 8.0, 0.02), painted("concrete.png", 0.8))
    for k in range(16):
        x = -6 + k * 0.8
        box("picket", O + V((x, -7.6, GROUND + 0.45)), (0.12, 0.05, 0.9), cream, 0.02)
        wedge("picket_top", O + V((x, -7.6, GROUND + 0.9)), 0.05, 0.10, 0.12, cream, rotz=0, bevel=0.0)
    for y in (0.35, 0.75):
        box("fence_rail", O + V((0, -7.63, GROUND + y)), (12.8, 0.04, 0.08), cream)
    for s, wall, roof in ((-1, "plaster_blue.png", "roof_blue.png"), (1, "plaster_pink.png", "roof_red.png")):
        c = O + V((s * 5.6, 2.6, GROUND))
        box("neighbour", c + V((0, 0, 1.8)), (4.0, 4.0, 3.6), painted(wall, 0.5), 0.05)
        wedge("neighbour_roof", c + V((0, 0, 3.6)), 4.6, 1.6, 4.4, painted(roof, 0.6))
    for k in range(5):
        blob("bush", O + V((random.uniform(-4, 4), random.uniform(-7.2, -6.2), GROUND + 0.25)), random.uniform(0.35, 0.6),
             painted("leaf.png", 1.5), scale=(1.4, 1, 0.8))
    rain_cloud = cloud("cloud_grey", O + V((0.6, -3.4, 11.0)), 3.6, tex="ep4_cloud_grey.png", seed=2)
    H["rain"] += rain_cloud
    streaks = [o for o in H["rain"] if o.name.startswith("rain")]
    return dict(rain=H["rain"], streaks=[(o, o.location.copy()) for o in streaks], hero=(hero, hl),
                kid_curious=(kid_c, sh_c), kid_wistful=(kid_w, sh_w), lamp=lamp, shade=shade)


# ---------------- props shared by several sets ----------------
def cloud(name, c, size, tex="ep4_cloud.png", seed=1, puffs=14):
    """PROP-CLOUD: overlapping puffs, cel-banded white to lavender, inked. Returns the puff objects."""
    rnd = random.Random(seed)
    out = []
    for k in range(puffs):
        a = k / puffs * 2 * math.pi
        r = size * rnd.uniform(0.35, 0.6)
        off = V((math.cos(a) * size * rnd.uniform(0.3, 0.9), math.sin(a) * size * rnd.uniform(0.2, 0.6), rnd.uniform(-0.15, 0.35) * size))
        out.append(blob(name, V(c) + off, r, painted(tex, 0.2), scale=(1.2, 1, 0.8), sub=3))
    out.append(blob(name, V(c) + V((0, 0, 0.1 * size)), size * 0.75, painted(tex, 0.2), scale=(1.3, 1, 0.8), sub=3))
    return out


def hero_drop(name, c, r, alpha_key=0.4):
    """PROP-RAINDROP at flight size: see-through body plus a small highlight (returns body, highlight)."""
    body = blob(name, V(c), r, glassy("#BFD8EC", alpha_key), scale=(0.9, 0.9, 1.25), sub=3)
    hl = blob(name + "_hl", V(c), r * 0.25, emit("#F4F8FC", 0.95), scale=(1, 1, 1.4), sub=2)
    return body, hl


# ---------------- BG-SEA-SUNNY ----------------
def sea_set(O, seed=3):
    """Open sea at z=0 around O, sun low ahead (+Y), a white cloud above O at z=30, wave crests near O."""
    rnd = random.Random(seed)
    O = V(O)
    plane("sea", O + V((0, 150, 0)), (600, 600), (0, 0, math.radians(90)), painted("sea.png", 0.35))
    waves = []
    for k in range(60):
        x, y = rnd.uniform(-14, 14), rnd.uniform(-6, 40)
        w = blob("wave", O + V((x, y, -0.05)), rnd.uniform(0.25, 0.5), painted("ep4_wave.png", 1.0), scale=(rnd.uniform(4, 8), 0.8, 0.5), sub=2)
        waves.append((w, w.location.copy(), rnd.uniform(0, 6.28)))
    glints = [blob("glint", O + V((rnd.uniform(-8, 8), rnd.uniform(2, 45), 0.06)), 0.05, emit("#FFFBEA", 2.0), scale=(3, 0.6, 0.3), sub=1)
              for _ in range(70)]
    sun = card("sun_disc", "sun_disc.png", 34, O + V((6, 320, 4)), shadow=False)[0]
    sun.data.materials[0] = pc.flatcard("sun_disc.png", 2.0)
    cl = cloud("cloud_white", O + V((0, 0, 31)), 5.0, seed=4)
    for k, (dx, dy, dz, s) in enumerate(((-26, 60, 18, 6), (30, 90, 22, 8), (-40, 140, 26, 9), (18, 40, 14, 4))):
        cloud("cloud_far", O + V((dx, dy, dz)), s, seed=10 + k, puffs=9)
    drop = hero_drop("sea_drop", O + V((0, 0, 28.5)), 0.28)
    rip = []
    for k in range(3):
        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.018, location=O + V((0, 0, 0.04)))
        t = bpy.context.active_object; t.name = "ripple"; t.data.materials.append(glassy("#FFFFFF", 0.5 + 0.001 * k))
        t.hide_render = True; rip.append(t)
    light("sun", "SUN", O + V((0, 0, 10)), 4.5, "#FFF2D6", rot=deg(55, 0, 0), angle=8)
    curls = vapor_curls(O + V((0, 13, 0)), 26, (-3.5, 3.5), (-2.5, 4.0), seed=6)
    return dict(waves=waves, glints=glints, drop=drop, ripples=rip, cloud=cl, curls=curls)


# ---------------- FX-VAPOR-CURLS ----------------
def vapor_curls(O, n, x_rng, y_rng, z0=0.05, height=1.6, seed=5, key=0.25):
    """Faint see-through rising ribbons (stylized: real vapor is invisible). Not inked.
    Returns [(obj, material, base_location, phase)]; animate with curl_step()."""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        A, lam, ph = rnd.uniform(0.08, 0.2), rnd.uniform(0.6, 1.1), rnd.uniform(0, 6.28)
        pts, ws = [], []
        for i in range(17):
            u = i / 16
            z = u * height
            pts.append((A * math.sin(2 * math.pi * z / lam + ph) * (0.4 + u), 0, z))
            ws.append(0.012 + 0.06 * math.sin(math.pi * u) ** 0.8)
        m = emit("#F2FAFF", 1.15, alpha=key + 0.0001 * k)
        o = strip("vapor", pts, ws, m, up=(0, 1, 0))
        o.location = V(O) + V((rnd.uniform(*x_rng), rnd.uniform(*y_rng), z0))
        o.hide_render = True
        out.append((o, m, o.location.copy(), rnd.uniform(0, 1)))
    return out


def curl_step(curls, f, f0, f1, rise=0.06, alpha=0.3, stagger=40):
    """Curls appear one after another from f0, rise, sway and fade; hidden outside [f0, f1)."""
    for k, (o, m, base, ph) in enumerate(curls):
        age = f - (f0 + ph * stagger)
        if f < f0 or f >= f1 or age < 0:
            o.hide_render = True
            continue
        o.hide_render = False
        o.location = base + V((0.15 * math.sin(age * 0.07 + ph * 6), 0, age * rise))
        o.rotation_euler.z = 0.25 * math.sin(age * 0.05 + ph * 3)
        o.scale = (1 + 0.15 * math.sin(age * 0.11 + ph), 1, 1 + age * 0.006)
        fade = min(1.0, age / 12) * max(0.0, min(1.0, (f1 - f) / 8))
        shimmer = 1 + 0.18 * math.sin(age * 0.6 + ph * 10)
        next(nd for nd in m.node_tree.nodes if nd.bl_idname == "ShaderNodeMixShader").inputs[0].default_value = alpha * fade * shimmer


# ---------------- BG-HIGH-SKY ----------------
def high_sky_set(O, seed=8):
    """High air above the sea: the sea far below, wisps passing the lens, vapor curls rising to C,
    droplets that sparkle, drift together and clump, and a cloud that grows from the clump."""
    rnd = random.Random(seed)
    O = V(O)
    C = O + V((0, 8, 0))
    plane("sea_far", O + V((0, 300, -140)), (3000, 3000), (0, 0, math.radians(90)), painted("sea.png", 0.02))
    for k, (dx, dy, dz, s) in enumerate(((-40, 120, -60, 14), (55, 200, -70, 18), (-90, 260, -80, 20), (30, 90, -50, 9))):
        cloud("cloud_low", O + V((dx, dy, dz)), s, seed=30 + k, puffs=9)
    wisps = []
    for k in range(7):
        side = rnd.choice((-1, 1))
        b = blob("wisp", O + V((side * rnd.uniform(2.6, 4.0), rnd.uniform(2.0, 7.0), rnd.uniform(-1.5, 1.0))), rnd.uniform(0.3, 0.45),
                 glassy("#FFFFFF", 0.22 + 0.0001 * k), scale=(2.4, 1, 0.6), sub=3)
        wisps.append((b, b.location.copy(), rnd.uniform(0.01, 0.025) * rnd.choice((-1, 1))))
    curls = vapor_curls(C + V((0, 0, -3.2)), 18, (-2.2, 2.2), (-1.4, 1.4), height=1.4, seed=9, key=0.31)
    drops = []
    for k in range(150):
        a, r = rnd.uniform(0, 6.28), rnd.uniform(0.3, 2.4)
        start = C + V((math.cos(a) * r, rnd.uniform(-1.3, 1.3), rnd.uniform(-1.6, 0.4)))
        a2, r2 = rnd.uniform(0, 6.28), rnd.uniform(0, 0.7) ** 0.7
        end = C + V((math.cos(a2) * r2 * 1.2, math.sin(a2) * r2 * 0.6, rnd.uniform(-0.25, 0.35)))
        d = blob("droplet", start, rnd.uniform(0.018, 0.032), emit("#EAF6FF", 1.7), sub=1)
        d.hide_render = True
        drops.append((d, start, end, rnd.uniform(0, 1)))
    puffs = cloud("cloud_form", C, 1.6, seed=12)
    for p in puffs:
        p["base_scale"] = tuple(p.scale)
        p.scale = (0, 0, 0)
        p.hide_render = True
    light("sun", "SUN", O + V((0, 0, 10)), 4.4, "#FFF6E8", rot=deg(28, 12, 0), angle=8)
    return dict(C=C, wisps=wisps, curls=curls, drops=drops, puffs=puffs)


# ---------------- BG-COAST-TOWN ----------------
KID_HOUSE = V((6.0, 26.0, 0.0))   # the kid's house in the town (front faces -Y, toward the sea)


def coast_town_set(O, seed=14):
    """Aerial coast: sea (y<0), beach, a small town of chunky houses with the kid's yellow house,
    hills behind. White clouds that drift in from the sea, wind streaks, and rain streaks."""
    rnd = random.Random(seed)
    O = V(O)
    plane("coast_sea", O + V((0, -400, -0.05)), (2000, 800), (0, 0, math.radians(90)), painted("sea.png", 0.05))
    box("beach", O + V((0, 3.0, -0.02)), (400, 6.0, 0.1), painted("sand.png", 0.3))
    box("land", O + V((0, 206, -0.05)), (400, 400, 0.1), painted("ep4_lawn.png", 0.15))
    for k in range(9):
        blob("hill", O + V((-120 + k * 32, 150 + rnd.uniform(-10, 10), -4)), rnd.uniform(18, 28), painted("hills.png", 0.08), scale=(1.6, 1, 0.55))
    walls = ["plaster_blue.png", "plaster_pink.png", "plaster_green.png", "plaster_cream.png"]
    roofs = ["roof_red.png", "roof_blue.png"]
    spots = [(-18, 16), (-11, 18), (-4, 15), (13, 17), (20, 15), (-15, 30), (-7, 33), (14, 31), (22, 29), (-2, 44), (9, 42), (18, 45)]
    for x, y in spots:
        c = O + V((x + rnd.uniform(-1, 1), y + rnd.uniform(-1, 1), 0))
        w, d, h = rnd.uniform(3.5, 4.8), rnd.uniform(3.5, 4.5), rnd.uniform(2.6, 3.6)
        box("house", c + V((0, 0, h / 2)), (w, d, h), painted(rnd.choice(walls), 0.5), 0.05)
        wedge("house_roof", c + V((0, 0, h)), d + 0.5, rnd.uniform(1.3, 1.8), w + 0.5, painted(rnd.choice(roofs), 0.6))
        for s in (-1, 1):
            box("house_win", c + V((s * w * 0.25, -d / 2 - 0.03, h * 0.55)), (0.7, 0.08, 0.75), painted("trim.png", 1.5), 0.02)
    # the kid's house: same colours as BG-WINDOW-RAINY (yellow siding, red roof, teal window, cream sill)
    kc = O + KID_HOUSE
    box("kid_house", kc + V((0, 0, 1.6)), (4.8, 4.0, 3.2), painted("ep4_siding_yellow.png", 0.9), 0.05)
    wedge("kid_roof", kc + V((0, 0, 3.2)), 4.6, 1.6, 5.4, painted("roof_red.png", 0.6))
    box("kid_frame", kc + V((0.4, -2.04, 1.55)), (1.6, 0.1, 1.5), painted("ep4_trim_teal.png", 2.0), 0.02)
    box("kid_glass", kc + V((0.4, -2.08, 1.55)), (1.3, 0.06, 1.25), painted("plaster_blue.png", 2.0))
    box("kid_mullion_v", kc + V((0.4, -2.13, 1.55)), (0.07, 0.04, 1.25), painted("ep4_trim_teal.png", 2.0))
    box("kid_mullion_h", kc + V((0.4, -2.13, 1.72)), (1.3, 0.04, 0.07), painted("ep4_trim_teal.png", 2.0))
    box("kid_sill", kc + V((0.4, -2.2, 0.76)), (1.9, 0.36, 0.08), painted("ep4_trim_cream.png", 2.0), 0.02)
    box("kid_planter", kc + V((0.4, -2.3, 0.55)), (1.7, 0.34, 0.32), painted("ep4_planter.png", 1.5), 0.03)
    for k in range(18):
        x, y = rnd.uniform(-30, 30), rnd.uniform(9, 55)
        if any(abs(x - sx) < 3.5 and abs(y - sy) < 3.5 for sx, sy in spots + [tuple(KID_HOUSE[:2])]):
            continue
        cyl("tree_trunk", O + V((x, y, 0.7)), 0.18, 1.4, painted("bark.png", 2.0))
        blob("tree", O + V((x, y, 2.0)), rnd.uniform(0.9, 1.4), painted("leaf.png", 1.2), scale=(1, 1, 1.1))
    clouds = []
    for k, (dx, dz, s) in enumerate(((-6, 20, 4.0), (5, 22, 5.0), (14, 19, 3.6))):
        base = O + V((dx, -46 + k * 6, dz))
        clouds.append((cloud("cloud_coast", base, s, seed=40 + k), base))
    wind = []
    for k in range(40):
        p = O + V((rnd.uniform(-14, 22), rnd.uniform(-60, 40), rnd.uniform(14, 26)))
        wind.append((plane("wind", p, (0.05, rnd.uniform(2.5, 5.0)), deg(0, 90, 0), glassy("#FFFFFF", 0.35)), p.copy()))
    rain = []
    for k in range(420):
        p = O + V((rnd.uniform(-16, 26), rnd.uniform(6, 50), rnd.uniform(0, 18)))
        r = plane("coast_rain", p, (0.03, rnd.uniform(0.8, 1.6)), deg(90, 0, 0), glassy("#E3EBF3", 0.3))
        r.hide_render = True
        rain.append((r, p.copy()))
    drop = hero_drop("coast_drop", O + V((4, 12, 18)), 0.26, alpha_key=0.4)
    for o in drop:
        o.visible_shadow = False   # no dark blot on the window as it arrives
    light("sun", "SUN", O + V((0, 0, 10)), 4.2, "#FFF4E2", rot=deg(40, -25, 0), angle=8)
    return dict(clouds=clouds, wind=wind, rain=rain, drop=drop)


# ---------------- BG-SHORE (serves BG-SHORE-DRAINING and BG-SEABED-EMPTY) ----------------
def shore_height(x, y):
    """Beach (y<6) falling into a seabed bowl that keeps sloping away from the shore (+Y)."""
    if y < 6:
        z = 0.25 - 0.06 * y
    else:
        d = y - 6
        z = -0.11 - 0.22 * d * (1 - min(d, 120) / 300) - 0.0
        z += 0.35 * math.sin(x * 0.27 + 1.3) * math.sin(y * 0.19) * min(1, d / 8)
    return z + 0.004 * x * x


def shore_set(O, seed=21):
    rnd = random.Random(seed)
    O = V(O)
    import bmesh as _bm
    bm = _bm.new()
    xs = [-70 + 2 * i for i in range(71)]
    ys = [-12 + 2 * j for j in range(161)]
    vv = [[bm.verts.new((x, y, shore_height(x, y))) for x in xs] for y in ys]
    dry, wet, bed = painted("sand.png", 0.35), painted("ep4_wet_sand.png", 0.35), painted("ep4_seabed_dry.png", 0.25)
    me = bpy.data.meshes.new("shore"); o = bpy.data.objects.new("shore", me)
    bpy.context.collection.objects.link(o)
    for m in (dry, wet, bed):
        me.materials.append(m)
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            f = bm.faces.new((vv[j][i], vv[j][i + 1], vv[j + 1][i + 1], vv[j + 1][i]))
            yc = ys[j] + 1
            f.material_index = 0 if yc < 4 else (1 if yc < 9 else 2)
            f.smooth = True
    bm.to_mesh(me); bm.free()
    o.location = O
    z = lambda x, y: shore_height(x, y)
    # jetty posts out into the bay, a rowboat, rocks, shells and seaweed on the seabed
    for k in range(9):
        y = 2 + k * 2.6
        for s in (-1, 1):
            cyl("jetty_post", O + V((-7 + s * 0.8, y, z(-7, y) + 0.9)), 0.13, 2.2 + 0.1 * k, painted("bark.png", 2.0), verts=12)
    boat = O + V((5.5, 19, z(5.5, 19) + 0.25))
    hull = cyl("rowboat", boat, 0.75, 3.2, painted("ep4_boat.png", 1.2), rot=deg(0, 90, 20), verts=24)
    hull.scale = (1, 1, 0.6)
    box("rowboat_seat", boat + V((0, 0, 0.2)), (0.25, 1.2, 0.08), painted("ep4_boat.png", 1.5), rot=deg(0, 0, 20))
    for k in range(26):
        x, y = rnd.uniform(-20, 20), rnd.uniform(9, 60)
        blob("rock", O + V((x, y, z(x, y) + 0.1)), rnd.uniform(0.3, 1.0), painted("rock.png", 1.0), scale=(1.3, 1, 0.6))
    for k in range(40):
        x, y = rnd.uniform(-12, 12), rnd.uniform(7, 40)
        blob("shell", O + V((x, y, z(x, y) + 0.04)), rnd.uniform(0.06, 0.12), painted(rnd.choice(["ep4_flower_pink.png", "ep4_flower_white.png"]), 3.0), scale=(1.2, 1, 0.5), sub=1)
    for k in range(30):
        x, y = rnd.uniform(-14, 14), rnd.uniform(8, 45)
        p0 = V((x, y, z(x, y) + 0.02))
        strip("seaweed", [O + p0 + V((0.25 * t * math.sin(t * 3 + k), 0.6 * t, 0.05)) for t in (i / 6 for i in range(7))],
              [0.12 * (1 - 0.6 * t) for t in (i / 6 for i in range(7))], painted("ep4_seaweed.png", 1.0, "UV"))
    # foreground: dune grass, a short fence and a bucket
    for k in range(22):
        x = rnd.uniform(-5, 5)
        p0 = O + V((x, rnd.uniform(-5.5, -3.5), z(x, -4.5)))
        strip("dune_grass", [p0 + V((0.08 * t * t, 0, 0.7 * t)) for t in (i / 5 for i in range(6))],
              [0.07 * (1 - t) + 0.01 for t in (i / 5 for i in range(6))], painted("leaf.png", 1.0, "UV"), up=(0, 1, 0))
    for k in range(6):
        x = -4.2 + k * 0.7
        box("fence_post", O + V((x, -2.6, z(x, -2.6) + 0.35)), (0.09, 0.09, 0.75), painted("trim.png", 1.5), 0.02)
    box("fence_rail", O + V((-2.45, -2.6, z(-2, -2.6) + 0.55)), (3.6, 0.05, 0.07), painted("trim.png", 1.5))
    cyl("bucket", O + V((2.2, -1.2, z(2.2, -1.2) + 0.15)), 0.17, 0.3, painted("toy_red.png", 2.0), r2=0.13, verts=20)
    # the sea: one big water plane that drains (drops and slides away)
    water = plane("sea_drain", O + V((0, 200, -0.3)), (400, 420), (0, 0, math.radians(90)), painted("sea.png", 0.3))
    foam = plane("sea_foam", O + V((0, 9.6, -0.27)), (140, 0.25), (0, 0, 0), glassy("#FFFFFF", 0.35))
    sun = card("dawn_sun", "sun_disc.png", 22, O + V((25, 260, -14)), shadow=False)[0]
    sun.data.materials[0] = pc.flatcard("sun_disc.png", 1.8)
    kid, kid_sh = card("kid_shock", "RAINKID-SHOCK-RAIN.png", 1.35, O + V((0.0, 2.6, z(0, 2.6))))
    kid_back, back_sh = card("kid_shore", "RAINKID-SHORE-RAIN.png", 1.3, O + V((0.4, 5.2, z(0.4, 5.2))))
    kid_back.hide_render = back_sh.hide_render = True
    sunl = light("sun", "SUN", O + V((0, 0, 10)), 3.0, "#FFE0C8", rot=deg(65, 0, 160), angle=8)
    # S06 boat: a proper open hull (a stretched half-sphere shell), tipped on its side; hidden until S06
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0, location=(0, 0, 0))
    hb = bpy.context.active_object; hb.name = "boat_hull_side"
    import bmesh as _bm2
    bmh = _bm2.new(); bmh.from_mesh(hb.data)
    _bm2.ops.delete(bmh, geom=[v for v in bmh.verts if v.co.z > 0.02], context="VERTS")
    for v in bmh.verts:                    # shape the bowl into a rowboat: pointed bow (+x), blunt stern, flatter bottom, sheer
        x, y, zz = v.co
        y *= 1 - 0.8 * max(0.0, x) ** 1.6
        x = max(x, -0.85)
        zz = max(zz, -0.75) + 0.14 * x * x * (1 + min(zz, 0.0))
        v.co = (x, y, zz)
    bmh.to_mesh(hb.data); bmh.free()
    hb.data.materials.append(painted("ep4_boat.png", 1.2))
    sol = hb.modifiers.new("shell", "SOLIDIFY"); sol.thickness = 0.06
    # rolled about its LONG axis (x) so it lies along the sand, opening tipped toward the S06 camera
    # (which looks in from -x,-y), then rested ON the sand: its lowest point just touches the ground
    hb.scale = (1.7, 0.7, 0.55)
    BROT = deg(35, 0, -30)
    hb.rotation_euler = BROT
    bx, by = 4.2, 19.3
    hb.location = O + V((bx, by, z(bx, by) + 2.0))
    bpy.context.view_layer.update()
    sink = min((hb.matrix_world @ v.co).z - (O.z + z((hb.matrix_world @ v.co).x - O.x, (hb.matrix_world @ v.co).y - O.y))
               for v in hb.data.vertices)
    hb.location.z -= sink + 0.12          # settle the keel ~12 cm in (ground mesh is coarser than z()) so it sits, not floats
    bpy.context.view_layer.update()
    side = [hb]
    for lx in (-0.55, 0.35):               # two thwarts (seats) across the open hull
        c = hb.matrix_world @ V((lx / 1.7, 0, -0.10 / 0.55))
        side.append(box("boat_seat_side", c, (0.32, 1.22, 0.06), painted("ep4_boat.png", 1.5), rot=BROT))
    for o in side:
        o.hide_render = True
    return dict(water=water, water_base=water.location.copy(), foam=foam, sun_card=sun, sun_base=sun.location.copy(),
                boat_side=side,
                kid=(kid, kid_sh), kid_back=(kid_back, back_sh), sun=sunl, z=z)


# ---------------- BG-INLAND (S07 green; S08 drying) ----------------
LAKE_C, LAKE_R = V((-9.0, 14.0)), (8.0, 5.0)     # lake centre and bowl radii (x, y), set-local
FIELD = (2.0, 19.0, 7.0, 26.0)                   # ploughed field: x0, x1, y0, y1


def inland_height(x, y):
    """Flat farmland with a shallow lake bowl, gentle rolls and a low hill behind (+Y)."""
    z = 0.12 * math.sin(x * 0.21 + 0.4) * math.sin(y * 0.17 + 1.1)
    e = ((x - LAKE_C.x) / LAKE_R[0]) ** 2 + ((y - LAKE_C.y) / LAKE_R[1]) ** 2
    if e < 1:
        z -= 0.75 * (1 - e) ** 1.5
    z += 6.0 * math.exp(-((y - 72) / 14) ** 2) * (0.7 + 0.3 * math.sin(x * 0.08))
    return z


def inland_set(O, seed=31):
    rnd = random.Random(seed)
    O = V(O)
    import bmesh as _bm
    bm = _bm.new()
    xs = [-50 + i for i in range(101)]
    ys = [-12 + j for j in range(101)]
    vv = [[bm.verts.new((x, y, inland_height(x, y))) for x in xs] for y in ys]
    lawn, soil, mud = painted("ep4_lawn.png", 0.25), painted("ep4_soil.png", 0.5), painted("ep4_wet_sand.png", 0.4)
    me = bpy.data.meshes.new("inland"); o = bpy.data.objects.new("inland", me)
    bpy.context.collection.objects.link(o)
    for m in (lawn, soil, mud):
        me.materials.append(m)
    x0, x1, y0, y1 = FIELD
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            f = bm.faces.new((vv[j][i], vv[j][i + 1], vv[j + 1][i + 1], vv[j + 1][i]))
            xc, yc = xs[i] + 0.5, ys[j] + 0.5
            e = ((xc - LAKE_C.x) / LAKE_R[0]) ** 2 + ((yc - LAKE_C.y) / LAKE_R[1]) ** 2
            f.material_index = 2 if e < 1.12 else (1 if x0 - 0.5 < xc < x1 + 0.5 and y0 - 0.5 < yc < y1 + 0.5 else 0)
            f.smooth = True
    bm.to_mesh(me); bm.free()
    o.location = O
    z = lambda x, y: inland_height(x, y)
    # the lake: a flat water disc filling the bowl (S08 shrinks and lowers it to show a dry rim)
    lake = cyl("lake", O + V((LAKE_C.x, LAKE_C.y, -0.06)), 1.0, 0.02, painted("sea.png", 0.6), verts=64)
    lake.scale = (LAKE_R[0] * 0.98, LAKE_R[1] * 0.98, 1)
    glints = [blob("lake_glint", O + V((LAKE_C.x + rnd.uniform(-5, 5), LAKE_C.y + rnd.uniform(-2.5, 2.5), -0.03)), 0.04,
                   emit("#FFFBEA", 2.0), scale=(3, 0.6, 0.3), sub=1) for _ in range(18)]
    # reeds along the near lake edge (foreground strip for the lake view)
    reeds = []
    for k in range(46):
        a = rnd.uniform(math.pi * 1.1, math.pi * 1.9)
        x = LAKE_C.x + math.cos(a) * LAKE_R[0] * rnd.uniform(0.86, 1.0)
        y = LAKE_C.y + math.sin(a) * LAKE_R[1] * rnd.uniform(0.86, 1.0)
        p0 = O + V((x, y, z(x, y) - 0.05)); h = rnd.uniform(0.6, 1.1); lean = rnd.uniform(-0.15, 0.15)
        reeds.append(strip("reed", [p0 + V((lean * t * t, 0, h * t)) for t in (i / 5 for i in range(6))],
                           [0.06 * (1 - t) + 0.012 for t in (i / 5 for i in range(6))], painted("ep4_seaweed.png", 1.0, "UV"), up=(0, 1, 0)))
    # ploughed field: soil ridges running away from the camera, a row of young plants on each
    ridges, plants = [], []
    nx = 11
    for r in range(nx):
        x = x0 + 0.6 + r * (x1 - x0 - 1.2) / (nx - 1)
        yc = (y0 + y1) / 2
        ridges.append(blob("ridge", O + V((x, yc, z(x, yc) + 0.02)), 1.0, painted("ep4_soil.png", 0.8), scale=(0.42, (y1 - y0) / 2 - 0.4, 0.2), sub=3))
        for k in range(10):
            y = y0 + 1.0 + k * (y1 - y0 - 2.0) / 9 + rnd.uniform(-0.2, 0.2)
            c = O + V((x + rnd.uniform(-0.05, 0.05), y, z(x, y) + 0.24))
            stem = cyl("plant_stem", c, 0.025, 0.24, painted("leaf.png", 2.0), verts=8)
            leaf = blob("plant", c + V((0, 0, 0.16)), rnd.uniform(0.17, 0.24), painted("leaf.png", 1.6), scale=(1.2, 1.2, 0.8), sub=2)
            plants.append((stem, leaf, leaf.location.copy()))
    # one puffy tree behind the field, a fence post and soil clods in front
    tc = O + V((14.5, 30.5, z(14.5, 30.5)))
    trunk = cyl("tree_trunk", tc + V((0, 0, 1.5)), 0.28, 3.0, painted("bark.png", 2.0), r2=0.2)
    crown = []
    for dx, dy, dz, r in ((0, 0, 3.6, 1.9), (-1.2, 0.3, 3.1, 1.4), (1.25, -0.2, 3.2, 1.5), (0.2, 0.4, 4.6, 1.3), (0.3, -0.6, 2.7, 1.2)):
        crown.append(blob("tree", tc + V((dx, dy, dz)), r, painted("leaf.png", 1.2), scale=(1, 1, 0.92), sub=3))
    box("fence_post", O + V((1.5, 6.5, z(1.5, 6.5) + 0.45)), (0.12, 0.12, 0.95), painted("trim.png", 1.5), 0.02)   # field corner
    for k in range(14):
        x, y = rnd.uniform(1.0, 9.0), rnd.uniform(3.0, 6.5)
        blob("clod", O + V((x, y, z(x, y) + 0.03)), rnd.uniform(0.08, 0.18), painted("ep4_soil.png", 1.5), scale=(1.3, 1, 0.6), sub=1)
    for k in range(5):
        blob("hill", O + V((-60 + k * 30, 95 + rnd.uniform(-8, 8), -3)), rnd.uniform(16, 24), painted("hills.png", 0.08), scale=(1.6, 1, 0.5))
    # vapor curls: off the lake, off the soil rows, off the plants (FX-VAPOR-CURLS, faint and few)
    c_lake = vapor_curls(O + V((LAKE_C.x, LAKE_C.y, -0.06)), 12, (-5.0, 5.0), (-2.4, 2.4), height=1.3, seed=32, key=0.33)
    c_soil = vapor_curls(O + V(((x0 + x1) / 2, (y0 + y1) / 2 - 3, 0.1)), 10, (-7.0, 7.0), (-7.0, 6.0), height=1.1, seed=33, key=0.35)
    picks = rnd.sample(range(len(plants)), 10)
    c_plant = []
    for k, i in enumerate(picks):
        cv = vapor_curls(plants[i][2] + V((0, 0, 0.1)), 1, (0, 0), (0, 0), z0=0.0, height=0.9, seed=40 + k, key=0.36 + 0.001 * k)
        c_plant += cv
    # PROP-CLOUD: a small patchy cloud that forms over the field, and two thin neighbours (they thin out in V4)
    def grow(puffs):
        for p in puffs:
            p["base_scale"] = tuple(p.scale); p.scale = (0, 0, 0); p.hide_render = True
        return puffs
    cl_main = grow(cloud("cloud_patchy", O + V((7.0, 36.0, 15.0)), 3.2, seed=51, puffs=11))
    cl_side = [cloud("cloud_thin", O + V((-9.0, 44.0, 17.0)), 2.6, seed=52, puffs=8),
               cloud("cloud_thin", O + V((20.0, 48.0, 18.5)), 2.4, seed=53, puffs=8),
               cloud("cloud_thin", O + V((-24.0, 40.0, 13.0)), 2.2, seed=54, puffs=7)]
    for cs in cl_side:
        for p in cs:
            p["base_scale"] = tuple(p.scale)
    kid, kid_sh = card("kid_point", "RAINKID-POINTUP-RAIN.png", 1.35, O + V((3.4, 4.6, z(3.4, 4.6))))
    light("sun", "SUN", O + V((0, 0, 10)), 4.2, "#FFF4E2", rot=deg(42, -20, 15), angle=8)
    # soft fill shining UP (and away from the camera): it only reaches downward-facing surfaces, so cloud
    # undersides seen from the ground lift out of the violet shadow band; the ground (facing up) gets none
    fill = light("fill_under", "SUN", O + V((0, 0, 10)), 2.4, "#FFF8F0", rot=deg(150, 0, 0), angle=10)
    fill.data.use_shadow = False      # otherwise the ground itself blocks a light from below

    # ---- S08 drying state: built here, hidden or neutral until S08 (S07 looks exactly as approved) ----
    r8 = random.Random(seed + 100)    # own stream, so nothing above changes
    dry_mix = []

    def dryable(mat, dry_tex):
        """Copy a painted material and mix a dry texture over it (factor 0 = unchanged)."""
        m = mat.copy(); nt = m.node_tree
        it = next(nd for nd in nt.nodes if nd.bl_idname == "ShaderNodeTexImage")
        it2 = nt.nodes.new("ShaderNodeTexImage"); it2.image = pc.image(dry_tex)
        it2.projection, it2.projection_blend = it.projection, it.projection_blend
        nt.links.new(it.inputs[0].links[0].from_socket, it2.inputs[0])
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type, mx.blend_type = "RGBA", "MIX"
        sock = lambda ident: next(sk for sk in mx.inputs if sk.identifier == ident)
        outs = [lk.to_socket for lk in it.outputs["Color"].links]
        for lk in list(it.outputs["Color"].links):
            nt.links.remove(lk)
        nt.links.new(it.outputs["Color"], sock("A_Color")); nt.links.new(it2.outputs["Color"], sock("B_Color"))
        res = next(sk for sk in mx.outputs if sk.identifier == "Result_Color")
        for to in outs:
            nt.links.new(res, to)
        f_in = sock("Factor_Float"); f_in.default_value = 0.0
        dry_mix.append(f_in)
        return m, f_in

    soil_m, soil_f = dryable(me.materials[1], "ep4_soil_dry.png"); me.materials[1] = soil_m
    mud_m, mud_f = dryable(me.materials[2], "ep4_seabed_dry.png"); me.materials[2] = mud_m
    ridge_m, ridge_f = dryable(ridges[0].data.materials[0], "ep4_soil_dry.png")
    for rg in ridges:
        rg.data.materials[0] = ridge_m
        rg["base_sz"] = rg.scale.z
    clods = [ob for ob in bpy.context.collection.objects if ob.name.startswith("clod")]
    if clods:
        clod_m, clod_f = dryable(clods[0].data.materials[0], "ep4_soil_dry.png")
        for ob in clods:
            ob.data.materials[0] = clod_m
    else:
        clod_f = None
    leaf_m, leaf_f = dryable(plants[0][1].data.materials[0], "ep4_leaf_dry.png")
    stem_m, stem_f = dryable(plants[0][0].data.materials[0], "ep4_leaf_dry.png")
    droop = []
    for stem, leaf, lbase in plants:
        stem.data.materials[0] = stem_m; leaf.data.materials[0] = leaf_m
        base = stem.location.copy() - V((0, 0, 0.12))
        a = r8.uniform(0, 2 * math.pi)
        droop.append((stem, leaf, base, V((math.cos(a), math.sin(a), 0)), r8.uniform(0.7, 1.0), tuple(leaf.scale)))
    crown_m, crown_f = dryable(crown[0].data.materials[0], "ep4_leaf_dry.png")
    for cb in crown:
        cb.data.materials[0] = crown_m
        cb["base_scale"] = tuple(cb.scale)
    # cloud puffs remember where they started (S08 drifts them toward the camera)
    for p in cl_main + [q for cs in cl_side for q in cs]:
        p["base_loc"] = tuple(p.location)
    # FX-RAIN sprinkle: a few streaks falling from the thinned cloud (sparse)
    sprinkle = []
    for k in range(28):
        p0 = O + V((r8.uniform(4.5, 9.5), r8.uniform(31.0, 37.0), 13.2))
        st = plane("sprinkle", p0, (0.045, r8.uniform(1.0, 1.5)), deg(90, 0, 0), glassy("#EEF3F8", 0.55))
        st.hide_render = True
        sprinkle.append((st, p0.copy(), r8.uniform(0, 1)))
    # FX-CRACKS: dark crack lines that grow across the field (and the lake's dry rim), segment by segment
    nx_r = 11
    ridge_x = [x0 + 0.6 + r * (x1 - x0 - 1.2) / (nx_r - 1) for r in range(nx_r)]
    ridge_hy = (y1 - y0) / 2 - 0.4
    yc_f = (y0 + y1) / 2
    RIDGE_H_DRY = 0.07

    def surf(x, y):
        """Ground or flattened-ridge top, whichever is higher, plus a hair (cracks lie on it)."""
        g = z(x, y)
        for rx in ridge_x:
            q = 1 - ((x - rx) / 0.42) ** 2 - ((y - yc_f) / ridge_hy) ** 2
            if q > 0:
                g = max(g, z(rx, yc_f) + 0.02 + RIDGE_H_DRY * math.sqrt(q))
        return g + 0.025

    crack_mat = emit("#3B2717", 1.0)
    cracks = []

    def crack(x, y, ang, nseg, t0, inside, w0=0.11):
        segs = []
        for i in range(nseg):
            L = r8.uniform(0.28, 0.42)
            ang += r8.uniform(-0.7, 0.7)
            nx2, ny2 = x + math.cos(ang) * L, y + math.sin(ang) * L
            if not inside(nx2, ny2):
                break
            w = w0 * (1 - 0.6 * i / max(1, nseg - 1))
            sg = strip("crack", [O + V((x, y, surf(x, y))), O + V((nx2, ny2, surf(nx2, ny2)))], [w, w * 0.85], crack_mat)
            sg.hide_render = True
            segs.append(sg)
            if r8.random() < 0.18 and i > 1:      # a side branch
                cracks.append((crack_branch(nx2, ny2, ang + r8.choice((-1, 1)) * r8.uniform(0.9, 1.5), t0 + i * 2), t0 + i * 2))
            x, y = nx2, ny2
        return segs

    def crack_branch(x, y, ang, t0):
        return crack(x, y, ang, r8.randint(2, 4), t0, in_field, w0=0.07)

    in_field = lambda x, y: x0 + 0.2 < x < x1 - 0.2 and y0 + 0.2 < y < y1 - 0.2
    for k in range(50):
        cx, cy = r8.uniform(x0 + 0.5, x1 - 0.5), r8.uniform(y0 + 0.5, y1 - 0.5)
        t0 = 916 + 34 * (cy - y0) / (y1 - y0) + r8.uniform(-4, 4)   # spreads from the near edge to the far edge
        cracks.append((crack(cx, cy, r8.uniform(0, 2 * math.pi), r8.randint(5, 9), t0, in_field), t0))

    def in_rim(x, y):
        e = ((x - LAKE_C.x) / LAKE_R[0]) ** 2 + ((y - LAKE_C.y) / LAKE_R[1]) ** 2
        return 0.5 < e < 1.0
    for k in range(14):
        a = r8.uniform(0, 2 * math.pi); rr = r8.uniform(0.78, 0.92)
        cx, cy = LAKE_C.x + math.cos(a) * LAKE_R[0] * rr, LAKE_C.y + math.sin(a) * LAKE_R[1] * rr
        cracks.append((crack(cx, cy, a + r8.uniform(-0.6, 0.6), r8.randint(3, 6), 950 + r8.uniform(0, 14), in_rim, w0=0.06), 950))
    # one faint curl that tries to rise from the cracked ground and fizzles out (S08 V3)
    fizzle = vapor_curls(O + V((9.9, 15.0, surf(9.9, 15.0) - 0.02)), 1, (0, 0), (0, 0), z0=0.0, height=0.9, seed=60, key=0.37)

    return dict(lake=lake, lake_base=(lake.location.copy(), tuple(lake.scale)), glints=glints, reeds=reeds, ridges=ridges,
                plants=plants, trunk=trunk, crown=crown, c_lake=c_lake, c_soil=c_soil, c_plant=c_plant,
                cl_main=cl_main, cl_side=cl_side, kid=(kid, kid_sh), z=z,
                glint_base=[g.location.copy() for g in glints],
                dry=dict(soil=soil_f, mud=mud_f, ridge=ridge_f, clod=clod_f, leaf=leaf_f, stem=stem_f, crown=crown_f),
                droop=droop, sprinkle=sprinkle, cracks=cracks, fizzle=fizzle)


# ---------------- BG-DRY-PLAIN (S09 day; S10 V4 and S11 add glare and night later) ----------------
SUN_DIR = V((0.28, 0.75, 0.60)).normalized()     # S09 sun: ~37 deg up, a little right of straight ahead (+Y)
KID_PLAIN = (0.0, 6.0)


def plain_height(x, y):
    """A flat baked plain with very slight swells (cracks lie on it, so it stays gentle)."""
    return 0.07 * math.sin(x * 0.23 + 0.7) * math.sin(y * 0.19 + 0.3) + 0.04 * math.sin(x * 0.61 + y * 0.43)


def billboard(name, mat, size, c):
    """A centred square quad (normal local -Y) with UVs; the caller turns it to the camera."""
    import bmesh as _bm
    bm = _bm.new(); uv = bm.loops.layers.uv.new("UVMap"); h = size / 2
    f = bm.faces.new([bm.verts.new(v) for v in ((-h, 0, -h), (h, 0, -h), (h, 0, h), (-h, 0, h))])
    for lp, t in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uv].uv = t
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    o.location = c
    return o


def flare_mat(color, strength):
    """FX-SUN-FLARE ghost: the soft glow texture added on top of the picture (additive, not inked).
    Returns (material, emission node) so the strength can fade per frame."""
    m = bpy.data.materials.new("flare_" + color); m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links; n.clear()
    it = n.new("ShaderNodeTexImage"); it.image = pc.image("glow.png")
    mul = n.new("ShaderNodeMix"); mul.data_type, mul.blend_type = "RGBA", "MULTIPLY"; mul.inputs["Factor"].default_value = 1
    mul.inputs["B"].default_value = pc.hexcol(color)
    l.new(it.outputs["Color"], mul.inputs["A"])
    am = n.new("ShaderNodeMix"); am.data_type, am.blend_type = "RGBA", "MULTIPLY"; am.inputs["Factor"].default_value = 1
    l.new(mul.outputs["Result"], am.inputs["A"]); l.new(it.outputs["Alpha"], am.inputs["B"])
    em = n.new("ShaderNodeEmission"); em.inputs[1].default_value = strength
    l.new(am.outputs["Result"], em.inputs[0])
    add = n.new("ShaderNodeAddShader"); tr = n.new("ShaderNodeBsdfTransparent")
    l.new(tr.outputs[0], add.inputs[0]); l.new(em.outputs[0], add.inputs[1])
    l.new(add.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    m.surface_render_method = "BLENDED"
    return m, em


def dry_plain_set(O, seed=41):
    rnd = random.Random(seed)
    O = V(O)
    z = lambda x, y: plain_height(x, y)
    import bmesh as _bm
    bm = _bm.new()
    xs = [-160 + 2 * i for i in range(161)]
    ys = [-20 + 2 * j for j in range(121)]
    vv = [[bm.verts.new((x, y, z(x, y))) for x in xs] for y in ys]
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            bm.faces.new((vv[j][i], vv[j][i + 1], vv[j + 1][i + 1], vv[j + 1][i])).smooth = True
    me = bpy.data.meshes.new("plain"); o = bpy.data.objects.new("plain", me)
    bpy.context.collection.objects.link(o)
    me.materials.append(painted("ep4_plain_dry.png", 0.3))
    bm.to_mesh(me); bm.free()
    o.location = O
    # FX-CRACKS (settled): a network of dark crack lines baked into the ground, denser near the camera
    crack_mat = emit("#5C3D22", 1.0)
    cracks = []
    for k in range(170):
        x, y = rnd.uniform(-14, 16), 1.5 + 45 * rnd.random() ** 1.6
        if abs(x - KID_PLAIN[0]) < 0.5 and abs(y - KID_PLAIN[1]) < 0.4:
            continue
        ang = rnd.uniform(0, 2 * math.pi); pts = [(x, y)]
        for i in range(rnd.randint(5, 11)):
            ang += rnd.uniform(-0.6, 0.6); L = rnd.uniform(0.35, 0.7)
            x, y = x + math.cos(ang) * L, y + math.sin(ang) * L
            pts.append((x, y))
        w0 = rnd.uniform(0.06, 0.1) * (1 + 0.02 * pts[0][1])
        cracks.append(strip("crack_dry", [O + V((px, py, z(px, py) + 0.025)) for px, py in pts],
                            [w0 * (1 - 0.55 * i / (len(pts) - 1)) for i in range(len(pts))], crack_mat))
    # clods and small rocks, a round boulder
    for k in range(40):
        x, y = rnd.uniform(-9, 12), rnd.uniform(1.5, 26)
        if abs(x - KID_PLAIN[0]) < 0.7 and abs(y - KID_PLAIN[1]) < 0.6:
            continue
        r = rnd.uniform(0.06, 0.16)
        blob("clod" if k % 2 else "pebble", O + V((x, y, z(x, y) + r * 0.3)), r,
             painted("ep4_seabed_dry.png", 1.5) if k % 2 else painted("rock.png", 2.0), scale=(1.3, 1, 0.6), sub=1)
    blob("boulder", O + V((5.2, 14.5, z(5.2, 14.5) + 0.55)), 1.0, painted("rock.png", 0.6), scale=(1.25, 1.05, 0.8), sub=3)
    # a few dry shrubs: tight clusters of brown-olive puffs over twigs
    bark = painted("bark.png", 2.0)
    for k, (sx, sy) in enumerate(((-3.2, 9.5), (2.6, 11.0), (-6.0, 15.0), (8.5, 20.0), (-1.5, 24.0), (11.0, 9.0), (-9.5, 7.5))):
        g = z(sx, sy)
        for i in range(4):
            a = rnd.uniform(0, 2 * math.pi); h = rnd.uniform(0.3, 0.5)
            strip("shrub_twig", [O + V((sx, sy, g)), O + V((sx + 0.2 * math.cos(a), sy + 0.2 * math.sin(a), g + h))], [0.04, 0.015], bark, up=(0, 1, 0))
        for i in range(rnd.randint(5, 7)):
            blob("shrub", O + V((sx + rnd.uniform(-0.3, 0.3), sy + rnd.uniform(-0.25, 0.25), g + rnd.uniform(0.2, 0.42))),
                 rnd.uniform(0.13, 0.2), painted("ep4_leaf_dry.png", 1.6), scale=(1.2, 1.2, 0.85), sub=2)
    # one bare tree: a trunk and forked branches
    tx, ty = -6.5, 21.0
    tb = O + V((tx, ty, z(tx, ty)))
    cyl("bare_trunk", tb + V((0, 0, 1.1)), 0.2, 2.2, bark, r2=0.12, verts=12)

    def branch(p, ang, tilt, L, w, depth):
        d = V((math.cos(ang) * math.sin(tilt), 0.3 * math.sin(ang) * math.sin(tilt), math.cos(tilt)))
        q = p + d * L
        strip("bare_branch", [p, p.lerp(q, 0.5) + V((0, 0, 0.05 * L)), q], [w, w * 0.8, w * 0.55], bark, up=(0, 1, 0))
        if depth:
            for s in (-1, 1):
                branch(q, ang + s * rnd.uniform(0.3, 0.6), tilt + rnd.uniform(-0.15, 0.25), L * 0.62, w * 0.55, depth - 1)
    for ang, tilt in ((0.0, 0.5), (math.pi, 0.55), (0.3, 0.15), (math.pi - 0.4, 0.95)):
        branch(tb + V((0, 0, 2.05)), ang, tilt, 1.15, 0.13, 2)
    # low flat-topped hills on the horizon
    mesa = painted("ep4_mesa.png", 0.05)
    for k in range(9):
        x, y = -150 + k * 37 + rnd.uniform(-10, 10), rnd.uniform(140, 200)
        r, h = rnd.uniform(14, 26), rnd.uniform(7, 14)
        cyl("mesa", O + V((x, y, h / 2 - 1.5)), r, h, mesa, verts=14, r2=r * rnd.uniform(0.6, 0.75))
    # the kid, standing deadpan in sun clothes (POSE-RAINKID-STAND, OUTFIT-RAINKID-SUN)
    kid = card("kid_stand", "RAINKID-STAND-SUN.png", 1.35, O + V((KID_PLAIN[0], KID_PLAIN[1], z(*KID_PLAIN))))
    # the sun: light along SUN_DIR, a disc and a soft glare bloom far off in the same direction (they face the camera)
    sun = light("sun", "SUN", O + V((0, 0, 10)), 4.2, "#FFF4E2", rot=tuple(SUN_DIR.to_track_quat("Z", "Y").to_euler()), angle=8)
    fill = light("fill_under", "SUN", O + V((0, 0, 10)), 1.6, "#FFF8F0", rot=deg(150, 0, 0), angle=10)
    fill.data.use_shadow = False
    sun_disc = billboard("sun_disc", pc.flatcard("sun_disc.png", 1.0), 34, O + SUN_DIR * 400)
    glow_m = pc.flatcard("glow.png", 1.0).copy()
    glow = billboard("sun_glow", glow_m, 120, O + SUN_DIR * 430)
    # FX-SUN-FLARE ghosts (placed each frame on the line from the sun through the frame centre)
    ghosts = []
    for col, s, size, g in (("#FFE9B0", 0.35, 0.55, 0.55), ("#BFE6D8", 0.22, 0.25, 0.2), ("#F7C7A0", 0.25, 0.4, -0.25),
                            ("#C8D8FF", 0.2, 0.18, -0.6), ("#FFD9A8", 0.22, 0.7, -1.0)):
        m, em = flare_mat(col, s)
        ghosts.append((billboard("flare_ghost", m, size, O), em, s, g))
    # PROP-CLOUD: one thin cloud that slides across the sun (S09); it rides along the sun's ray from the camera
    veil_c = O + V((0.3, 2.5, 0.8)) + SUN_DIR * 70
    veil = cloud("cloud_veil", veil_c, 5.5, seed=71, puffs=9)
    vm = painted("ep4_cloud.png", 0.2, lift=1.12)
    for p in veil:
        p.data.materials[0] = vm
        p.scale = (p.scale[0] * 1.5, p.scale[1] * 0.6, p.scale[2] * 0.7)
        p["base_loc"] = tuple(p.location)
    # ---- S10 additions: built hidden (S09 looks exactly as approved); own random stream ----
    r10 = random.Random(seed + 200)
    # PROP-CLOUD-LAYER: a wide sheet of cloud clusters high over the plain (its shadow is the parasol)
    layer = []
    for i in range(9):
        for j in range(9):
            if r10.random() < 0.15:
                continue
            c = O + V((-36 + 9 * i + r10.uniform(-2.5, 2.5), -14 + 9 * j + r10.uniform(-2.5, 2.5), 24 + r10.uniform(-1, 1)))
            layer.append((c, cloud("cloud_layer", c, 3.6, seed=300 + 9 * i + j, puffs=5)))
    for c, puffs in layer:
        for p in puffs:
            p["base_scale"] = tuple(p.scale); p.hide_render = True
    # FX-SUNBEAMS: soft arrows of light (bounce off the layer's tops in V2; pour through gaps to the ground in V3-V4)
    beam_m = emit("#FFE69C", 1.0, alpha=0.82)
    tops = [c for c, _ in layer if -14 < c.x - O.x < 14 and 4 < c.y - O.y < 40]
    r10.shuffle(tops)
    bounce = []
    for k, c in enumerate(tops[:9]):
        nrm = V((r10.uniform(-0.25, 0.25), r10.uniform(-0.25, 0.25), 1)).normalized()
        bounce.append((arrow("beam_in", 7.0, 1.7, beam_m), arrow("beam_out", 7.0, 1.7, beam_m), c + V((0, 0, 2.0)), nrm,
                       1200 + 6.5 * k + r10.uniform(-2, 2)))
    spot_m = emit("#FFB25E", 1.0, alpha=0.42)
    pour = []
    for k in range(16):
        x, y = r10.uniform(-5, 6), r10.uniform(9, 26)
        hit = O + V((x, y, z(x, y) + 0.03))
        spot = cyl("warm_spot", hit, 1.0, 0.01, spot_m, verts=28)
        spot.hide_render = True
        pour.append((arrow("beam_down", 3.4, 0.6, beam_m), hit, spot, r10.uniform(0.7, 1.3), 1270 + 4.6 * k + r10.uniform(-2, 2)))
    # FX-HEAT-SHIMMER: wavy see-through ribbons wobbling just above the hot ground (not inked)
    shimmer = []
    for k in range(16):
        x, y = r10.uniform(-3.5, 4.0), r10.uniform(1.5, 16)
        if abs(x) < 0.6 and abs(y - KID_PLAIN[1]) < 0.8:
            continue
        h, A, ph = r10.uniform(0.5, 1.1), r10.uniform(0.03, 0.07), r10.uniform(0, 6.28)
        pts = [(A * math.sin(9 * u + ph), 0, u * h) for u in (i / 12 for i in range(13))]
        ws = [0.02 + 0.07 * math.sin(math.pi * u) for u in (i / 12 for i in range(13))]
        m = emit("#FFF4DA", 1.1, alpha=0.2 + 0.0001 * k)
        o = strip("heat_shimmer", pts, ws, m, up=(0, 1, 0))
        o.location = O + V((x, y, z(x, y)))
        o.hide_render = True
        shimmer.append((o, m, o.location.copy(), r10.uniform(0, 1)))
    for a_in, a_out, *_ in bounce:
        a_in.hide_render = a_out.hide_render = True
    for a_dn, *_ in pour:
        a_dn.hide_render = True
    # ---- S11 additions: built hidden (S09-S10 unchanged); own random stream ----
    r11 = random.Random(seed + 300)
    kp = O + V((KID_PLAIN[0], KID_PLAIN[1], z(*KID_PLAIN)))
    kids = {"stand": kid}
    for key, tex, px in (("shield", "RAINKID-SHIELD-SUN.png", 1753), ("fan", "RAINKID-FAN-SUN.png", 1753),
                         ("shiver", "RAINKID-SHIVER-NIGHT.png", 1852)):
        kids[key] = card("kid_" + key, tex, 1.35 * px / 1753, kp)     # same body size as the standing card
        for ob in kids[key]:
            ob.hide_render = True
    # FX-STARS-FROST: small frost glints on the cracks and a few twinkling stars low over the plain (not inked)
    frost_m = emit("#EAF6FF", 1.6)
    frost = []
    for k in range(80):
        cr = r11.choice(cracks)
        p = cr.data.vertices[r11.randrange(len(cr.data.vertices))].co
        g = blob("frost", V(p) + V((0, 0, 0.012)), r11.uniform(0.018, 0.03), frost_m, scale=(2.2, 0.8, 0.5), sub=1)
        g.hide_render = True
        frost.append((g, tuple(g.scale), r11.uniform(0, 1)))
    star_m = emit("#F4F6FF", 1.0)
    stars = []
    for k in range(50):
        a, el = math.radians(r11.uniform(-55, 55)), math.radians(r11.uniform(6, 48))
        c = O + V((math.sin(a) * math.cos(el), math.cos(a) * math.cos(el), math.sin(el))) * 900
        st = blob("star_twinkle", c, r11.uniform(1.2, 2.2), star_m, sub=1)
        st.hide_render = True
        stars.append((st, r11.uniform(0, 1)))
    return dict(z=z, kid=kid, kids=kids, cracks=cracks, sun=sun, sun_disc=sun_disc, glow=glow, glow_m=glow_m, ghosts=ghosts,
                veil=veil, veil_c=veil_c, layer=layer, bounce=bounce, pour=pour, shimmer=shimmer, frost=frost, stars=stars)


def arrow(name, L, W, mat):
    """FX-SUNBEAMS arrow: a flat shaft and head, tip at the origin pointing +X (not inked; turned to the camera per frame)."""
    import bmesh as _bm
    bm = _bm.new(); h = 0.32 * L; s = 0.22 * W
    head = [bm.verts.new(v) for v in ((0, 0, 0), (-h, W / 2, 0), (-h, -W / 2, 0))]
    bm.faces.new(head)
    bm.faces.new([bm.verts.new(v) for v in ((-h, -s, 0), (-h, s, 0), (-L, s, 0), (-L, -s, 0))])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    return o


# ---------------- BG-SPACE-EARTH (S10 V1) ----------------
EARTH_R = 30.0
SPACE_CAM_DIR = V((0.0, -1.0, 0.28)).normalized()   # where the V1 camera sits, seen from the Earth's centre
SPACE_LIGHT = V((0.55, -0.6, 0.6)).normalized()       # sunlight from the upper right, in front (most of the face lit)
SPACE_BEAM = V((0.72, -0.22, 0.66)).normalized()      # the arrows come in from the upper right of the frame (the sun's side)


def space_earth_set(O, seed=81):
    rnd = random.Random(seed)
    O = V(O)
    earth = pc.sphere("earth", O, EARTH_R, painted("earth_map.png", 1.0, "UV", lift=1.1))
    # turn the globe so Africa and Europe face the camera (earth_map u ~0.55, v ~0.35)
    from mathutils import Euler as _E
    me = earth.data
    uvl = me.uv_layers.active.data
    best = None
    for spin in range(0, 360, 5):
        R = _E((math.radians(23.4), 0, math.radians(spin))).to_matrix()
        for poly in list(me.polygons)[::7]:
            if (R @ poly.normal).dot(SPACE_CAM_DIR) > 0.995:
                u = sum(uvl[i].uv.x for i in poly.loop_indices) / poly.loop_total
                err = abs(u - 0.55)
                if best is None or err < best[0]:
                    best = (err, spin)
    earth.rotation_euler = deg(23.4, 0, best[1] if best else 0)
    # a thin blue atmosphere rim: an additive glow behind the globe (only its edge shows)
    halo_m, _ = flare_mat("#6FA8FF", 0.6)
    halo = billboard("atmosphere", halo_m, EARTH_R * 2.7, O - SPACE_CAM_DIR * 2)
    # the cloud shell: clusters of flattened puffs riding just above the surface, mostly on the side we see
    cl_m = painted("ep4_cloud.png", 0.2)
    clusters = []
    while len(clusters) < 58:
        n = V((rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1))).normalized()
        if n.dot(SPACE_CAM_DIR) < 0.2:
            continue
        t1 = n.cross(V((0, 0, 1))).normalized(); t2 = n.cross(t1)
        c = O + n * (EARTH_R + 0.9)
        rot = n.to_track_quat("Z", "Y").to_euler()
        for _ in range(5):
            off = t1 * rnd.uniform(-2.6, 2.6) + t2 * rnd.uniform(-1.8, 1.8) + n * rnd.uniform(0, 0.4)
            b = blob("cloud_shell", c + off, rnd.uniform(1.2, 2.0), cl_m, scale=(1.4, 1.1, 0.5), sub=2)
            b.rotation_euler = rot
        clusters.append((c, n))
    light("sun", "SUN", O + V((0, 0, 60)), 4.4, "#FFF4E2", rot=tuple(SPACE_LIGHT.to_track_quat("Z", "Y").to_euler()), angle=2)
    # the sun as a bright disc at the frame's upper-right edge (placed for the V1 camera; it is far away)
    cam0 = O + SPACE_CAM_DIR * 185
    sdir = (-SPACE_CAM_DIR + V((0.08, 0, 0)) + V((0, 0, 0.28))).normalized()
    sun_disc = billboard("sun_disc", pc.flatcard("sun_disc.png", 1.0), 90, cam0 + sdir * 1500)
    sun_glow = billboard("sun_glow", pc.flatcard("glow.png", 1.0), 300, cam0 + sdir * 1520)
    # FX-SUNBEAMS: arrows from the sun side that hit bright cloud tops and bounce back out to space
    beam_m = emit("#FFE69C", 1.0, alpha=0.85)
    lit = [(c, n) for c, n in clusters if n.dot(SPACE_BEAM) > 0.3 and n.dot(SPACE_CAM_DIR) > 0.55]
    rnd.shuffle(lit)
    bounce = []
    for k, (c, n) in enumerate(lit[:7]):
        bounce.append((arrow("beam_in", 11.0, 2.6, beam_m), arrow("beam_out", 11.0, 2.6, beam_m), c + n * 1.0, n,
                       1136 + 7.0 * k + rnd.uniform(-2, 2)))
    for a_in, a_out, *_ in bounce:
        a_in.hide_render = a_out.hide_render = True
    # faint dust specks drifting near the lens (not inked; placed relative to the camera each frame)
    dust = [(blob("dust", O, rnd.uniform(0.025, 0.05), glassy("#E4EAFF", 0.5), sub=1),
             V((rnd.uniform(-1.6, 1.6), rnd.uniform(5, 9), rnd.uniform(-2.6, 2.6))), rnd.uniform(0, 6.28)) for _ in range(10)]
    return dict(earth=earth, halo=halo, sun_disc=sun_disc, sun_glow=sun_glow, bounce=bounce, dust=dust)
