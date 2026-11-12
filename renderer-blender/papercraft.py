"""Shared Blender helpers for the papercraft look (visual-style v2, EP003 set-specs v1).

Painted textures x soft light ramp x gentle AO x one whole-scene grade, emitted,
so surfaces never show a hard terminator. Sets carry no outlines; cutout cards
(characters, printed props) are unlit images x grade. Same shading as the
approved bedroom look test.
"""
import math, os
import bpy, bmesh
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
TEX, CARDS = os.path.join(HERE, "textures"), os.path.join(HERE, "cards")
LIFT = 0.88
CEL = False   # cel look (draft visual-style v3): hard light bands + ink outlines; set before building materials
INK = "#2B2238"
_imgs, _mats = {}, {}


def hexcol(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb], a)


def setup(scale=100, samples=48):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, scale
    sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"
    sc.eevee.taa_render_samples = samples
    global GRADE, G_RGB, G_SAT, WORLD
    GRADE = bpy.data.node_groups.new("Grade", "ShaderNodeTree")
    GRADE.interface.new_socket(name="Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    GRADE.interface.new_socket(name="Sat", in_out="OUTPUT", socket_type="NodeSocketFloat")
    out, G_RGB, G_SAT = GRADE.nodes.new("NodeGroupOutput"), GRADE.nodes.new("ShaderNodeRGB"), GRADE.nodes.new("ShaderNodeValue")
    GRADE.links.new(G_RGB.outputs[0], out.inputs[0]); GRADE.links.new(G_SAT.outputs[0], out.inputs[1])
    G_SAT.outputs[0].default_value = 1.0
    WORLD = bpy.data.worlds.new("World")
    sc.world = WORLD
    WORLD.use_nodes = True
    n, l = WORLD.node_tree.nodes, WORLD.node_tree.links
    env, mx = n.new("ShaderNodeTexEnvironment"), n.new("ShaderNodeMix")
    mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"; mx.inputs["Factor"].default_value = 1
    gr = n.new("ShaderNodeGroup"); gr.node_tree = GRADE
    l.new(env.outputs["Color"], mx.inputs["A"]); l.new(gr.outputs[0], mx.inputs["B"])
    hs = _sat(n, l, mx.outputs["Result"], gr)
    l.new(hs.outputs[0], n["Background"].inputs[0])
    return sc


def _sat(n, l, color_out, gr):
    """Hue/Saturation node driven by the grade's saturation value."""
    hs = n.new("ShaderNodeHueSaturation")
    l.new(color_out, hs.inputs["Color"]); l.new(gr.outputs["Sat"], hs.inputs["Saturation"])
    return hs


def image(name):
    if name not in _imgs:
        _imgs[name] = bpy.data.images.load(os.path.join(CARDS if os.path.exists(os.path.join(CARDS, name)) else TEX, name))
    return _imgs[name]


def set_world(tex, strength, grade, sat=1.0):
    env = next(n for n in WORLD.node_tree.nodes if n.bl_idname == "ShaderNodeTexEnvironment")
    env.image = image(tex)
    WORLD.node_tree.nodes["Background"].inputs[1].default_value = strength
    G_RGB.outputs[0].default_value = hexcol(grade)
    G_SAT.outputs[0].default_value = sat


def painted(tex, scale=1.0, coords="OBJ", lift=1.0):
    key = (tex, scale, coords, lift)
    if key in _mats:
        return _mats[key]
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
    dif, s2r, bw, mul, ramp = (n.new(t) for t in ("ShaderNodeBsdfDiffuse", "ShaderNodeShaderToRGB", "ShaderNodeRGBToBW", "ShaderNodeMath", "ShaderNodeValToRGB"))
    l.new(dif.outputs[0], s2r.inputs[0]); l.new(s2r.outputs[0], bw.inputs[0]); l.new(bw.outputs[0], mul.inputs[0]); l.new(mul.outputs[0], ramp.inputs[0])
    mul.operation, mul.inputs[1].default_value = "MULTIPLY", 0.55
    e = ramp.color_ramp.elements
    lift *= LIFT
    ao, aomix = n.new("ShaderNodeAmbientOcclusion"), n.new("ShaderNodeMapRange")
    ao.inputs["Distance"].default_value = 0.6
    if CEL:
        # three flat tones with hard edges between them; AO snaps to one contact-shadow step
        ramp.color_ramp.interpolation = "CONSTANT"
        e[0].position, e[0].color = 0.0, (0.56 * lift, 0.55 * lift, 0.70 * lift, 1)   # cool violet shadow
        e[1].position, e[1].color = 0.72, (1.10 * lift, 1.07 * lift, 1.0 * lift, 1)   # warm light
        e.new(0.44).color = (0.90 * lift, 0.89 * lift, 0.93 * lift, 1)
        aomix.interpolation_type = "STEPPED"
        aomix.inputs["Steps"].default_value = 1
        aomix.inputs[1].default_value, aomix.inputs[2].default_value = 0.55, 1.1
        aomix.inputs[3].default_value, aomix.inputs[4].default_value = 0.8, 1.0
    else:
        ramp.color_ramp.interpolation = "EASE"
        e[0].position, e[0].color = 0.0, (0.66 * lift,) * 3 + (1,)
        e[1].position, e[1].color = 0.9, (1.06 * lift,) * 3 + (1,)
        e.new(0.45).color = (0.92 * lift,) * 3 + (1,)
        aomix.inputs[3].default_value, aomix.inputs[4].default_value = 0.8, 1.0
    l.new(ao.outputs["AO"], aomix.inputs[0])
    m1, m2, m3 = (n.new("ShaderNodeMix") for _ in range(3))
    for mx in (m1, m2, m3):
        mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"; mx.inputs["Factor"].default_value = 1.0
    gr = n.new("ShaderNodeGroup"); gr.node_tree = GRADE
    l.new(it.outputs["Color"], m1.inputs["A"]); l.new(ramp.outputs[0], m1.inputs["B"])
    l.new(m1.outputs["Result"], m2.inputs["A"]); l.new(aomix.outputs[0], m2.inputs["B"])
    l.new(m2.outputs["Result"], m3.inputs["A"]); l.new(gr.outputs[0], m3.inputs["B"])
    em = n.new("ShaderNodeEmission")
    l.new(_sat(n, l, m3.outputs["Result"], gr).outputs[0], em.inputs[0]); l.new(em.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    _mats[key] = m
    return m


def cel_ink(sc, px=5.0, inner_px=2.8, crease_deg=140):
    """Freestyle ink lines on painted 3D geometry only (cards already carry drawn outlines; glows,
    rings and dots stay soft). Outer edges px wide, folds and creases inner_px, at 1080 wide,
    scaled with the render percentage."""
    ink = bpy.data.collections.get("INK") or bpy.data.collections.new("INK")   # not linked to the scene: a selection set
    for o in sc.objects:
        mats = [s.material for s in getattr(o, "material_slots", []) if s.material]
        if o.type == "MESH" and mats and all(m.name.startswith("paint_") for m in mats) and o.name not in ink.objects:
            ink.objects.link(o)
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = "ABSOLUTE"
    fs = sc.view_layers[0].freestyle_settings
    fs.crease_angle = math.radians(crease_deg)
    while len(fs.linesets) < 2:
        fs.linesets.new("Ink")
    for ls, edges, w in ((fs.linesets[0], ("silhouette", "border", "external_contour"), px), (fs.linesets[1], ("crease",), inner_px)):
        if ls.linestyle is None:   # an empty factory file has no line style
            ls.linestyle = bpy.data.linestyles.new("Ink")
        ls.select_by_collection, ls.collection, ls.collection_negation = True, ink, "INCLUSIVE"
        ls.select_by_visibility, ls.visibility = True, "VISIBLE"
        ls.select_by_edge_types = True
        for k in ("silhouette", "border", "crease", "external_contour"):
            setattr(ls, "select_" + k, k in edges)
        st = ls.linestyle
        st.color = hexcol(INK)[:3]
        st.thickness = w * sc.render.resolution_percentage / 100
        st.caps = "ROUND"
    return ink


def flatcard(tex, strength=1.0):
    """Unlit image x grade, with alpha: cutout characters, printed props, overlays."""
    key = ("card", tex, strength)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new("card_" + tex)
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    it = n.new("ShaderNodeTexImage"); it.image = image(tex)
    gr = n.new("ShaderNodeGroup"); gr.node_tree = GRADE
    mx = n.new("ShaderNodeMix"); mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"; mx.inputs["Factor"].default_value = 1
    l.new(it.outputs["Color"], mx.inputs["A"]); l.new(gr.outputs[0], mx.inputs["B"])
    em, tr, mix = n.new("ShaderNodeEmission"), n.new("ShaderNodeBsdfTransparent"), n.new("ShaderNodeMixShader")
    em.inputs[1].default_value = strength
    l.new(_sat(n, l, mx.outputs["Result"], gr).outputs[0], em.inputs[0])
    l.new(it.outputs["Alpha"], mix.inputs[0]); l.new(tr.outputs[0], mix.inputs[1]); l.new(em.outputs[0], mix.inputs[2])
    l.new(mix.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    m.surface_render_method = "DITHERED"
    _mats[key] = m
    return m


def ring_mat(tex="ring_band.png", haze="#CFE6F5", haze_amt=0.3, strength=1.0, opaque=False, alpha_mul=1.0):
    """Unlit painted ring with see-through gaps, softened toward the sky colour (aerial haze)."""
    m = bpy.data.materials.new("ring_" + tex)
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    it = n.new("ShaderNodeTexImage"); it.image = image(tex)
    hz = n.new("ShaderNodeMix"); hz.data_type = "RGBA"; hz.inputs["Factor"].default_value = haze_amt
    hz.inputs["B"].default_value = hexcol(haze)
    l.new(it.outputs["Color"], hz.inputs["A"])
    gr = n.new("ShaderNodeGroup"); gr.node_tree = GRADE
    mx = n.new("ShaderNodeMix"); mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"; mx.inputs["Factor"].default_value = 1
    l.new(hz.outputs["Result"], mx.inputs["A"]); l.new(gr.outputs[0], mx.inputs["B"])
    em, tr, mix = n.new("ShaderNodeEmission"), n.new("ShaderNodeBsdfTransparent"), n.new("ShaderNodeMixShader")
    em.inputs[1].default_value = strength
    l.new(_sat(n, l, mx.outputs["Result"], gr).outputs[0], em.inputs[0])
    if opaque:   # the ring's rim, seen edge-on from the equator
        l.new(em.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
        return m
    am = n.new("ShaderNodeMath"); am.operation = "MULTIPLY"; am.inputs[1].default_value = alpha_mul
    l.new(it.outputs["Alpha"], am.inputs[0])
    l.new(am.outputs[0], mix.inputs[0]); l.new(tr.outputs[0], mix.inputs[1]); l.new(em.outputs[0], mix.inputs[2])
    l.new(mix.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])
    m.surface_render_method = "BLENDED"
    return m
    return m


def shadow_mat(strength=0.5):
    if "shadow" in _mats:
        return _mats["shadow"]
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
    _mats["shadow"] = m
    return m


def _finish(o, mat, name):
    o.name = name
    if mat:
        o.data.materials.append(mat)
    return o


def box(name, c, size, mat, bevel=0.0, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=c, rotation=rot)
    o = bpy.context.active_object
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width, b.segments = bevel, 3
    return _finish(o, mat, name)


def plane(name, c, size, rot, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=c, rotation=rot)
    o = bpy.context.active_object
    o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, mat, name)


def cyl(name, c, r, depth, mat, rot=(0, 0, 0), verts=32, r2=None, bevel=0.0):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=c, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=c, rotation=rot)
    o = bpy.context.active_object
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width, b.segments = bevel, 3
    return _finish(o, mat, name)


def blob(name, c, r, mat, scale=(1, 1, 1), smooth=True, sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=c)
    o = bpy.context.active_object
    o.scale = scale
    if smooth:
        bpy.ops.object.shade_smooth()
    return _finish(o, mat, name)


def sphere(name, c, r, mat, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=r, location=c)
    o = bpy.context.active_object
    o.scale = scale
    bpy.ops.object.shade_smooth()
    return _finish(o, mat, name)


def wedge(name, c, w, h, L, mat, rotz=0.0, bevel=0.04):
    """Triangular roof prism, ridge along local x."""
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in ((-L / 2, -w / 2, 0), (-L / 2, w / 2, 0), (-L / 2, 0, h), (L / 2, -w / 2, 0), (L / 2, w / 2, 0), (L / 2, 0, h))]
    for f in ((0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)):
        bm.faces.new([vs[i] for i in f])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.location, o.rotation_euler.z = c, rotz
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL"); b.width, b.segments = bevel, 3
    me.materials.append(mat)
    return o


def strip(name, pts, widths, mat, up=(0, 0, 1)):
    """Ribbon along a polyline (leaves, fronds) with UVs along its length."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    rows = []
    for i, (p, w) in enumerate(zip(pts, widths)):
        p = Vector(p)
        d = (Vector(pts[min(i + 1, len(pts) - 1)]) - Vector(pts[max(i - 1, 0)])).normalized()
        side = d.cross(Vector(up)).normalized() * w / 2
        rows.append((bm.verts.new(p - side), bm.verts.new(p + side)))
    n = len(rows)
    for i in range(n - 1):
        f = bm.faces.new((rows[i][0], rows[i + 1][0], rows[i + 1][1], rows[i][1]))
        for lp, (u, v) in zip(f.loops, ((i / (n - 1), 0), ((i + 1) / (n - 1), 0), ((i + 1) / (n - 1), 1), (i / (n - 1), 1))):
            lp[uv].uv = (u, v)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    me.materials.append(mat)
    return o


def ring(name, origin, lat_deg, R, r_in, r_out, mat, thick=0.012, segs=720, rim_mat=None):
    """A planetary ring in Earth's equatorial plane, seen from a set on the surface at latitude lat.
    Local frame of the set: z up, y north. Earth's centre is R below the set."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    inner = [bm.verts.new((r_in * R * math.cos(a), r_in * R * math.sin(a), 0)) for a in (2 * math.pi * i / segs for i in range(segs))]
    outer = [bm.verts.new((r_out * R * math.cos(a), r_out * R * math.sin(a), 0)) for a in (2 * math.pi * i / segs for i in range(segs))]
    for i in range(segs):
        j = (i + 1) % segs
        f = bm.faces.new((inner[i], inner[j], outer[j], outer[i]))
        for lp, (u, v) in zip(f.loops, ((i / segs * 40, 0), ((i + 1) / segs * 40, 0), ((i + 1) / segs * 40, 1), (i / segs * 40, 1))):
            lp[uv].uv = (u, v)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    me.materials.append(mat)
    sol = o.modifiers.new("thick", "SOLIDIFY"); sol.thickness = thick * R; sol.offset = 0
    if rim_mat is not None:
        me.materials.append(rim_mat); sol.material_offset_rim = 1
    lat = math.radians(lat_deg)
    axis = Vector((0, math.cos(lat), math.sin(lat)))
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(axis)
    o.location = Vector(origin) + Vector((0, 0, -R))
    return o


CARD_OBJS = []


def face_cards(cam_loc):
    """Turn every cutout card about the world up axis so it faces the camera (its normal is local -Y)."""
    for o, base in CARD_OBJS:
        d = Vector(cam_loc) - base
        o.rotation_euler.z = math.atan2(d.x, -d.y)


def card(name, tex, height, c, cam=None, shadow=True, shadow_w=1.4):
    im = image(tex)
    w = height * im.size[0] / im.size[1]
    # upright quad with its origin at the feet and its face toward local -Y
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    vs = [bm.verts.new(v) for v in ((-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, height), (-w / 2, 0, height))]
    f = bm.faces.new(vs)
    for lp, t in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uv].uv = t
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(flatcard(tex))
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.location = c
    CARD_OBJS.append((o, Vector((c[0], c[1], c[2]))))
    sh = plane(name + "_shadow", (c[0], c[1], c[2] + 0.012), (w * shadow_w, height * 0.3), (0, 0, 0), shadow_mat()) if shadow else None
    return o, sh


def light(name, kind, loc, energy, color, rot=(0, 0, 0), size=None, angle=None):
    ld = bpy.data.lights.new(name, kind)
    ld.energy, ld.color = energy, hexcol(color)[:3]
    if size: ld.size = size
    if angle: ld.angle = math.radians(angle)
    o = bpy.data.objects.new(name, ld)
    o.location, o.rotation_euler = loc, rot
    bpy.context.collection.objects.link(o)
    return o


def collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    vl = bpy.context.view_layer
    vl.active_layer_collection = vl.layer_collection.children[name]
    return col


def camera(clip_end=60000):
    sc = bpy.context.scene
    data = bpy.data.cameras.new("cam"); data.sensor_fit = "VERTICAL"; data.clip_start, data.clip_end = 0.05, clip_end
    cam = bpy.data.objects.new("cam", data); sc.collection.objects.link(cam); sc.camera = cam
    aim = bpy.data.objects.new("aim", None); sc.collection.objects.link(aim)
    t = cam.constraints.new("TRACK_TO"); t.target, t.track_axis, t.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
    data.dof.use_dof, data.dof.focus_object = True, aim
    return cam, aim


def emit(color, strength=1.0, alpha=None):
    """Plain glowing colour (pins, crater flashes, sparkles), multiplied by the grade."""
    key = ("emit", color, strength, alpha)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new("emit_" + color)
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    n.clear()
    em = n.new("ShaderNodeEmission"); em.inputs[0].default_value = hexcol(color); em.inputs[1].default_value = strength
    out = n.new("ShaderNodeOutputMaterial")
    if alpha is None:
        l.new(em.outputs[0], out.inputs[0])
    else:
        tr, mx = n.new("ShaderNodeBsdfTransparent"), n.new("ShaderNodeMixShader")
        mx.inputs[0].default_value = alpha
        l.new(tr.outputs[0], mx.inputs[1]); l.new(em.outputs[0], mx.inputs[2]); l.new(mx.outputs[0], out.inputs[0])
        m.surface_render_method = "BLENDED"
    _mats[key] = m
    return m


def ring_around(name, center, Rg, r_in, r_out, mat, tilt_deg=0.0, rim_mat=None, thick=0.01, segs=360):
    """A ring around a free-floating globe of radius Rg, tilted about the x axis."""
    o = ring(name, Vector(center) + Vector((0, 0, Rg)), 90, Rg, r_in, r_out, mat, thick=thick, segs=segs, rim_mat=rim_mat)
    o.rotation_mode = "XYZ"
    o.rotation_euler = (math.radians(tilt_deg), 0, 0)
    o.location = Vector(center)
    return o
