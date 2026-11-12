"""Render one scene in parallel Blender jobs, then check and finish it (see 01_SPECS/render-pipeline-notes.md).

usage: python3 -I renderer-blender/scripts/render_scene.py S10 1140 1401 [--jobs 3] [--scale 100] [--ep 004]
       (run from the repo root; START is inclusive, END exclusive, both on the storyboard v2 clock)

Jobs are started from Python with each number as its own argument (no shell word splitting), each job's log
must start at its own first frame, and the scene is only finished when no frame is missing and no log has a Traceback.
"""
import os, re, subprocess, sys, time

args = sys.argv[1:]
opt = lambda k, d: args[args.index(k) + 1] if k in args else d
scene, start, end = args[0], int(args[1]), int(args[2])
jobs, scale, ep = int(opt("--jobs", 3)), int(opt("--scale", 100)), opt("--ep", "004")
frames_dir, out_dir, logs = f"renders/ep{ep}/frames-v2", f"renders/ep{ep}-v2", f"renders/ep{ep}"
cuts = [start + round(i * (end - start) / jobs) for i in range(jobs + 1)]
t0 = time.time()
procs = []
for i in range(jobs):
    a, b = cuts[i], cuts[i + 1]
    log = open(os.path.join(logs, f"{scene.lower()}-{a}-{b}.log"), "w")
    cmd = ["blender", "-b", "-P", f"renderer-blender/ep{ep}_render.py", "--", frames_dir, str(scale), str(a), str(b)]
    procs.append((subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT), log.name, a))
    print("started", " ".join(cmd), flush=True)
for p, name, a in procs:
    p.wait()
    txt = open(name).read()
    first = re.search(r"^FRAME (\d+)", txt, re.M)
    if not first or int(first.group(1)) != a:
        sys.exit(f"{name}: first frame is {first and first.group(1)}, expected {a}; stopping")
    if "Traceback" in txt:
        sys.exit(f"{name}: Traceback in log; stopping")
missing = [f for f in range(start, end) if not os.path.exists(os.path.join(frames_dir, f"f_{f:04d}.png"))]
print(f"rendered {end - start} frames in {(time.time() - t0) / 60:.1f} min; missing {missing}", flush=True)
if missing:
    sys.exit(1)
subprocess.run([sys.executable, "-I", f"renderer-blender/scripts/finish_ep{ep}.py", frames_dir, out_dir, scene], check=True)
clip = os.path.join(out_dir, "scenes", f"EP{ep}-{scene}.mp4")
print(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                      "stream=duration,nb_read_frames", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip(), clip)
