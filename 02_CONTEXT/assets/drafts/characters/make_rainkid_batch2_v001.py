"""Draw CHAR-RAINKID art batch 2 (seven poses, four outfits) on the approved batch 1 rig.

Spec: EPISODES/EP004/character-specs.md v2. Reuses head, faces, line weights and colours
from make_rainkid_v001.py (approved batch 1) without changing them.
usage: python3 -I make_rainkid_batch2_v001.py OUT_DIR
Writes CHAR-RAINKID-poses-v001.svg and CHAR-RAINKID-outfits-v001.svg (drafts).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_rainkid_v001 as k  # approved batch 1 parts
from make_rainkid_v001 import p, NAVY, WHITE, OL, LIMB, HEAD, HEAD_Y, TORSO, HEAD_SHADE, HAIR

FACE = {f[0].split("-")[-1].lower(): f for f in k.FACES}  # curious, deadpan, shocked, worried, squint, shiver, wistful

# ---------- outfit colours (spec v2; shade bands about 15% darker) ----------
C = dict(
    shirt=("#6FB7E8", "#5E9CC6"), trousers=("#7A7F8C", "#686C77"), socks=("#C9CCDA", "#ABAEBA"),
    coat=("#FFC83D", "#E8A92A"), boots=("#3A6FD8", "#2C55A8"),
    tee=("#FFE27A", "#E8C95E"), shorts=("#F08A3C", "#D07430"), cap=("#D9483B", "#B83A30"), sandal=("#8A5A3A", "#6E472D"),
    jacket=("#3B4A7A", "#2F3B62"), red=("#D9483B", "#B83A30"), darktrousers=("#4A4E5A", "#3E414B"), shoes=("#3A3F4C", "#2E323C"),
)
COAT = "M -80 -474 Q 0 -486 80 -474 L 122 -228 Q 124 -210 104 -210 L -104 -210 Q -124 -210 -122 -228 Z"
JACKET = "M -90 -476 Q 0 -490 90 -476 L 120 -272 Q 122 -250 100 -250 L -100 -250 Q -122 -250 -120 -272 Z"
EXTRA_DEFS = (f'<clipPath id="coatclip"><path d="{COAT}"/></clipPath>'
              f'<clipPath id="jacketclip"><path d="{JACKET}"/></clipPath>')

SH = (-66, -448)  # left shoulder; right is mirrored

# ---------- poses: per arm (control point, hand point, hand shape), drawn in front of the body or behind ----------
POSES = {
    "POSE-RAINKID-WINDOW": dict(arms=[((-122, -372), (-56, -372), "nub"), ((122, -372), (56, -372), "nub")], front=True),
    "POSE-RAINKID-POINT-UP": dict(arms=[((-112, -404), (-128, -318), "nub"), ((178, -520), (222, -716), "point")], front=False),
    "POSE-RAINKID-SHOCK": dict(arms=[((-150, -462), (-226, -566), "nub"), ((150, -462), (226, -566), "nub")], front=False, legs="wide"),
    "POSE-RAINKID-SHIELD": dict(arms=[((-112, -404), (-128, -318), "nub"), ((330, -640), (150, -716), "flat")], front=True),
    "POSE-RAINKID-SHIVER": dict(arms=[((-10, -340), (62, -394), "nub"), ((10, -360), (-62, -414), "nub")], front=True, legs="knock"),
    "POSE-RAINKID-SHORE": dict(arms=[((-112, -404), (-128, -318), "nub"), ((112, -404), (128, -318), "nub")], front=False, back=True),
    "POSE-RAINKID-FAN": dict(arms=[((-112, -404), (-128, -318), "nub"), ((170, -430), (206, -640), "nub")], front=False, fan=True),
}


def arm_path(side, ctrl, hand):
    return f"M {side * -SH[0]} {SH[1]} Q {ctrl[0]} {ctrl[1]} {hand[0]} {hand[1]}"


def hand_shape(hand, kind):
    x, y = hand
    if kind == "point":
        return (f'<circle cx="{x}" cy="{y}" r="17" fill="{NAVY}"/>'
                + p(f"M {x} {y - 10} L {x + 6} {y - 40}", w=12))
    if kind == "flat":
        return f'<ellipse cx="{x - 20}" cy="{y}" rx="52" ry="15" fill="{NAVY}" transform="rotate(-8 {x} {y})"/>'
    return f'<circle cx="{x}" cy="{y}" r="17" fill="{NAVY}"/>'


def arms(pose, sleeve=None):
    """sleeve: None (short sleeves / bare), or (fill, shade, width) for long sleeves following the arm."""
    out = '<g id="arms">'
    for (ctrl, hand, kind), side, name in zip(POSES[pose]["arms"], (-1, 1), ("arm-L", "arm-R")):
        d = arm_path(side, ctrl, hand)
        out += f'<g id="{name}">'
        if sleeve:
            fill, shade, w = sleeve
            out += p(d, w=w + 12) + p(d, stroke=fill if side < 0 else shade, w=w)
        else:
            out += p(d, w=LIMB)
        out += hand_shape(hand, kind) + '</g>'
    return out + '</g>'


def short_sleeves(fill, shade):
    out = '<g id="sleeves">'
    for s in (-1, 1):
        d = (f"M {s * 64} -474 Q {s * 104} -466 {s * 116} -416 L {s * 86} -400 "
             f"Q {s * 80} -430 {s * 66} -436 Z")
        out += p(d, fill=fill if s < 0 else shade, w=OL - 2)
    return out + '</g>'


def legs(pose, top=-270, bottom=-40):
    style = POSES[pose].get("legs")
    out = '<g id="legs">'
    for s in (-1, 1):
        foot_x = s * (70 if style == "wide" else 46)
        if style == "knock":
            out += p(f"M {s * 42} {top} Q {s * 20} {(top + bottom) / 2} {s * 46} {bottom}", w=LIMB)
        else:
            out += p(f"M {s * 42} {top} L {foot_x} {bottom}", w=LIMB)
    return out + '</g>'


def foot_x(pose, s):
    return s * (84 if POSES[pose].get("legs") == "wide" else 60)


# ---------- outfits ----------
def torso_block(clip, shape, fill, shade, extra=""):
    return (f'<g clip-path="url(#{clip})"><rect x="-140" y="-500" width="280" height="300" fill="{fill}"/>'
            f'<path d="M 62 -500 L 140 -500 L 140 -200 L 86 -200 Z" fill="{shade}"/>{extra}</g>'
            + p(shape, w=OL))


def outfit_indoor(pose):
    body = k.body_indoor()
    trouser = '<g id="trouser-legs">'
    for s in (-1, 1):
        d = f"M {s * 8} -290 L {s * 76} -290 L {s * 66} -96 Q {s * 44} -86 {s * 24} -96 Z"
        trouser += p(d, fill=C["trousers"][0] if s < 0 else C["trousers"][1], w=OL - 1)
    trouser += '</g>'
    feet = '<g id="feet">' + "".join(
        f'<ellipse cx="{foot_x(pose, s)}" cy="-24" rx="40" ry="24" fill="{C["socks"][0]}" stroke="{NAVY}" stroke-width="{OL - 1}"/>'
        for s in (-1, 1)) + '</g>'
    return dict(under=legs(pose) + trouser + feet, body=body, top=short_sleeves(*C["shirt"]), sleeve=None, hat="")


def outfit_rain(pose, back=False):
    fill, shade = C["coat"]
    extra = "" if back else (p("M 0 -470 L 0 -212", w=6) + "".join(
        f'<circle cx="16" cy="{y}" r="9" fill="#FFF4E2" stroke="{NAVY}" stroke-width="5"/>' for y in (-420, -350, -280)))
    body = '<g id="body" data-outfit="OUTFIT-RAINKID-RAIN">' + torso_block("coatclip", COAT, fill, shade, extra) + '</g>'
    boots = '<g id="boots">'
    for s in (-1, 1):
        x = foot_x(pose, s) - s * 14
        d = (f"M {x - 30} -134 L {x + 30} -134 L {x + 32} -22 Q {x + 32} 0 {x + 8} 0 "
             f"L {x - 38} 0 Q {x - 52} 0 {x - 50} -16 Q {x - 48} -30 {x - 30} -34 Z") if s < 0 else \
            (f"M {x + 30} -134 L {x - 30} -134 L {x - 32} -22 Q {x - 32} 0 {x - 8} 0 "
             f"L {x + 38} 0 Q {x + 52} 0 {x + 50} -16 Q {x + 48} -30 {x + 30} -34 Z")
        boots += p(d, fill=C["boots"][0], w=OL - 1) + p(f"M {x - 40} -12 L {x + 40} -12", stroke=C["boots"][1], w=8)
    boots += '</g>'
    hood = p("M -74 -478 Q 0 -506 74 -478 Q 84 -420 0 -398 Q -84 -420 -74 -478 Z", fill=shade, w=OL - 1) if back else \
        f'<ellipse cx="0" cy="-470" rx="96" ry="28" fill="{shade}" stroke="{NAVY}" stroke-width="{OL - 1}"/>'
    return dict(under=legs(pose, -214, -120) + boots, body=body, top="", collar=hood, sleeve=(fill, shade, 22), hat="")


def outfit_sun(pose):
    tf, ts = C["tee"]
    shirt_clip = "M -130 -500 L 130 -500 L 130 -330 Q 0 -318 -130 -330 Z"
    body = ('<g id="body" data-outfit="OUTFIT-RAINKID-SUN"><g clip-path="url(#torsoclip)">'
            f'<rect x="-130" y="-500" width="260" height="260" fill="{C["shorts"][0]}"/>'
            f'<path d="M 60 -500 L 130 -500 L 130 -240 L 82 -240 Z" fill="{C["shorts"][1]}"/>'
            f'<path d="{shirt_clip}" fill="{tf}"/><path d="M 58 -500 L 130 -500 L 130 -331 Q 100 -328 74 -326 Z" fill="{ts}"/>'
            + p("M -130 -330 Q 0 -318 130 -330", w=7) + '</g>' + p(TORSO, w=OL) + '</g>')
    shorts = '<g id="short-legs">'
    for s in (-1, 1):
        d = f"M {s * 8} -290 L {s * 80} -290 L {s * 74} -206 Q {s * 46} -196 {s * 20} -206 Z"
        shorts += p(d, fill=C["shorts"][0] if s < 0 else C["shorts"][1], w=OL - 1)
    shorts += '</g>'
    sandals = '<g id="sandals">'
    for s in (-1, 1):
        x = foot_x(pose, s)
        sandals += (f'<ellipse cx="{x}" cy="-8" rx="42" ry="12" fill="{C["sandal"][0]}" stroke="{NAVY}" stroke-width="{OL - 2}"/>'
                    + p(f"M {x - 22} -12 Q {x} -40 {x + 22} -12", stroke=C["sandal"][1], w=10))
    sandals += '</g>'
    cf, cs = C["cap"]
    cap = ('<g id="cap">'
           + p("M -150 -110 Q -150 -205 0 -205 Q 150 -205 150 -110 Q 0 -128 -150 -110 Z", fill=cf, w=OL)
           + p("M 40 -200 Q 120 -190 148 -112 Q 100 -122 70 -120 Z", fill=cs, w=0)
           + p("M -160 -112 Q 0 -140 200 -100 Q 210 -84 190 -80 Q 0 -112 -156 -96 Q -170 -100 -160 -112 Z", fill=cs, w=OL - 1)
           + f'<circle cx="0" cy="-204" r="10" fill="{cf}" stroke="{NAVY}" stroke-width="5"/></g>')
    return dict(under=legs(pose, -210, -14) + shorts + sandals, body=body, top=short_sleeves(tf, ts), sleeve=None, hat=cap)


def outfit_night(pose):
    jf, js = C["jacket"]
    quilt = "".join(p(f"M -130 {y} Q 0 {y + 10} 130 {y}", stroke="#55669A", w=5) for y in (-420, -360, -300))
    body = ('<g id="body" data-outfit="OUTFIT-RAINKID-NIGHT">' + torso_block("jacketclip", JACKET, jf, js, quilt)
            + p("M 0 -470 L 0 -252", stroke="#55669A", w=5) + '</g>')
    rf, rs = C["red"]
    scarf = (f'<g id="scarf"><ellipse cx="0" cy="-468" rx="88" ry="26" fill="{rf}" stroke="{NAVY}" stroke-width="{OL - 1}"/>'
             + p("M 22 -458 L 58 -458 L 64 -352 L 30 -352 Z", fill=rs, w=OL - 2)
             + p("M 32 -360 L 34 -340 M 46 -360 L 48 -340 M 60 -360 L 62 -340", w=4) + '</g>')
    trouser = '<g id="trouser-legs">'
    for s in (-1, 1):
        d = f"M {s * 8} -270 L {s * 78} -270 L {s * 68} -70 Q {s * 44} -60 {s * 22} -70 Z"
        trouser += p(d, fill=C["darktrousers"][0] if s < 0 else C["darktrousers"][1], w=OL - 1)
    trouser += '</g>'
    feet = '<g id="shoes">' + "".join(
        f'<ellipse cx="{foot_x(pose, s)}" cy="-24" rx="44" ry="26" fill="{C["shoes"][0]}" stroke="{NAVY}" stroke-width="{OL - 1}"/>'
        for s in (-1, 1)) + '</g>'
    beanie = ('<g id="beanie">'
              + p("M -158 -96 Q -170 -230 0 -232 Q 170 -230 158 -96 Z", fill=rf, w=OL)
              + p("M -164 -132 Q 0 -150 164 -132 L 162 -92 Q 0 -110 -162 -92 Z", fill=rs, w=OL - 1)
              + "".join(p(f"M {x} -128 L {x} -100", stroke="#9C2F27", w=5) for x in range(-120, 140, 40))
              + f'<circle cx="0" cy="-238" r="26" fill="#F07466" stroke="{NAVY}" stroke-width="{OL - 2}"/></g>')
    return dict(under=legs(pose, -250, -50) + trouser + feet, body=body, top="", collar=scarf,
                sleeve=(jf, js, 30), hat=beanie)


OUTFITS = {"OUTFIT-RAINKID-INDOOR": outfit_indoor, "OUTFIT-RAINKID-RAIN": outfit_rain,
           "OUTFIT-RAINKID-SUN": outfit_sun, "OUTFIT-RAINKID-NIGHT": outfit_night}


# ---------- head (front from batch 1; back view new) ----------
def head_front(face, hat):
    h = k.head(face)
    if hat:  # a hat hides the hair tuft
        import re
        h = re.sub(r'<path [^>]*id="hair-tuft"/>', '', h)
    return h[:-4] + hat + '</g>'  # hat goes inside the head group, over the face


def head_back(hat):
    hair = ("M -220 -280 L 220 -280 L 220 30 Q 150 62 108 40 Q 70 72 30 46 Q 0 72 -30 46 "
            "Q -70 72 -108 40 Q -150 62 -220 30 Z")
    tuft = "M 8 -187 Q 12 -224 -24 -234 Q -6 -214 -14 -189 Z M -12 -188 Q -24 -214 -48 -214 Q -30 -202 -30 -185 Z"
    return ('<g id="head-back">'
            f'<path d="{HEAD}" fill="{HEAD_SHADE}"/>'
            f'<g clip-path="url(#headclip)"><path d="{HEAD}" fill="{WHITE}" transform="translate(20,-16)"/>'
            f'<path id="hair-back" d="{hair}" fill="{HAIR}"/></g>'
            + p(tuft, fill=HAIR) + p(HEAD, w=OL) + hat + '</g>')


def figure(pose, outfit, face_key, x, y, scale, label=None):
    P = POSES[pose]
    back = P.get("back", False)
    o = OUTFITS[outfit](pose, back) if outfit == "OUTFIT-RAINKID-RAIN" else OUTFITS[outfit](pose)
    arm_svg = arms(pose, o["sleeve"])
    head = head_back(o["hat"]) if back else head_front(FACE[face_key], o["hat"])
    fan = ""
    if P.get("fan"):
        hx, hy = P["arms"][1][1]
        fan = "".join(p(f"M {hx + 30 + i * 16} {hy - 30 + i * 22} Q {hx + 44 + i * 16} {hy - 10 + i * 22} {hx + 30 + i * 16} {hy + 10 + i * 22}", w=6)
                      for i in range(3))
    layers = (o["under"] + ("" if P["front"] else arm_svg) + o["body"] + o.get("top", "") + o.get("collar", "")
              + f'<g transform="translate(0,{HEAD_Y})">{head}</g>' + (arm_svg if P["front"] else "") + fan)
    gid = f"{pose}" if label is None else label
    return (f'<g id="{gid}" data-outfit="{outfit}" data-face="{"none (back view)" if back else FACE[face_key][0]}" '
            f'transform="translate({x},{y}) scale({scale})">'
            f'<ellipse cx="0" cy="2" rx="150" ry="20" fill="url(#cshadow)"/>'
            f'<g filter="url(#wobble)">{layers}</g></g>')


def defs():
    return k.defs().replace("</defs>", EXTRA_DEFS + "</defs>")


# pose -> (outfit, face) where it appears in the story
CAST = [
    ("POSE-RAINKID-WINDOW", "OUTFIT-RAINKID-INDOOR", "curious", "window (indoor)"),
    ("POSE-RAINKID-SHORE", "OUTFIT-RAINKID-RAIN", "deadpan", "shore, back view (rain)"),
    ("POSE-RAINKID-SHOCK", "OUTFIT-RAINKID-RAIN", "shocked", "shock (rain)"),
    ("POSE-RAINKID-POINT-UP", "OUTFIT-RAINKID-RAIN", "worried", "point up (rain)"),
    ("POSE-RAINKID-SHIELD", "OUTFIT-RAINKID-SUN", "squint", "shield eyes (sun)"),
    ("POSE-RAINKID-FAN", "OUTFIT-RAINKID-SUN", "deadpan", "fan self (sun)"),
    ("POSE-RAINKID-SHIVER", "OUTFIT-RAINKID-NIGHT", "shiver", "shiver (night)"),
]


def poses_sheet():
    cells = [(200, 560), (560, 560), (940, 560), (1300, 560), (380, 1110), (760, 1110), (1140, 1110)]
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1150" width="1500" height="1150">{defs()}'
           f'<rect id="preview-backdrop" width="1500" height="1150" fill="#F3EEE4"/>'
           + k.text(40, 50, "CHAR-RAINKID poses v001 (DRAFT): each pose in the outfit where it appears", 28, weight="bold"))
    for (x, y), (pose, outfit, face, label) in zip(cells, CAST):
        out += figure(pose, outfit, face, x, y - 40, 0.48) + k.text(x, y - 8, f"{label}", 20, "middle", "bold")
    return out + '</svg>'


def outfits_sheet():
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 640" width="1500" height="640">{defs()}'
           f'<rect id="preview-backdrop" width="1500" height="640" fill="#F3EEE4"/>'
           + k.text(40, 50, "CHAR-RAINKID outfits v001 (DRAFT): same body, clothes fit the environment", 28, weight="bold"))
    labels = {"OUTFIT-RAINKID-INDOOR": "indoor", "OUTFIT-RAINKID-RAIN": "shore (drizzle)",
              "OUTFIT-RAINKID-SUN": "harsh sun", "OUTFIT-RAINKID-NIGHT": "cold night"}
    for i, outfit in enumerate(OUTFITS):
        x = 220 + i * 355
        POSES["_STAND"] = dict(arms=[((-112, -404), (-128, -318), "nub"), ((112, -404), (128, -318), "nub")], front=False)
        out += figure("_STAND", outfit, "curious", x, 580, 0.58, label=outfit) + k.text(x, 625, labels[outfit], 22, "middle", "bold")
    return out + '</svg>'


def main():
    out = sys.argv[1]
    for name, svg in (("CHAR-RAINKID-poses-v001.svg", poses_sheet()), ("CHAR-RAINKID-outfits-v001.svg", outfits_sheet())):
        n = 0
        while 'id="mclip"' in svg:
            n += 1
            svg = svg.replace('id="mclip"', f'id="mclip{n}"', 1).replace('url(#mclip)', f'url(#mclip{n})', 1)
        open(os.path.join(out, name), "w").write(svg)
        print(name)


if __name__ == "__main__":
    main()
