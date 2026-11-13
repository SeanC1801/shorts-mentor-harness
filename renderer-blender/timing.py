"""The one timing file. Reads an episode's timings (EPISODES/<ID>/episode.json, or a small JSON of the same shape)
for the renderer, the finish step and the scene launcher. No Blender needed.

A shot may list `views` (viewId, startFrame, endFrame, join); a shot without them is one view, "V1".
View keys are "<shotId>-<viewId>", for example "S03-V2".
"""
import glob, json, os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load(path):
    path = path if os.path.isabs(path) else os.path.join(REPO, path)
    d = json.load(open(path))
    root = os.path.dirname(path)
    shots, views = [], []
    for s in d["shots"]:
        vs = s.get("views") or [dict(viewId="V1", startFrame=s["startFrame"], endFrame=s["endFrame"], join="cut")]
        at = s["startFrame"]
        for v in vs:
            if v["startFrame"] != at or v["endFrame"] <= v["startFrame"]:
                raise SystemExit(f"timing: {s['shotId']}-{v['viewId']} does not follow the previous view (expected start {at})")
            at = v["endFrame"]
            views.append(dict(key=f"{s['shotId']}-{v['viewId']}", shot=s["shotId"], start=v["startFrame"], end=v["endFrame"], join=v.get("join", "cut")))
        if at != s["endFrame"]:
            raise SystemExit(f"timing: views of {s['shotId']} end at {at}, the shot ends at {s['endFrame']}")
        shots.append(dict(id=s["shotId"], start=s["startFrame"], end=s["endFrame"]))
    total = d.get("totalFrames", shots[-1]["end"])
    if shots[0]["start"] != 0 or shots[-1]["end"] != total or any(a["end"] != b["start"] for a, b in zip(shots, shots[1:])):
        raise SystemExit("timing: shots must run from frame 0 to totalFrames with no gaps")
    audio = (d.get("narration") or {}).get("sourceFile")
    audio = os.path.join(root, audio) if audio and os.path.exists(os.path.join(root, audio)) else None
    words = []
    wt = sorted(glob.glob(os.path.join(root, "audio", "word-timings*.json")))
    if wt:
        W = json.load(open(wt[-1]))["sentences"]
        fps = d.get("fps", 30)
        for k in sorted(W, key=lambda x: int(x[1:])):
            words += [(round(w["startMs"] * fps / 1000), w["text"]) for w in W[k]]
    return dict(id=d.get("episodeId", "EP"), fps=d.get("fps", 30), total=total, shots=shots, views=views, audio=audio, words=words,
                finish=dict(dict(fadeIn=False, fadeOut=False, captions=bool(words), captionPx=60), **d.get("finish", {})), path=path)


def shot(T, shot_id):
    for s in T["shots"]:
        if s["id"] == shot_id:
            return s
    raise SystemExit(f"timing: no shot {shot_id!r}; shots are {[s['id'] for s in T['shots']]}")


def view_at(T, f):
    for v in T["views"]:
        if v["start"] <= f < v["end"]:
            return v
    raise SystemExit(f"timing: frame {f} is outside 0..{T['total'] - 1}")
