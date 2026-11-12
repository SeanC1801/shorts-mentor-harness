"""Draw CHAR-RAINKID art batch 1 (master front view + face sheet) as layered SVG.

Spec: EPISODES/EP004/character-specs.md v2 (approved 2026-11-10).
usage: python3 -I make_rainkid_v001.py OUT_DIR
Writes CHAR-RAINKID-master-v001.svg and CHAR-RAINKID-faces-v001.svg (drafts).
"""
import os, sys

NAVY = "#232238"
WHITE = "#FFFFFF"
HEAD_SHADE = "#E4E6EE"
HAIR = "#4A3428"
HAIR_HI = "#6E5242"
CORAL = "#FF7A6B"
MOUTH_IN = "#3A1E2E"
BLUSH = "#FFB8A8"
SHIRT, SHIRT_SH = "#6FB7E8", "#5E9CC6"
TROUSER, TROUSER_SH = "#7A7F8C", "#686C77"
SOCK, SOCK_SH = "#C9CCDA", "#ABAEBA"
OL = 11      # outline weight (sheet units; about 1% of frame height at usual size)
LIMB = 15    # limb stroke weight

DEFS = f"""<defs>
<filter id="wobble" x="-5%" y="-5%" width="110%" height="110%">
 <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="11" result="t"/>
 <feDisplacementMap in="SourceGraphic" in2="t" scale="3" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<radialGradient id="cshadow"><stop offset="0" stop-color="#1B1430" stop-opacity="0.38"/><stop offset="1" stop-color="#1B1430" stop-opacity="0"/></radialGradient>
<clipPath id="headclip"><path d="{{HEAD}}"/></clipPath>
<clipPath id="torsoclip"><path d="{{TORSO}}"/></clipPath>
</defs>"""

# Head in head-local coordinates: centre (0,0); egg 378 tall, widest below the middle.
HEAD = ("M 0 -189 C 120 -189 170 -49 168 51 C 166 141 100 189 0 189 "
        "C -100 189 -166 141 -168 51 C -170 -49 -120 -189 0 -189 Z")
HEAD_Y = -651  # head centre above the feet (character-local)
TORSO = ("M -78 -472 Q 0 -484 78 -472 L 108 -282 Q 110 -262 90 -262 "
         "L -90 -262 Q -110 -262 -108 -282 Z")


def p(d, fill="none", stroke=NAVY, w=OL, extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linejoin="round" stroke-linecap="round"{extra}/>')


# ---------- face parts (head-local) ----------
EYE_X, EYE_Y = 62, 45


def eye(side, kind):
    cx, cy = side * EYE_X, EYE_Y
    if kind in ("normal", "wide", "small"):
        rx, ry, hr = {"normal": (24, 36, 8), "wide": (29, 44, 7), "small": (20, 30, 7)}[kind]
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{NAVY}"/>'
                f'<circle cx="{cx + rx * 0.33:.1f}" cy="{cy - ry * 0.36:.1f}" r="{hr}" fill="{WHITE}"/>')
    if kind in ("half", "soft"):
        lid = cy - 4 if kind == "half" else cy - 14
        bend = 0 if kind == "half" else 6
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="24" ry="36" fill="{NAVY}"/>'
                f'<rect x="{cx - 34}" y="{cy - 46}" width="68" height="{lid - (cy - 46)}" fill="{WHITE}"/>'
                f'<circle cx="{cx + 8}" cy="{lid + 13}" r="6" fill="{WHITE}"/>'
                + p(f"M {cx - 30} {lid} Q {cx} {lid - bend} {cx + 30} {lid}", w=9))
    if kind == "squint":  # squeezed shut: > <
        s = -side
        return p(f"M {cx - 20 * s} {cy - 18} L {cx + 18 * s} {cy} L {cx - 20 * s} {cy + 18}", w=10)
    raise ValueError(kind)


def brow(side, outer_y, inner_y):
    ox, ix = side * 95, side * 38
    mx, my = (ox + ix) / 2, (outer_y + inner_y) / 2 - 8
    return p(f"M {ox} {outer_y} Q {mx} {my} {ix} {inner_y}", w=16)


def mouth(kind):
    if kind == "line":
        return p("M -22 120 L 22 120", w=9)
    if kind == "o":
        return f'<ellipse cx="0" cy="122" rx="11" ry="13" fill="{MOUTH_IN}" stroke="{NAVY}" stroke-width="7"/>'
    if kind == "open":
        return (f'<clipPath id="mclip"><ellipse cx="0" cy="130" rx="30" ry="38"/></clipPath>'
                f'<ellipse cx="0" cy="130" rx="30" ry="38" fill="{MOUTH_IN}"/>'
                f'<ellipse cx="0" cy="160" rx="21" ry="13" fill="{CORAL}" clip-path="url(#mclip)"/>'
                f'<ellipse cx="0" cy="130" rx="30" ry="38" fill="none" stroke="{NAVY}" stroke-width="9"/>')
    if kind == "frown":
        return p("M -24 130 Q 0 110 24 130", w=9)
    if kind == "grit":
        return (f'<rect x="-32" y="107" width="64" height="30" rx="12" fill="{WHITE}" stroke="{NAVY}" stroke-width="8"/>'
                + p("M -30 122 L 30 122", w=5) + p("M -11 109 L -11 135 M 11 109 L 11 135", w=4))
    if kind == "zigzag":
        return p("M -30 122 L -20 114 L -10 128 L 0 114 L 10 128 L 20 114 L 30 122", w=7)
    if kind == "smile":
        return p("M -20 116 Q 0 134 20 116", w=9)
    raise ValueError(kind)


FACES = [  # id, label, brows (outer_y, inner_y), eyes, mouth, extras
    ("FACE-RAINKID-CURIOUS", "curious", (-40, -48), "normal", "o", ""),
    ("FACE-RAINKID-DEADPAN", "deadpan", (-14, -14), "half", "line", ""),
    ("FACE-RAINKID-SHOCKED", "shocked", (-58, -68), "wide", "open", ""),
    ("FACE-RAINKID-WORRIED", "worried", (-10, -42), "normal", "frown", ""),
    ("FACE-RAINKID-SQUINT", "squinting", (-36, -6), "squint", "grit", "sweat"),
    ("FACE-RAINKID-SHIVER", "shivering", (-12, -36), "small", "zigzag", "shiver"),
    ("FACE-RAINKID-WISTFUL", "wistful", (-22, -30), "soft", "smile", "blush"),
]


def extras(kind):
    if kind == "blush":
        return "".join(f'<ellipse cx="{s * 104}" cy="96" rx="22" ry="12" fill="{BLUSH}" opacity="0.85"/>' for s in (-1, 1))
    if kind == "sweat":
        return p("M 140 -60 Q 124 -30 140 -22 Q 156 -30 140 -60 Z", fill="#9FD8F5", w=6)
    if kind == "shiver":
        return "".join(p(f"M {s * 200} -40 Q {s * 214} -20 {s * 200} 0 Q {s * 186} 20 {s * 200} 40", w=6)
                       + p(f"M {s * 226} -25 Q {s * 238} -8 {s * 226} 9 Q {s * 214} 26 {s * 226} 43", w=6)
                       for s in (-1, 1))
    return ""


def face(spec):
    fid, _, (oy, iy), ek, mk, ex = spec
    return (f'<g id="{fid}">'
            f'<g id="brows">{brow(-1, oy, iy)}{brow(1, oy, iy)}</g>'
            f'<g id="eyes">{eye(-1, ek)}{eye(1, ek)}</g>'
            f'<g id="mouth">{mouth(mk)}</g>{extras(ex)}</g>')


def head(spec):
    # side-swept fringe (asymmetric, so the head never reads as an acorn)
    hair = ("M -220 -280 L 220 -280 L 220 -150 Q 160 -152 116 -126 L 100 -146 "
            "Q 64 -114 22 -106 L 24 -130 Q -36 -102 -98 -94 L -84 -118 Q -150 -98 -220 -72 Z")
    tuft = ("M -8 -187 Q -12 -224 24 -234 Q 6 -214 14 -189 Z "
            "M 12 -188 Q 24 -214 48 -214 Q 30 -202 30 -185 Z")
    return (f'<g id="head">'
            f'<path id="head-shade" d="{HEAD}" fill="{HEAD_SHADE}"/>'
            f'<g clip-path="url(#headclip)"><path id="head-fill" d="{HEAD}" fill="{WHITE}" transform="translate(-20,-16)"/>'
            f'<path id="hair" d="{hair}" fill="{HAIR}"/>'
            + p("M -112 -170 Q -80 -186 -48 -176", stroke=HAIR_HI, w=7) +
            '</g>'
            + p(tuft, fill=HAIR, w=OL, extra=' id="hair-tuft"')
            + p(HEAD, w=OL, extra=' id="head-outline"')
            + face(spec) + '</g>')


def body_indoor():
    shirt_clip = "M -130 -500 L 130 -500 L 130 -330 Q 0 -318 -130 -330 Z"
    return (f'<g id="body" data-outfit="OUTFIT-RAINKID-INDOOR">'
            f'<g clip-path="url(#torsoclip)">'
            f'<rect x="-130" y="-500" width="260" height="260" fill="{TROUSER}"/>'
            f'<path d="M 60 -500 L 130 -500 L 130 -240 L 82 -240 Z" fill="{TROUSER_SH}"/>'
            f'<path id="shirt" d="{shirt_clip}" fill="{SHIRT}"/>'
            f'<path d="M 58 -500 L 130 -500 L 130 -331 Q 100 -328 74 -326 Z" fill="{SHIRT_SH}"/>'
            + p("M -130 -330 Q 0 -318 130 -330", w=7) +
            '</g>' + p(TORSO, w=OL, extra=' id="torso-outline"') + '</g>')


def arms():
    out = '<g id="arms">'
    for s, name in ((-1, "arm-L"), (1, "arm-R")):
        out += (f'<g id="{name}">' + p(f"M {s * 66} -448 Q {s * 112} -404 {s * 128} -318", w=LIMB)
                + f'<circle cx="{s * 130}" cy="{-308}" r="17" fill="{NAVY}"/></g>')
    return out + '</g>'


def sleeves():
    out = '<g id="sleeves">'
    for s in (-1, 1):
        d = (f"M {s * 64} -474 Q {s * 104} -466 {s * 116} -416 L {s * 86} -400 "
             f"Q {s * 80} -430 {s * 66} -436 Z")
        out += p(d, fill=SHIRT if s < 0 else SHIRT_SH, w=OL - 2)
    return out + '</g>'


def legs():
    out = '<g id="legs">'
    for s in (-1, 1):
        out += p(f"M {s * 42} -270 L {s * 46} -40", w=LIMB)
    # trouser legs (indoor outfit): tapered tubes so the hip block reads as trousers, not a skirt
    out += '</g><g id="trouser-legs" data-outfit="OUTFIT-RAINKID-INDOOR">'
    for s in (-1, 1):
        d = (f"M {s * 8} -290 L {s * 76} -290 L {s * 66} -96 Q {s * 44} -86 {s * 24} -96 Z")
        out += p(d, fill=TROUSER if s < 0 else TROUSER_SH, w=OL - 1)
    out += '</g><g id="feet" data-outfit="OUTFIT-RAINKID-INDOOR">'
    for s in (-1, 1):
        out += (f'<ellipse cx="{s * 60}" cy="-24" rx="40" ry="24" fill="{SOCK}" stroke="{NAVY}" stroke-width="{OL - 1}"/>'
                + p(f"M {s * 60 + 28 * s} -16 Q {s * 60} -2 {s * 60 - 30 * s} -10", stroke=SOCK_SH, w=6))
    return out + '</g>'


def character(spec, x, y, scale=1.0, gid="CHAR-RAINKID-front"):
    return (f'<g id="{gid}" transform="translate({x},{y}) scale({scale})">'
            f'<ellipse id="contact-shadow" cx="0" cy="2" rx="150" ry="20" fill="url(#cshadow)"/>'
            f'<g filter="url(#wobble)">{legs()}{arms()}{body_indoor()}{sleeves()}'
            f'<g transform="translate(0,{HEAD_Y})">{head(spec)}</g></g></g>')


def text(x, y, s, size=22, anchor="start", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{NAVY}" text-anchor="{anchor}">{s}</text>')


def defs():
    return DEFS.replace("{HEAD}", HEAD).replace("{TORSO}", TORSO)


def master():
    swatches = [("head", WHITE), ("head shade", HEAD_SHADE), ("hair", HAIR), ("line / limbs", NAVY),
                ("shirt", SHIRT), ("trousers", TROUSER), ("socks", SOCK), ("tongue", CORAL), ("blush", BLUSH)]
    sw = "".join(f'<rect x="900" y="{560 + i * 40}" width="30" height="30" rx="6" fill="{c}" stroke="{NAVY}" stroke-width="3"/>'
                 + text(945, 583 + i * 40, f"{n} {c}", 20) for i, (n, c) in enumerate(swatches))
    small = character(FACES[0], 1010, 470, 150 / 840, gid="readability-150px")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1000" width="1500" height="1000">{defs()}'
            f'<rect id="preview-backdrop" width="1500" height="1000" fill="#F3EEE4"/>'
            + character(FACES[0], 420, 950)
            + text(900, 90, "CHAR-RAINKID master v001 (DRAFT)", 30, weight="bold")
            + text(900, 125, "Front view, indoor outfit, face: curious", 22)
            + text(900, 158, "Spec v2, approved 2026-11-10", 22)
            + text(900, 250, "Readability test: 150 px tall", 22)
            + f'<rect x="900" y="270" width="220" height="230" fill="#DDE7F0" stroke="{NAVY}" stroke-width="2"/>'
            + small + sw + '</svg>')


def faces():
    cells = [(200, 330), (550, 330), (900, 330), (1250, 330), (375, 790), (725, 790), (1075, 790)]
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1000" width="1500" height="1000">{defs()}'
           f'<rect id="preview-backdrop" width="1500" height="1000" fill="#F3EEE4"/>'
           + text(40, 60, "CHAR-RAINKID face sheet v001 (DRAFT): seven swappable faces", 30, weight="bold"))
    for (x, y), spec in zip(cells, FACES):
        out += (f'<g id="sheet-{spec[0]}" transform="translate({x},{y - 30}) scale(0.82)">'
                f'<g filter="url(#wobble)">{head(spec)}</g></g>'
                + text(x, y + 175, f"{FACES.index(spec) + 1}. {spec[1]}", 24, "middle", "bold"))
    return out + '</svg>'


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, svg in (("CHAR-RAINKID-master-v001.svg", master()), ("CHAR-RAINKID-faces-v001.svg", faces())):
        # mouth clip ids must be unique per sheet: number them
        n = 0
        while 'id="mclip"' in svg:
            n += 1
            svg = svg.replace('id="mclip"', f'id="mclip{n}"', 1).replace('url(#mclip)', f'url(#mclip{n})', 1)
        open(os.path.join(out, name), "w").write(svg)
        print(name)


if __name__ == "__main__":
    main()
