"""EP003 look test: the bedroom set (BG-BEDROOM-MORNING) in the papercraft look (set-specs v1).

Painted textures, soft high-ambient shading, no outlines on the set, flat kid card
with a soft contact shadow, one whole-scene grade per lighting state.

usage: blender -b -P renderer-blender/ep003_lookdev_bedroom.py -- OUT_DIR [scale%]
"""
import math, os, random, sys
import bpy, bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
TEX, CARDS = os.path.join(HERE, "textures"), os.path.join(HERE, "cards")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["/tmp/ep003_lookdev"]
OUT, SCALE = argv[0], int(argv[1]) if len(argv) > 1 else 100
random.seed(5)


def hexcol(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb], a)


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, SCALE
sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
sc.eevee.taa_render_samples = 48
world = bpy.data.worlds.new("World")
sc.world = world
world.use_nodes = True
bgn = world.node_tree.nodes["Background"]

# ---------- whole-scene grade (one RGB value multiplies every material) ----------
grade = bpy.data.node_groups.new("Grade", "ShaderNodeTree")
grade.interface.new_socket(name="Color", in_out="OUTPUT", socket_type="NodeSocketColor")
g_out, g_rgb = grade.nodes.new("NodeGroupOutput"), grade.nodes.new("ShaderNodeRGB")
grade.links.new(g_rgb.outputs[0], g_out.inputs[0])
_imgs = {}


def image(name):
    if name not in _imgs:
        _imgs[name] = bpy.data.images.load(os.path.join(CARDS if os.path.exists(os.path.join(CARDS, name)) else TEX, name))
    return _imgs[name]


LIFT = 0.88  # overall exposure of painted surfaces


def painted(tex, scale=1.0, coords="OBJ", lift=1.0):
    """Painted surface: texture x soft light ramp x gentle AO x grade, as emission (no hard terminator)."""
    m = bpy.data.materials.new(f"paint_{tex}_{scale}_{coords}")
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    tc, mp, it = n.new("ShaderNodeTexCoord"), n.new("ShaderNodeMapping"), n.new("ShaderNodeTexImage")
    it.image = image(tex)
    mp.inputs["Scale"].default_value = (scale, scale, scale)
    if coords == "OBJ":
        it.projection, it.projection_blend = "BOX", 0.25
        l.new(tc.outputs["Object"], mp.inputs[0])
    else:
        l.new(tc.outputs["UV"], mp.inputs[0])
    l.new(mp.outputs[0], it.inputs[0])
    dif, s2r, mul, ramp = n.new("ShaderNodeBsdfDiffuse"), n.new("ShaderNodeShaderToRGB"), n.new("ShaderNodeMath"), n.new("ShaderNodeValToRGB")
    l.new(dif.outputs[0], s2r.inputs[0])
    mul.operation, mul.inputs[1].default_value = "MULTIPLY", 0.55
    bw = n.new("ShaderNodeRGBToBW")
    l.new(s2r.outputs[0], bw.inputs[0]); l.new(bw.outputs[0], mul.inputs[0]); l.new(mul.outputs[0], ramp.inputs[0])
    ramp.color_ramp.interpolation = "EASE"
    e = ramp.color_ramp.elements
    lift *= LIFT
    e[0].position, e[0].color = 0.0, (0.66 * lift,) * 3 + (1,)
    e[1].position, e[1].color = 0.9, (1.06 * lift,) * 3 + (1,)
    e.new(0.45).color = (0.92 * lift,) * 3 + (1,)
    ao = n.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.6
    aomix = n.new("ShaderNodeMapRange")
    aomix.inputs[3].default_value, aomix.inputs[4].default_value = 0.8, 1.0
    l.new(ao.outputs["AO"], aomix.inputs[0])
    m1, m2, m3 = (n.new("ShaderNodeMix") for _ in range(3))
    for mx in (m1, m2, m3):
        mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"
        mx.inputs["Factor"].default_value = 1.0
    gr = n.new("ShaderNodeGroup"); gr.node_tree = grade
    l.new(it.outputs["Color"], m1.inputs["A"]); l.new(ramp.outputs[0], m1.inputs["B"])
    l.new(m1.outputs["Result"], m2.inputs["A"]); l.new(aomix.outputs[0], m2.inputs["B"])
    l.new(m2.outputs["Result"], m3.inputs["A"]); l.new(gr.outputs[0], m3.inputs["B"])
    em = n.new("ShaderNodeEmission")
    l.new(m3.outputs["Result"], em.inputs[0])
    l.new(em.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    return m


def flatcard(tex, strength=1.0):
    """Unlit image (painted backdrop or cutout card) x grade, with alpha."""
    m = bpy.data.materials.new("card_" + tex)
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    it = n.new("ShaderNodeTexImage"); it.image = image(tex)
    gr = n.new("ShaderNodeGroup"); gr.node_tree = grade
    mx = n.new("ShaderNodeMix"); mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"; mx.inputs["Factor"].default_value = 1
    l.new(it.outputs["Color"], mx.inputs["A"]); l.new(gr.outputs[0], mx.inputs["B"])
    em, tr, mix = n.new("ShaderNodeEmission"), n.new("ShaderNodeBsdfTransparent"), n.new("ShaderNodeMixShader")
    em.inputs[1].default_value = strength
    l.new(mx.outputs["Result"], em.inputs[0])
    l.new(it.outputs["Alpha"], mix.inputs[0]); l.new(tr.outputs[0], mix.inputs[1]); l.new(em.outputs[0], mix.inputs[2])
    l.new(mix.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    m.surface_render_method = "DITHERED"
    return m


def shadow_mat(strength=0.5):
    m = bpy.data.materials.new("contact_shadow")
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    tc, gd, rp = n.new("ShaderNodeTexCoord"), n.new("ShaderNodeTexGradient"), n.new("ShaderNodeValToRGB")
    gd.gradient_type = "SPHERICAL"
    l.new(tc.outputs["Object"], gd.inputs[0])
    rp.color_ramp.interpolation = "EASE"
    rp.color_ramp.elements[0].position = 0.5
    rp.color_ramp.elements[1].position, rp.color_ramp.elements[1].color = 0.9, (strength,) * 3 + (1,)
    sh, tr, mx = n.new("ShaderNodeEmission"), n.new("ShaderNodeBsdfTransparent"), n.new("ShaderNodeMixShader")
    sh.inputs[0].default_value = hexcol("#1B1430")
    l.new(gd.outputs[0], rp.inputs[0]); l.new(rp.outputs[0], mx.inputs[0])
    l.new(tr.outputs[0], mx.inputs[1]); l.new(sh.outputs[0], mx.inputs[2])
    l.new(mx.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    m.surface_render_method = "BLENDED"
    return m


def box(name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.active_object
    o.name = name
    o.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width, b.segments = bevel, 3
    return o


def plane(name, loc, size, rot, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    return o


def cyl(name, loc, r, depth, mat, rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat)
    return o


def sphere(name, loc, r, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=r, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    return o


# ---------- materials ----------
WALL, FLOOR, TRIM = painted("wallpaper.png", 0.7), painted("floor.png", 0.55), painted("trim.png", 1.2)
CEIL, CURTAIN, CUSHION = painted("ceiling.png", 0.5), painted("curtain.png", 1.0, "UV"), painted("cushion.png", 1.5)
BRASS, ROCK, GLOBE = painted("brass.png", 2.0), painted("rock.png", 6.0), painted("earth_map.png", 1.0, "UV", lift=1.05)
RUG, TOYR, TOYC = painted("rug.png", 1.0, "UV"), painted("toy_red.png", 3.0), painted("toy_cream.png", 3.0)

# ---------- room (x right, y into the room toward the window, z up) ----------
WX0, WX1, WZ0, WZ1, WY = 0.0, 1.6, 0.9, 2.4, 3.2
plane("floor", (0, 0.1, 0), (6.4, 6.4), (0, 0, 0), FLOOR)
plane("ceiling", (0, 0.1, 3.2), (6.4, 6.4), (math.pi, 0, 0), CEIL)
for nm, a in (("wall_L", (-3.2, WX0, WZ0 - 0.9, 3.2)), ("wall_R", (WX1, 3.2, 0, 3.2))):
    box(nm, a[0], a[1], WY, WY + 0.25, a[2], a[3], WALL)
box("wall_low", WX0, WX1, WY, WY + 0.25, 0, WZ0, WALL)
box("wall_top", WX0, WX1, WY, WY + 0.25, WZ1, 3.2, WALL)
box("wall_side", -2.7, -2.45, -3, WY, 0, 3.2, WALL)
box("baseboard_back", -2.45, 3.2, WY - 0.04, WY, 0, 0.16, TRIM, 0.01)
box("baseboard_side", -2.45, -2.41, -3, WY, 0, 0.16, TRIM, 0.01)
# chunky window frame and cross bars
F = 0.12
for nm, a in (("fr_L", (WX0 - F, WX0, WZ0 - F, WZ1 + F)), ("fr_R", (WX1, WX1 + F, WZ0 - F, WZ1 + F)),
              ("fr_B", (WX0 - F, WX1 + F, WZ0 - F, WZ0)), ("fr_T", (WX0 - F, WX1 + F, WZ1, WZ1 + F)),
              ("fr_V", ((WX0 + WX1) / 2 - 0.04, (WX0 + WX1) / 2 + 0.04, WZ0, WZ1)), ("fr_H", (WX0, WX1, 1.62, 1.70))):
    box(nm, a[0], a[1], WY - 0.06, WY + 0.3, a[2], a[3], TRIM, 0.025)
# window seat with cushion
box("seat", WX0 - 0.3, WX1 + 0.3, WY - 0.55, WY, 0, 0.5, TRIM, 0.03)
box("cushion", WX0 - 0.25, WX1 + 0.25, WY - 0.52, WY - 0.02, 0.5, 0.62, CUSHION, 0.05)
# painted sky backdrop outside the window
plane("sky", (0.8, 6.5, 1.8), (8.0, 4.0), (math.radians(90), 0, 0), flatcard("sky_day.png"))
SKY = bpy.data.objects["sky"]
# curtain rod and curtains with soft folds
cyl("rod", (0.8, WY - 0.12, 2.62), 0.025, 2.9, BRASS, rot=(0, math.radians(90), 0))
for x in (-0.65, 2.25):
    sphere("rod_knob", (x, WY - 0.12, 2.62), 0.05, BRASS)


def curtain(name, x0, x1, gather):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=60, y_segments=8, size=0.5, calc_uvs=True)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    w, h = x1 - x0, 2.5
    for v in me.vertices:
        u, t = v.co.x + 0.5, v.co.y + 0.5
        depth = 0.05 * (1 + gather * (1 - t)) * math.sin(u * math.pi * 10)
        v.co = Vector((x0 + u * w * (1 - 0.25 * gather * (1 - t)) + (0.25 * gather * (1 - t) * w if gather < 0 else 0), WY - 0.16 + depth, 0.12 + t * h))
    me.materials.append(CURTAIN)
    for p in me.polygons: p.use_smooth = True
    return o


curtain("curtain_L", -0.7, 0.22, 1.0)
curtain("curtain_R", 1.38, 2.3, -1.0)
# rug
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=0.012, location=(0.55, 1.6, 0.006))
rug = bpy.context.active_object; rug.scale = (1.25, 0.85, 1); rug.data.materials.append(RUG)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.uv.cylinder_project(); bpy.ops.object.mode_set(mode="OBJECT")
# wall shelf with books on the side wall
box("shelf", -2.45, -2.05, 0.8, 2.2, 1.72, 1.78, TRIM, 0.01)
x = 0.85
for i in range(9):
    h, w = random.uniform(0.22, 0.32), random.uniform(0.06, 0.1)
    col = random.choice(["toy_red.png", "toy_cream.png", "rug.png", "curtain.png", "brass.png"])
    box(f"book{i}", -2.43, -2.12, x, x + w, 1.78, 1.78 + h, painted(col, 3.0), 0.008)
    x += w + 0.01
# bedside table (foreground left) with the desk globe, its rocky ring and a toy rocket
box("table_top", -1.75, -0.85, 0.25, 0.95, 0.72, 0.78, TRIM, 0.02)
for lx, ly in ((-1.68, 0.32), (-0.92, 0.32), (-1.68, 0.88), (-0.92, 0.88)):
    box("leg", lx - 0.03, lx + 0.03, ly - 0.03, ly + 0.03, 0, 0.72, TRIM, 0.01)
G = Vector((-1.35, 0.62, 1.08))
cyl("globe_base", (G.x, G.y, 0.80), 0.09, 0.04, BRASS)
cyl("globe_stem", (G.x, G.y, 0.86), 0.015, 0.1, BRASS)
globe = sphere("globe", G, 0.17, GLOBE)
globe.rotation_euler = (math.radians(23), 0, math.radians(30))
tilt = math.radians(23)
for i in range(46):
    a = i / 46 * 2 * math.pi + random.uniform(-0.04, 0.04)
    r = random.uniform(0.26, 0.31)
    p = Vector((r * math.cos(a), r * math.sin(a), random.uniform(-0.006, 0.006)))
    p = Vector((p.x, p.y * math.cos(tilt) - p.z * math.sin(tilt), p.y * math.sin(tilt) + p.z * math.cos(tilt)))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.010, 0.018), location=G + p)
    rk = bpy.context.active_object
    rk.scale = (random.uniform(0.8, 1.3), random.uniform(0.8, 1.3), random.uniform(0.7, 1.1))
    rk.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3))
    rk.data.materials.append(ROCK)
cyl("rocket_body", (-1.0, 0.45, 0.88), 0.04, 0.2, TOYC, verts=24)
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.04, depth=0.08, location=(-1.0, 0.45, 1.02))
bpy.context.active_object.data.materials.append(TOYR)
for k in range(3):
    a = k * 2 * math.pi / 3
    box("fin", -1.0 + 0.045 * math.cos(a) - 0.008, -1.0 + 0.045 * math.cos(a) + 0.008, 0.45 + 0.045 * math.sin(a) - 0.008,
        0.45 + 0.045 * math.sin(a) + 0.008, 0.78, 0.85, TOYR)
# kid card and its contact shadow
KID_H = 1.18
# wall picture, a potted plant on the seat, and toy blocks on the rug (painted detail and depth)
box("frame", -1.75, -0.55, WY - 0.05, WY, 1.35, 2.25, TRIM, 0.02)
plane("picture", (-1.15, WY - 0.056, 1.8), (1.0, 0.75), (math.radians(90), 0, 0), painted("picture.png", 1.0, "UV", lift=1.05))
cyl("pot", (1.45, WY - 0.3, 0.74), 0.11, 0.2, painted("pot.png", 3.0), verts=24)
for k in range(9):
    a = k * 2 * math.pi / 9
    sphere("leaf", (1.45 + 0.1 * math.cos(a), WY - 0.3 + 0.1 * math.sin(a), 0.92 + 0.08 * (k % 3)), 0.09, painted("leaf.png", 4.0), scale=(0.6, 0.6, 1.3))
for k, (bx, by, c) in enumerate(((0.1, 1.2, "toy_red.png"), (0.24, 1.15, "curtain.png"), (0.16, 1.3, "brass.png"))):
    o = box("block", bx - 0.06, bx + 0.06, by - 0.06, by + 0.06, 0.012 + 0.0 * k, 0.132, painted(c, 4.0), 0.012)
    o.rotation_euler.z = random.uniform(-0.5, 0.5)
# Saturn poster (printed cutout) on the wall right of the window
plane("saturn_poster", (2.55, WY - 0.02, 1.6), (0.6, 0.6 * 1466 / 1120), (math.radians(90), 0, 0), flatcard("PROP-SATURN-POSTER.png"))
kid_imgs = {k: image(f"KID-{k}.png") for k in ("FRONT", "BACK")}


def kid_card(kind, loc):
    im = kid_imgs[kind]
    w = KID_H * im.size[0] / im.size[1]
    o = plane(f"kid_{kind}", (loc[0], loc[1], KID_H / 2), (w, KID_H), (math.radians(90), 0, 0), flatcard(f"KID-{kind}.png"))
    sh = plane(f"kid_{kind}_shadow", (loc[0], loc[1], 0.016), (w * 1.5, 0.42), (0, 0, 0), shadow_mat())
    return o, sh


kid_front = kid_card("FRONT", (0.8, 2.35))
kid_back = kid_card("BACK", (0.8, 2.25))

# ---------- light: soft, high ambient; mood from the grade ----------
def light(kind, loc, energy, color, rot=(0, 0, 0), size=None, angle=None):
    ld = bpy.data.lights.new(kind, kind)
    ld.energy, ld.color = energy, hexcol(color)[:3]
    if size: ld.size = size
    if angle: ld.angle = math.radians(angle)
    o = bpy.data.objects.new(kind, ld)
    o.location, o.rotation_euler = loc, rot
    sc.collection.objects.link(o)
    return ld


sun = light("SUN", (0, 5, 5), 3.2, "#FFE7C2", rot=(math.radians(-58), 0, math.radians(-12)), angle=18)
win = light("AREA", (0.8, WY - 0.3, 1.65), 160, "#FFF0D8", rot=(math.radians(90), 0, 0), size=1.6)
fill = light("AREA", (0.4, -2.6, 2.4), 260, "#FFF6EA", rot=(math.radians(70), 0, math.radians(180)), size=4)

STATES = {
    "LS1": dict(grade="#F4E8D6", world=("#F7EEDF", 0.9), sun=3.2, win=160, fill=260, sky="sky_day.png"),
    "LS8": dict(grade="#D8C9E6", world=("#E2D6EE", 0.7), sun=1.4, win=110, fill=180, sky="sky_dawn.png"),
}


def set_state(k):
    s = STATES[k]
    g_rgb.outputs[0].default_value = hexcol(s["grade"])
    bgn.inputs[0].default_value, bgn.inputs[1].default_value = hexcol(s["world"][0]), s["world"][1]
    sun.energy, win.energy, fill.energy = s["sun"], s["win"], s["fill"]
    SKY.data.materials[0] = flatcard(s["sky"])


cam_data = bpy.data.cameras.new("cam"); cam_data.sensor_fit = "VERTICAL"
cam = bpy.data.objects.new("cam", cam_data); sc.collection.objects.link(cam); sc.camera = cam
aim = bpy.data.objects.new("aim", None); sc.collection.objects.link(aim)
tcn = cam.constraints.new("TRACK_TO"); tcn.target, tcn.track_axis, tcn.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
cam_data.dof.use_dof, cam_data.dof.focus_object = True, aim

SHOTS = [
    ("A_S01V1_globe", "LS1", "FRONT", (-0.85, -0.6, 1.3), (-1.3, 0.66, 1.05), 30, 5.6),
    ("B_S01V2_window", "LS1", "FRONT", (0.05, -2.3, 1.3), (0.7, 2.6, 1.3), 24, 8.0),
    ("C_S10_dawn", "LS8", "BACK", (0.55, 0.15, 1.05), (0.8, 3.2, 1.6), 28, 8.0),
]
os.makedirs(OUT, exist_ok=True)
for name, state, kid, pos, tgt, lens, fstop in SHOTS:
    set_state(state)
    for k, (o, sh) in (("FRONT", kid_front), ("BACK", kid_back)):
        o.hide_render = sh.hide_render = k != kid
    cam.location, aim.location = pos, tgt
    cam_data.lens, cam_data.dof.aperture_fstop = lens, fstop
    sc.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath)
