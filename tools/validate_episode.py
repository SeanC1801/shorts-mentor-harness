#!/usr/bin/env python3
"""Dependency-free structural and cross-field validator for an episode packet."""
import json
import sys
from pathlib import Path


def fail(msg):
    print(f"ERROR: {msg}")
    return False


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def schema_errors(value, schema, path="$" ):
    errors=[]
    typ=schema.get("type")
    checks={"object":lambda v:isinstance(v,dict),"array":lambda v:isinstance(v,list),"string":lambda v:isinstance(v,str),"integer":lambda v:isinstance(v,int) and not isinstance(v,bool),"number":lambda v:isinstance(v,(int,float)) and not isinstance(v,bool),"boolean":lambda v:isinstance(v,bool)}
    if typ and not checks[typ](value): return [f"{path}: expected {typ}"]
    if "const" in schema and value != schema["const"]: errors.append(f"{path}: expected {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]: errors.append(f"{path}: expected one of {schema['enum']!r}")
    if isinstance(value,str):
        if len(value)<schema.get("minLength",0): errors.append(f"{path}: string is too short")
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        if value<schema.get("minimum",float("-inf")): errors.append(f"{path}: below minimum")
        if value>schema.get("maximum",float("inf")): errors.append(f"{path}: above maximum")
    if isinstance(value,list):
        if len(value)<schema.get("minItems",0): errors.append(f"{path}: too few items")
        if "items" in schema:
            for i,item in enumerate(value): errors.extend(schema_errors(item,schema["items"],f"{path}[{i}]"))
    if isinstance(value,dict):
        for key in schema.get("required",[]):
            if key not in value: errors.append(f"{path}: missing required field {key}")
        props=schema.get("properties",{})
        if schema.get("additionalProperties") is False:
            for key in value.keys()-props.keys(): errors.append(f"{path}: unexpected field {key}")
        for key,child in props.items():
            if key in value: errors.extend(schema_errors(value[key],child,f"{path}.{key}"))
    return errors

def validate(folder: Path) -> bool:
    path = folder / "episode.json" if folder.is_dir() else folder
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read episode JSON: {exc}")
    schema_path=Path(__file__).parent.parent/"02_CONTEXT/templates/contracts/shot-spec.schema.json"
    try:
        schema=json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read episode schema: {exc}")
    errors = schema_errors(data,schema)
    if errors: return report(errors)
    def need(cond, msg):
        if not cond: errors.append(msg)
    need(isinstance(data, dict), "episode root must be an object")
    if not isinstance(data, dict):
        return False
    for key in ("episodeId", "version", "fps", "width", "height", "narration", "syncToleranceMs", "totalFrames", "shots", "exports"):
        need(key in data, f"missing top-level field: {key}")
    if errors: return report(errors)
    # 30 fps master (24 fps stays valid for episodes made before motion rules v2)
    POSE_FPS = {30: 15, 24: 12}
    need(data["fps"] in POSE_FPS and data["width"] == 1080 and data["height"] == 1920, "master must be 1080x1920 at 30fps (24fps only for episodes made before motion rules v2)")
    fps = data["fps"] if data["fps"] in POSE_FPS else 30
    need(integer(data["totalFrames"]) and data["totalFrames"] > 0, "totalFrames must be a positive integer")
    need(integer(data["syncToleranceMs"]) and 0 <= data["syncToleranceMs"] <= 250, "syncToleranceMs must be an integer from 0 to 250")
    narration = data["narration"]
    need(isinstance(narration, dict), "narration must be an object")
    if not isinstance(narration, dict): return report(errors)
    duration = narration.get("durationMs")
    need(integer(duration) and duration > 0, "narration.durationMs must be a positive integer measured from audio")
    need(narration.get("syncSource") == "measured-audio", "narration.syncSource must be measured-audio")
    shots = data["shots"]
    need(isinstance(shots, list) and len(shots) > 0, "shots must be a non-empty array")
    if not isinstance(shots, list) or not shots: return report(errors)
    expected_frame = 0
    prior_narration_end = 0
    tolerance = data["syncToleranceMs"] if integer(data["syncToleranceMs"]) else 0
    all_ids = []
    for index, shot in enumerate(shots):
        label = f"shots[{index}]"
        if not isinstance(shot, dict):
            errors.append(f"{label} must be an object"); continue
        sid = shot.get("shotId"); all_ids.append(sid)
        start, end = shot.get("startFrame"), shot.get("endFrame")
        need(integer(start) and integer(end) and 0 <= start < end, f"{label} needs integer half-open frame range [startFrame,endFrame)")
        if integer(start) and integer(end):
            need(start == expected_frame, f"{label} must begin at previous shot end (expected {expected_frame})")
            expected_frame = end
            if integer(data["fps"]) and data["fps"] > 0:
                expected_start_ms = round(start * 1000 / data["fps"])
                expected_end_ms = round(end * 1000 / data["fps"])
                ns, ne = shot.get("narrationStartMs"), shot.get("narrationEndMs")
                if integer(ns): need(abs(ns - expected_start_ms) <= tolerance, f"{label} narration start differs from frame boundary beyond tolerance")
                if integer(ne): need(abs(ne - expected_end_ms) <= tolerance, f"{label} narration end differs from frame boundary beyond tolerance")
            for cap in shot.get("captions", []) if isinstance(shot.get("captions", []), list) else []:
                cs, ce = cap.get("startFrame"), cap.get("endFrame")
                need(integer(cs) and integer(ce) and start <= cs < ce <= end, f"{label} caption range must fit within shot")
        ns, ne = shot.get("narrationStartMs"), shot.get("narrationEndMs")
        need(integer(ns) and integer(ne) and 0 <= ns < ne <= duration, f"{label} narration range must fit measured narration duration")
        if integer(ns) and integer(ne):
            need(ns == prior_narration_end, f"{label} narration range must be contiguous with the previous shot")
            prior_narration_end = ne
        cm = shot.get("characterMotion", {})
        held = cm.get("poseFps") == POSE_FPS[fps] and cm.get("exposureFrames") == 2          # motion rules v1-v2: cutout poses held 2 frames
        every = cm.get("poseFps") == fps and cm.get("exposureFrames") == 1                    # motion rules v3: 3D characters move every frame
        need(held or every, f"{label} character motion must be {fps}fps with 1-frame exposure (motion rules v3) or {POSE_FPS[fps]}fps poses exposed for 2 frames (v2)")
        views = shot.get("views")
        if isinstance(views, list) and integer(start) and integer(end):                       # the renderer and finish step read these
            at = start
            for vi, view in enumerate(views):
                vs, ve = view.get("startFrame"), view.get("endFrame")
                need(integer(vs) and integer(ve) and vs == at and vs < ve, f"{label}.views[{vi}] must start where the previous view ended (expected {at}) and have a positive length")
                at = ve if integer(ve) else at
            need(at == end, f"{label}.views must end at the shot's endFrame")
            ids = [view.get("viewId") for view in views]
            need(len(set(ids)) == len(ids), f"{label}.views need unique viewId values")
        need(shot.get("camera", {}).get("fps") == fps, f"{label} camera must use {fps}fps")
        for segment in shot.get("narrationSegments", []) if isinstance(shot.get("narrationSegments", []), list) else []:
            a, b = segment.get("startMs"), segment.get("endMs")
            need(integer(a) and integer(b) and ns <= a < b <= ne, f"{label} narration segment must fit its shot narration range")
        for track in shot.get("audio", []) if isinstance(shot.get("audio", []), list) else []:
            a, b = track.get("startMs"), track.get("endMs")
            need(integer(a) and integer(b) and 0 <= a < b, f"{label} audio cue needs a positive integer millisecond range")
            if integer(b) and integer(data["totalFrames"]):
                video_end_ms=round(data["totalFrames"]*1000/data["fps"])
                need(b <= video_end_ms+tolerance, f"{label} audio cue exceeds video duration plus sync tolerance")
            if track.get("kind") == "narration":
                need(track.get("assetId") == narration.get("assetId"), f"{label} narration cue must reference episode narration asset")
                if integer(b) and integer(duration): need(b <= duration, f"{label} narration cue exceeds measured narration duration")
    need(expected_frame == data["totalFrames"], "last shot must end at totalFrames")
    need(prior_narration_end == duration, "shot narration ranges must end at measured narration duration")
    need(len(set(all_ids)) == len(all_ids), "shotId values must be unique")
    exports = data["exports"]
    need(isinstance(exports, dict) and isinstance(exports.get("preview"), dict), "exports.preview is required")
    scene_exports = exports.get("scenes", []) if isinstance(exports, dict) else []
    need(isinstance(scene_exports, list), "exports.scenes must be an array")
    if isinstance(scene_exports, list):
        exp_ids = [item.get("shotId") for item in scene_exports if isinstance(item, dict)]
        need(sorted(exp_ids) == sorted(all_ids), "exports.scenes must contain exactly one export for each shot")
        names = [item.get("filename") for item in scene_exports if isinstance(item, dict)]
        need(len(names) == len(set(names)), "scene export filenames must be unique")
        for item in scene_exports:
            if isinstance(item, dict):
                need(item.get("format") == "mp4" and item.get("width") == 1080 and item.get("height") == 1920 and item.get("fps") == fps, f"each scene export must be 1080x1920, {fps}fps MP4")
    return report(errors)


def report(errors):
    if errors:
        for e in errors: print(f"ERROR: {e}")
        return False
    print("Episode packet passes structural and cross-field checks. This does not render video.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tools/validate_episode.py EPISODES/<ID>")
        sys.exit(2)
    sys.exit(0 if validate(Path(sys.argv[1])) else 1)
