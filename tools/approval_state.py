#!/usr/bin/env python3
"""Record explicit creator approvals and invalidate stale downstream gates."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

GATES = ["idea", "script", "storyboard", "animationPreview"]
FILES = {
    "idea": ["idea.md"],
    "script": ["research.md", "script.md"],
    "storyboard": ["storyboard.md", "episode.json"],
    "animationPreview": ["animation-preview.mp4"],
}
DEPS = {"idea": [], "script": ["idea"], "storyboard": ["script"], "animationPreview": ["storyboard"]}

def now(): return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
def gate_hash(folder, gate):
    parts=[]
    for rel in FILES[gate]:
        p=folder/rel
        if not p.is_file(): return None
        parts.append(rel.encode()+b"\0"+hashlib.sha256(p.read_bytes()).digest())
    return hashlib.sha256(b"\0".join(parts)).hexdigest()
def load(folder):
    p=folder/"status.json"
    state=json.loads(p.read_text(encoding="utf-8"))
    state.setdefault("approvals", {})
    for gate in GATES:
        state["approvals"].setdefault(gate, {"status":"pending" if gate=="idea" else "blocked"})
    return state,p
def save(state,path):
    path.write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8")
def sync(folder, persist=True):
    state,path=load(folder); approvals=state["approvals"]; events=[]; dirty=False
    for gate in GATES:
        rec=approvals[gate]; current=gate_hash(folder,gate)
        if rec.get("status")=="approved":
            if current is None or current != rec.get("contentHash"):
                rec["status"]="invalidated"; rec["invalidatedAt"]=now(); rec["invalidationReason"]="Approved artifact files changed or are missing."; events.append(f"{gate} approval invalidated: artifact content changed")
            else:
                actual_deps={d:approvals[d].get("contentHash") for d in DEPS[gate]}
                if any(approvals[d].get("status")!="approved" for d in DEPS[gate]) or actual_deps != rec.get("dependencyHashes",{}):
                    rec["status"]="invalidated"; rec["invalidatedAt"]=now(); rec["invalidationReason"]="An upstream approved artifact changed or is no longer approved."; events.append(f"{gate} approval invalidated: upstream approval changed")
        if rec.get("status") not in ("approved","invalidated"):
            if gate!="idea" and any(approvals[d].get("status")!="approved" for d in DEPS[gate]): rec["status"]="blocked"
            elif current is None: rec["status"]="pending"
            elif rec.get("status")=="blocked": rec["status"]="pending"
        if rec.get("artifactFiles") != FILES[gate] or rec.get("currentContentHash") != current: dirty=True
        rec["artifactFiles"]=FILES[gate]
        rec["currentContentHash"]=current
    if events:
        state.setdefault("history",[]).extend({"at":now(),"event":e} for e in events)
    if persist and (events or dirty): save(state,path)
    return state,events

def cmd_sync(args):
    folder=Path(args.episode_dir); state,events=sync(folder)
    if events:
        print("\n".join(events))
    else: print("Approval state is current; no stale approvals found.")
    for gate in GATES: print(f"{gate}: {state['approvals'][gate].get('status')}")

def cmd_record(args):
    folder=Path(args.episode_dir)
    state,_=sync(folder)
    gate=args.gate; rec=state["approvals"][gate]
    if args.confirm != f"I approve {gate} {args.artifact_version}":
        raise SystemExit(f"Confirmation must exactly equal: I approve {gate} {args.artifact_version}")
    if any(state["approvals"][d].get("status")!="approved" for d in DEPS[gate]):
        raise SystemExit(f"Cannot approve {gate}: prerequisite approvals are not current.")
    digest=gate_hash(folder,gate)
    if digest is None: raise SystemExit(f"Cannot approve {gate}: required artifact file(s) missing: {', '.join(FILES[gate])}")
    rec.update({"status":"approved","version":args.artifact_version,"approvedBy":args.approved_by,"approvedAt":now(),"artifactFiles":FILES[gate],"contentHash":digest,"dependencyHashes":{d:state['approvals'][d].get('contentHash') for d in DEPS[gate]},"approvalText":args.confirm})
    rec.pop("invalidatedAt",None); rec.pop("invalidationReason",None)
    state.setdefault("history",[]).append({"at":rec["approvedAt"],"event":f"{gate} approved","version":args.artifact_version,"contentHash":digest,"approvedBy":args.approved_by})
    _,path=load(folder); save(state,path)
    print(f"Recorded explicit {gate} approval for {args.artifact_version} ({digest[:12]}…).")
    print("Run sync before resuming episode work; changed content invalidates this and dependent approvals.")

def main():
    parser=argparse.ArgumentParser(description=__doc__); sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("sync",help="recheck stored hashes and invalidate stale approvals"); p.add_argument("episode_dir"); p.set_defaults(func=cmd_sync)
    p=sub.add_parser("record",help="record a creator's explicit approval after the decision is made"); p.add_argument("episode_dir"); p.add_argument("--gate",choices=GATES,required=True); p.add_argument("--artifact-version",required=True); p.add_argument("--approved-by",required=True); p.add_argument("--confirm",required=True,help='must exactly read: I approve <gate> <version>'); p.set_defaults(func=cmd_record)
    a=parser.parse_args(); a.func(a)
if __name__=="__main__": main()
