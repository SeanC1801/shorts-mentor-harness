"""Flat two-tone look and 3D characters (LOOK TEST, 2026-11-13; not an approved style).

Tried against visual-style v3 (painted textures, three light bands, flat cutout character cards):
- surfaces are flat colour fills with one hard shadow tone (tinted cool by a scene-wide shade colour)
- skies are clean gradients, not painted cards
- characters are real 3D figures (egg head with a painted, swappable face; bean body; thin limbs), so they
  take the scene's light, cast real shadows, get the same ink line as the set, and never hide lines behind
  an invisible card rectangle
Uses papercraft.py for setup, camera, grade and the Freestyle ink pass (materials named paint_* get inked).
"""
import math, os
import bpy, bmesh
from mathutils import Vector, Matrix
import papercraft as pc

V = Vector
FACES = os.path.join(pc.TEX, "faces3d")
_flat = {}
SHADE = None      # node group: the scene-wide shadow multiplier (cool tint)
AMBIENT = 0.30    # light every surface gets from the sky (shadows sit at this level)
SKIN_SOFT = 0.0   # 0..1: how far skin shadows are lifted back toward the skin colour (look test v2 uses 0.45)


def _shade_group():
    global SHADE
    if SHADE is None or SHADE.name not in bpy.data.node_groups:
        SHADE = bpy.data.node_groups.new("Shade", "ShaderNodeTree")
        SHADE.interface.new_socket(name="Color", in_out="OUTPUT", socket_type="NodeSocketColor")
        SHADE.interface.new_socket(name="Step", in_out="OUTPUT", socket_type="NodeSocketFloat")
        SHADE.interface.new_socket(name="Hi", in_out="OUTPUT", socket_type="NodeSocketFloat")
        SHADE.interface.new_socket(name="Light", in_out="OUTPUT", socket_type="NodeSocketFloat")
        out, rgb, val = SHADE.nodes.new("NodeGroupOutput"), SHADE.nodes.new("ShaderNodeRGB"), SHADE.nodes.new("ShaderNodeValue")
        hi, lt = SHADE.nodes.new("ShaderNodeValue"), SHADE.nodes.new("ShaderNodeValue")
        rgb.name, val.name, hi.name, lt.name = "tint", "step", "hi", "light"
        rgb.outputs[0].default_value = (0.60, 0.58, 0.86, 1)
        val.outputs[0].default_value = 0.6
        hi.outputs[0].default_value = 1e6      # highlight tone off
        lt.outputs[0].default_value = 0.0      # coloured light off
        SHADE.links.new(rgb.outputs[0], out.inputs[0]); SHADE.links.new(val.outputs[0], out.inputs[1])
        SHADE.links.new(hi.outputs[0], out.inputs[2]); SHADE.links.new(lt.outputs[0], out.inputs[3])
    return SHADE


def set_shade(tint, step, hi=None, light=0.0):
    """Shadow tint (multiplies the fill colour in shade) and the light level where shade turns to light.
    hi: light level above which a brighter highlight tone appears (None = off).
    light: 0..1, how much a lamp's own colour tints the surfaces it lights (0 = off)."""
    g = _shade_group()
    g.nodes["tint"].outputs[0].default_value = (*tint, 1)
    g.nodes["step"].outputs[0].default_value = step
    g.nodes["hi"].outputs[0].default_value = 1e6 if hi is None else hi
    g.nodes["light"].outputs[0].default_value = light


def _two_tone(n, l, color_socket):
    """color -> (color x shade tint) in shadow, color in light, one hard edge; returns the mixed colour socket."""
    sh = n.new("ShaderNodeGroup"); sh.node_tree = _shade_group()
    dif, s2r, bw, gt = (n.new(t) for t in ("ShaderNodeBsdfDiffuse", "ShaderNodeShaderToRGB", "ShaderNodeRGBToBW", "ShaderNodeMath"))
    dif.inputs["Color"].default_value = (1, 1, 1, 1)
    gt.operation = "GREATER_THAN"
    l.new(dif.outputs[0], s2r.inputs[0]); l.new(s2r.outputs[0], bw.inputs[0]); l.new(bw.outputs[0], gt.inputs[0]); l.new(sh.outputs["Step"], gt.inputs[1])
    dark = n.new("ShaderNodeMix"); dark.data_type, dark.blend_type = "RGBA", "MULTIPLY"; dark.inputs["Factor"].default_value = 1
    l.new(color_socket, dark.inputs["A"]); l.new(sh.outputs["Color"], dark.inputs["B"])
    # highlight tone: the fill colour lifted toward white where the light is strongest
    gain = n.new("ShaderNodeMix"); gain.data_type, gain.blend_type = "RGBA", "MULTIPLY"; gain.inputs["Factor"].default_value = 1
    gain.inputs["B"].default_value = (1.22, 1.2, 1.14, 1); l.new(color_socket, gain.inputs["A"])
    lift = n.new("ShaderNodeMix"); lift.data_type = "RGBA"; lift.inputs["Factor"].default_value = 0.05
    lift.inputs["B"].default_value = (1, 1, 1, 1); l.new(gain.outputs["Result"], lift.inputs["A"])
    gh = n.new("ShaderNodeMath"); gh.operation = "GREATER_THAN"
    l.new(bw.outputs[0], gh.inputs[0]); l.new(sh.outputs["Hi"], gh.inputs[1])
    lit = n.new("ShaderNodeMix"); lit.data_type = "RGBA"
    l.new(gh.outputs[0], lit.inputs["Factor"]); l.new(color_socket, lit.inputs["A"]); l.new(lift.outputs["Result"], lit.inputs["B"])
    # coloured light: the hue of whatever lights the surface (lamp, neon) tints the lit tone
    inv = n.new("ShaderNodeMath"); inv.operation = "DIVIDE"; inv.inputs[0].default_value = 1.0
    mxv = n.new("ShaderNodeMath"); mxv.operation = "MAXIMUM"; mxv.inputs[1].default_value = 0.05
    l.new(bw.outputs[0], mxv.inputs[0]); l.new(mxv.outputs[0], inv.inputs[1])
    hue = n.new("ShaderNodeVectorMath"); hue.operation = "SCALE"
    l.new(s2r.outputs[0], hue.inputs[0]); l.new(inv.outputs[0], hue.inputs["Scale"])
    tinted = n.new("ShaderNodeMix"); tinted.data_type, tinted.blend_type, tinted.clamp_result = "RGBA", "MULTIPLY", True
    l.new(sh.outputs["Light"], tinted.inputs["Factor"]); l.new(lit.outputs["Result"], tinted.inputs["A"]); l.new(hue.outputs[0], tinted.inputs["B"])
    mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"
    l.new(gt.outputs[0], mx.inputs["Factor"]); l.new(dark.outputs["Result"], mx.inputs["A"]); l.new(tinted.outputs["Result"], mx.inputs["B"])
    return mx.outputs["Result"]


def _finish(n, l, color_socket):
    gr = n.new("ShaderNodeGroup"); gr.node_tree = pc.GRADE
    m = n.new("ShaderNodeMix"); m.data_type, m.blend_type = "RGBA", "MULTIPLY"; m.inputs["Factor"].default_value = 1
    l.new(color_socket, m.inputs["A"]); l.new(gr.outputs[0], m.inputs["B"])
    em = n.new("ShaderNodeEmission")
    l.new(pc._sat(n, l, m.outputs["Result"], gr).outputs[0], em.inputs[0])
    l.new(em.outputs[0], n.new("ShaderNodeOutputMaterial").inputs[0])


def flat(color):
    """Flat colour fill with one hard, tinted shadow tone. Inked (name starts with paint_)."""
    if color in _flat:
        return _flat[color]
    m = bpy.data.materials.new("paint_flat_" + color.lstrip("#")); m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links; n.clear()
    rgb = n.new("ShaderNodeRGB"); rgb.outputs[0].default_value = pc.hexcol(color)
    _finish(n, l, _two_tone(n, l, rgb.outputs[0]))
    _flat[color] = m
    return m


def head_mat(skin, face, half_w=0.158, zc=-0.03):
    """Skin fill with a painted face on the front of the head (planar from the front; swap `face` to change it)."""
    m = bpy.data.materials.new(f"paint_head_{skin.lstrip('#')}_{face}"); m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links; n.clear()
    rgb = n.new("ShaderNodeRGB"); rgb.outputs[0].default_value = pc.hexcol(skin)
    base = _two_tone(n, l, rgb.outputs[0])
    soft = n.new("ShaderNodeMix"); soft.data_type = "RGBA"; soft.inputs["Factor"].default_value = SKIN_SOFT   # 0 = full shadow tone on skin
    l.new(base, soft.inputs["A"]); l.new(rgb.outputs[0], soft.inputs["B"]); base = soft.outputs["Result"]
    tc, sep, comb, it = (n.new(t) for t in ("ShaderNodeTexCoord", "ShaderNodeSeparateXYZ", "ShaderNodeCombineXYZ", "ShaderNodeTexImage"))
    l.new(tc.outputs["Object"], sep.inputs[0])
    u, v = n.new("ShaderNodeMath"), n.new("ShaderNodeMath")
    u.operation = v.operation = "MULTIPLY_ADD"
    u.inputs[1].default_value, u.inputs[2].default_value = 1 / (2 * half_w), 0.5
    v.inputs[1].default_value, v.inputs[2].default_value = 1 / (2 * half_w), 0.5 - zc / (2 * half_w)
    l.new(sep.outputs["X"], u.inputs[0]); l.new(sep.outputs["Z"], v.inputs[0])
    l.new(u.outputs[0], comb.inputs["X"]); l.new(v.outputs[0], comb.inputs["Y"]); l.new(comb.outputs[0], it.inputs[0])
    it.image = bpy.data.images.load(os.path.join(FACES, face + ".png"), check_existing=True)
    it.extension = "CLIP"
    front = n.new("ShaderNodeMath"); front.operation = "LESS_THAN"; front.inputs[1].default_value = -0.02
    l.new(sep.outputs["Y"], front.inputs[0])
    a = n.new("ShaderNodeMath"); a.operation = "MULTIPLY"
    l.new(it.outputs["Alpha"], a.inputs[0]); l.new(front.outputs[0], a.inputs[1])
    mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"
    l.new(a.outputs[0], mx.inputs["Factor"]); l.new(base, mx.inputs["A"]); l.new(it.outputs["Color"], mx.inputs["B"])
    _finish(n, l, mx.outputs["Result"])
    return m


def sky(zenith, horizon, ground, ambient="#FFFFFF", level=None):
    """Clean gradient sky for the camera; a flat ambient light for everything else (so shadows stay one tone)."""
    w = bpy.context.scene.world; nt = w.node_tree; n, l = nt.nodes, nt.links; n.clear()
    tc, sep, ramp = n.new("ShaderNodeTexCoord"), n.new("ShaderNodeSeparateXYZ"), n.new("ShaderNodeValToRGB")
    mr = n.new("ShaderNodeMapRange"); mr.inputs[1].default_value, mr.inputs[2].default_value = -0.25, 1.0
    l.new(tc.outputs["Generated"], sep.inputs[0]); l.new(sep.outputs["Z"], mr.inputs[0]); l.new(mr.outputs[0], ramp.inputs[0])
    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.0, pc.hexcol(ground)
    e[1].position, e[1].color = 0.78, pc.hexcol(zenith)
    e.new(0.195).color = pc.hexcol(ground)
    e.new(0.2).color = pc.hexcol(horizon)
    lp, mx, bg = n.new("ShaderNodeLightPath"), n.new("ShaderNodeMix"), n.new("ShaderNodeBackground")
    mx.data_type = "RGBA"
    amb = pc.hexcol(ambient); lv = AMBIENT if level is None else level
    mx.inputs["A"].default_value = (amb[0] * lv, amb[1] * lv, amb[2] * lv, 1)
    l.new(lp.outputs["Is Camera Ray"], mx.inputs["Factor"]); l.new(ramp.outputs[0], mx.inputs["B"])
    l.new(mx.outputs["Result"], bg.inputs[0]); l.new(bg.outputs[0], n.new("ShaderNodeOutputWorld").inputs[0])


# ---------------- meshes ----------------
def _obj(name, bm, mat, smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o)
    return o


def lathe(name, profile, mat, segs=40, scale=(1, 1, 1)):
    """Surface of revolution about Z from a profile [(r, z), ...] (r = 0 closes an end). Smooth shaded."""
    bm = bmesh.new(); rings = []
    for r, z in profile:
        if r < 1e-6:
            rings.append([bm.verts.new((0, 0, z * scale[2]))])
        else:
            rings.append([bm.verts.new((r * math.cos(2 * math.pi * k / segs) * scale[0], r * math.sin(2 * math.pi * k / segs) * scale[1], z * scale[2])) for k in range(segs)])
    for a, b in zip(rings, rings[1:]):
        for k in range(segs):
            k2 = (k + 1) % segs
            if len(a) == 1 and len(b) == 1:
                continue
            if len(a) == 1:
                bm.faces.new((a[0], b[k], b[k2]))
            elif len(b) == 1:
                bm.faces.new((a[k], b[0], a[k2]))
            else:
                bm.faces.new((a[k], b[k], b[k2], a[k2]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(name, bm, mat)


def ball(name, c, r, mat, scale=(1, 1, 1)):
    n = 14
    o = lathe(name, [(r * math.sin(math.pi * i / n), -r * math.cos(math.pi * i / n)) for i in range(n + 1)], mat, scale=scale)
    o.location = c
    return o


def _tube_rings(pts, r, r_end=None, sides=10, per=8):
    """Rings of points for a round tube through pts (smoothed), radius r tapering to r_end."""
    P = [V(p) for p in pts]
    if len(P) == 2:
        P = [P[0], (P[0] + P[1]) / 2, P[1]]
    ext = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    path = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for s in range(per):
            t = s / per
            path.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    path.append(P[-1])
    rings = []
    nrm = V((0, 1, 0))
    for i, p in enumerate(path):
        tan = (path[min(i + 1, len(path) - 1)] - path[max(i - 1, 0)]).normalized()
        if abs(tan.dot(nrm)) > 0.95:
            nrm = V((1, 0, 0))
        nrm = (nrm - tan * nrm.dot(tan)).normalized(); bi = tan.cross(nrm)
        rr = r + ((r_end if r_end is not None else r) - r) * i / (len(path) - 1)
        rings.append([p + (nrm * math.cos(2 * math.pi * k / sides) + bi * math.sin(2 * math.pi * k / sides)) * rr for k in range(sides)])
    return rings


def tube(name, pts, r, mat, r_end=None, sides=10, per=8):
    """A round tube through the points (smoothed), radius r tapering to r_end. For limbs, stems, pipes."""
    bm = bmesh.new()
    rings = [[bm.verts.new(c) for c in ring] for ring in _tube_rings(pts, r, r_end, sides, per)]
    for a, b in zip(rings, rings[1:]):
        for k in range(sides):
            bm.faces.new((a[k], b[k], b[(k + 1) % sides], a[(k + 1) % sides]))
    bm.faces.new(rings[0]); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _obj(name, bm, mat)
    o["tube"] = (r, r if r_end is None else r_end, sides, per)
    return o


def tube_update(o, pts):
    """Move an existing tube (2 or 3 control points, as built) to new control points. Used to re-pose limbs per frame."""
    r, r_end, sides, per = o["tube"]
    flat_co = [c for ring in _tube_rings(pts, r, r_end, int(sides), int(per)) for v in ring for c in v]
    o.data.vertices.foreach_set("co", flat_co)
    o.data.update()


# ---------------- the character ----------------
LIMB = "#23233B"
RIGS = {}        # name -> the movable parts of each built character (filled by kid(), used by pose_kid and face_kid)
POSES = {   # hand positions and elbow pulls relative to each shoulder (x outward, y forward is -Y, z up); feet (x, y)
    "stand": dict(L=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), R=((0.07, 0.0, -0.33), (0.05, 0.02, 0))),
    "wave": dict(L=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), R=((0.22, -0.02, 0.26), (0.12, 0.0, -0.08))),
    "point_up": dict(L=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), R=((0.10, -0.05, 0.42), (0.06, 0.0, -0.02)), tilt=-8),
    "shock": dict(L=((0.24, -0.02, 0.30), (0.10, 0, -0.10)), R=((0.24, -0.02, 0.30), (0.10, 0, -0.10)), feet=((0.11, 0), (0.11, 0))),
    "shrug": dict(L=((0.26, -0.06, -0.02), (0.06, 0.04, -0.12)), R=((0.26, -0.06, -0.02), (0.06, 0.04, -0.12))),
    "think": dict(L=((0.02, -0.10, -0.20), (0.10, 0.0, -0.05)), R=((-0.06, -0.17, 0.12), (0.10, -0.02, -0.14)), tilt=6),
    "walk": dict(L=((0.05, 0.12, -0.30), (0.04, 0.05, 0)), R=((0.05, -0.14, -0.28), (0.04, -0.02, 0)), feet=((0.06, 0.12), (0.06, -0.14)), lean=4),
    "shield": dict(L=((0.07, 0.0, -0.33), (0.05, 0.02, 0)), R=((-0.07, -0.19, 0.27), (0.16, -0.04, 0.02))),
}


def kid(name, O, pose="stand", face="neutral", skin="#F4EFE6", top="#F2B10C", bottom="#2E6FD1", shoes="#C9482F",
        hair="#4A2C1A", hat=None, turn=0.0, scale=1.0, build="classic"):
    """Build one 3D character standing at O, facing -Y, turned `turn` degrees. Returns (root, parts).
    build "classic": shirt with a coloured hem, thick limbs, ball hands (look test v1).
    build "bean": one long bean body, shorter legs, thinner limbs, smaller hands and shoes (look test v2)."""
    bean = build == "bean"
    LR, HR, SR = (0.015, 0.03, 0.05) if bean else (0.021, 0.042, 0.062)      # limb, hand and shoe radii
    root = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(root)
    parts = []
    P = POSES[pose]
    limb = flat(LIMB)
    rig = RIGS[name] = dict(root=root, O=V(O), bean=bean, skin=skin, legs=[], shoes=[], arms=[], hands=[], sleeves=[], faces={})

    def add(o):
        o.parent = root; parts.append(o); return o
    feet = P.get("feet", ((0.065, 0.0), (0.065, 0.0)))
    hip_z, sh_z = (0.42 if bean else 0.50), 0.745
    for s, (fx, fy) in zip((-1, 1), feet):
        hip, foot = V((s * 0.06, 0, hip_z)), V((s * fx, fy, 0.05))
        rig["legs"].append(add(tube(name + "_leg", [hip, (hip + foot) / 2 + V((0, -0.015 if fy <= 0 else 0.01, 0)), foot], LR, limb)))
        rig["shoes"].append(add(ball(name + "_shoe", foot + V((0, -0.03, -0.012)), SR, flat(shoes), scale=(0.9, 1.45, 0.62))))
    if bean:
        body = add(lathe(name + "_body", [(0, 0.345), (0.07, 0.35), (0.125, 0.38), (0.152, 0.45), (0.156, 0.54), (0.145, 0.64), (0.125, 0.73), (0.10, 0.79), (0.06, 0.815), (0, 0.82)],
                         flat(top), scale=(1, 0.88, 1)))
    else:
        body = add(lathe(name + "_body", [(0, 0.445), (0.10, 0.45), (0.158, 0.475), (0.17, 0.52), (0.158, 0.62), (0.135, 0.72), (0.105, 0.785), (0.06, 0.81), (0, 0.815)],
                         flat(top), scale=(1, 0.86, 1)))
        add(lathe(name + "_hem", [(0, 0.40), (0.11, 0.405), (0.15, 0.43), (0.165, 0.47), (0.15, 0.50), (0, 0.50)], flat(bottom), scale=(1, 0.86, 1)))
    for k in range(3):   # buttons
        add(ball(name + "_button", V((0, (-0.137 if bean else -0.143) + (0.006 if bean else 0.012) * k, (0.50 if bean else 0.56) + 0.085 * k)), 0.016, flat("#FFFFFF"), scale=(1, 0.5, 1)))
    for s, key in ((-1, "L"), (1, "R")):
        hand, elbow = P[key]
        sh = V((s * 0.125, 0, sh_z)); hp = sh + V((s * hand[0], hand[1], hand[2]))
        mid = (sh + hp) / 2 + V((s * elbow[0], elbow[1], elbow[2]))
        if not bean:
            rig["sleeves"].append(add(tube(name + "_sleeve", [sh, sh.lerp(mid, 0.36)], 0.043, flat(top), r_end=0.037)))
        rig["arms"].append(add(tube(name + "_arm", [sh, mid, hp], LR, limb)))
        rig["hands"].append(add(ball(name + "_hand", hp, HR, limb)))
    head = add(lathe(name + "_head", [(0, -0.19)] + [(0.2 * math.sin(a), -0.19 * math.cos(a) if a < math.pi / 2 else -0.265 * math.cos(a))
                                                  for a in (math.pi * i / 22 for i in range(1, 22))] + [(0, 0.265)],
                     head_mat(skin, face), segs=48))
    hz = 0.965
    head.location = (0, 0, hz)
    rig["head"] = head; rig["faces"][face] = head.data.materials[0]
    tilt = math.radians(P.get("tilt", 0))
    head.rotation_euler = (tilt, 0, 0)
    tops = []
    if hat:      # a cap: dome plus a brim
        dome = lathe(name + "_cap", [(0.0, 0.285)] + [(0.208 * math.sin(a), 0.07 + 0.215 * math.cos(a)) for a in (math.pi / 2 * i / 10 for i in range(1, 11))] + [(0.2, 0.055), (0, 0.055)],
                     flat(hat), segs=48)
        brim = lathe(name + "_brim", [(0, 0.062), (0.15, 0.06), (0.165, 0.07), (0.15, 0.082), (0, 0.084)], flat(hat), segs=32, scale=(1.05, 1.0, 1))
        brim.location = (0, -0.19, 0.01)
        tops += [dome, brim]
        add(ball(name + "_capbutton", V((0, 0, hz + 0.287)), 0.022, flat(hat)))
    elif hair:   # hair: a shell over the top and back of the head, hairline high in front, plus a tuft
        bm = bmesh.new()
        segs, rows = 48, 16
        grid = []
        for i in range(rows + 1):
            a = math.pi * i / rows
            z = -0.19 * math.cos(a) if a < math.pi / 2 else -0.265 * math.cos(a)
            grid.append([bm.verts.new((0.207 * math.sin(a) * math.cos(2 * math.pi * k / segs), 0.207 * math.sin(a) * math.sin(2 * math.pi * k / segs), z * 1.035)) for k in range(segs)])
        for i in range(rows):
            for k in range(segs):
                k2 = (k + 1) % segs
                bm.faces.new((grid[i][k], grid[i + 1][k], grid[i + 1][k2], grid[i][k2]))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
        # one slanted cut gives a clean hairline: high over the forehead, dipping at the temples, low at the nape
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0.075), plane_no=(0, 0.19, 0.4), clear_inner=True)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        tops.append(_obj(name + "_hair", bm, flat(hair)))
        tuft = tube(name + "_tuft", [(0, 0.0, 0.25), (0.015, -0.02, 0.31), (0.05, -0.045, 0.335)], 0.03, flat(hair), r_end=0.006)
        tops.append(tuft)
    for o in tops:
        o.parent = head; parts.append(o)
    root.location = V(O)
    root.rotation_euler = (math.radians(P.get("lean", 0)), 0, math.radians(turn))
    root.scale = (scale, scale, scale)
    rig["scale"], rig["turn"] = scale, turn
    return root, parts


# ---------------- moving the character ----------------

def mix_pose(A, B, t):
    """Blend two poses (entries of POSES, or dicts of the same shape); t may overshoot 0..1 a little."""
    def lerp(a, b):
        if isinstance(a, (tuple, list)):
            return tuple(lerp(x, y) for x, y in zip(a, b))
        return a + (b - a) * t
    feet0 = ((0.065, 0.0), (0.065, 0.0))
    out = dict(L=lerp(A["L"], B["L"]), R=lerp(A["R"], B["R"]), feet=lerp(A.get("feet", feet0), B.get("feet", feet0)))
    for k in ("tilt", "lean", "look", "nod"):
        out[k] = lerp(A.get(k, 0.0), B.get(k, 0.0))
    return out


def pose_kid(name, P, turn=None, hop=0.0, squash=1.0, loc=None):
    """Re-pose a built character in place: limbs follow the pose, the head tilts and looks, the body leans,
    hops (metres) and squashes (1 = none; above 1 stretches upward)."""
    rig = RIGS[name]; bean = rig["bean"]
    hip_z, sh_z = (0.42 if bean else 0.50), 0.745
    feet = P.get("feet", ((0.065, 0.0), (0.065, 0.0)))
    for i, (s, (fx, fy)) in enumerate(zip((-1, 1), feet)):
        hip, foot = V((s * 0.06, 0, hip_z)), V((s * fx, fy, 0.05))
        tube_update(rig["legs"][i], [hip, (hip + foot) / 2 + V((0, -0.015 if fy <= 0 else 0.01, 0)), foot])
        rig["shoes"][i].location = foot + V((0, -0.03, -0.012))
    for i, (s, key) in enumerate(((-1, "L"), (1, "R"))):
        hand, elbow = P[key]
        sh = V((s * 0.125, 0, sh_z)); hp = sh + V((s * hand[0], hand[1], hand[2]))
        mid = (sh + hp) / 2 + V((s * elbow[0], elbow[1], elbow[2]))
        if rig["sleeves"]:
            tube_update(rig["sleeves"][i], [sh, sh.lerp(mid, 0.36)])
        tube_update(rig["arms"][i], [sh, mid, hp])
        rig["hands"][i].location = hp
    rig["head"].rotation_euler = (math.radians(P.get("tilt", 0.0) + P.get("nod", 0.0)), 0, math.radians(P.get("look", 0.0)))
    root = rig["root"]
    if turn is not None:
        rig["turn"] = turn
    if loc is not None:
        rig["O"] = V(loc)
    root.location = rig["O"] + V((0, 0, hop))
    root.rotation_euler = (math.radians(P.get("lean", 0.0)), 0, math.radians(rig["turn"]))
    k = rig["scale"]; side = 1 / math.sqrt(squash)
    root.scale = (k * side, k * side, k * squash)


def face_kid(name, face):
    """Swap the painted face (any name in textures/faces3d)."""
    rig = RIGS[name]
    if face not in rig["faces"]:
        rig["faces"][face] = head_mat(rig["skin"], face)
    rig["head"].data.materials[0] = rig["faces"][face]


def glow(sc, strength=0.6, threshold=1.0, size=0.5, vignette=0.0):
    """Finishing pass: bloom around bright lamps, signs and windows, and an optional soft dark vignette."""
    tree = bpy.data.node_groups.new("Finish", "CompositorNodeTree")
    sc.compositing_node_group = tree
    tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    n, l = tree.nodes, tree.links
    rl, gl, out = n.new("CompositorNodeRLayers"), n.new("CompositorNodeGlare"), n.new("NodeGroupOutput")
    for key, val in (("Type", "Bloom"), ("Threshold", threshold), ("Strength", strength), ("Size", size)):
        try:
            gl.inputs[key].default_value = val
        except Exception as e:
            print("glow: could not set", key, e)
    # the ink lines come as their own pass and are laid over the picture before the glow
    sc.render.use_freestyle = True
    sc.view_layers[0].freestyle_settings.as_render_pass = True
    over = n.new("CompositorNodeAlphaOver")
    l.new(rl.outputs["Image"], over.inputs["Background"]); l.new(rl.outputs["Freestyle"], over.inputs["Foreground"])
    l.new(over.outputs[0], gl.inputs["Image"])
    last = gl.outputs[0]
    if vignette > 0:
        el, bl, mx = n.new("CompositorNodeEllipseMask"), n.new("CompositorNodeBlur"), n.new("ShaderNodeMix")
        el.inputs["Size"].default_value = (0.95, 0.95, 0) if len(el.inputs["Size"].default_value) == 3 else (0.95, 0.95)
        bl.inputs["Size"].default_value = (260, 260, 0) if len(bl.inputs["Size"].default_value) == 3 else (260, 260)
        l.new(el.outputs[0], bl.inputs["Image"])
        mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"; mx.inputs["Factor"].default_value = vignette
        lift = n.new("ShaderNodeMath"); lift.operation = "ADD"; lift.inputs[1].default_value = 0.35; lift.use_clamp = True
        l.new(bl.outputs[0], lift.inputs[0])
        l.new(last, mx.inputs["A"]); l.new(lift.outputs[0], mx.inputs["B"])
        last = mx.outputs["Result"]
    l.new(last, out.inputs[0])
    return tree


def sign(text, loc, size=0.3, color="#FFFFFF", rot=(math.pi / 2, 0, 0), strength=1.0, align="CENTER"):
    """Readable set text (shop signs, labels, posters): flat glowing letters facing -Y by default. Not inked."""
    cu = bpy.data.curves.new("sign", "FONT"); cu.body, cu.size, cu.align_x, cu.align_y = text, size, align, "CENTER"
    o = bpy.data.objects.new("sign_" + text[:12], cu); bpy.context.collection.objects.link(o)
    o.location, o.rotation_euler = loc, rot
    cu.materials.append(pc.emit(color, strength))
    return o
