"""Render one scene of an episode in parallel Blender jobs, check it, finish it and make a contact sheet.

usage: python3 -I renderer-blender/scripts/render_scene.py EPISODE SHOT [--jobs 1] [--scale 100]
       (run from the repo root; EPISODE names a file in renderer-blender/episodes/, SHOT is a shot id such as S03)

The frame range comes from the episode's timing file; nothing is typed by hand. Each number is passed to Blender
as its own argument. The scene is finished only if every job started on its own first frame, no frame is missing and
no log holds a Traceback. A job that runs past twice its expected time is stopped.
Output: renders/<episode>/frames/f_NNNN.png, renders/<episode>/scenes/<ID>-<SHOT>.mp4 and <SHOT>-sheet.png.
(EP003 and EP004 keep their own scripts; this launcher is for episodes made with render_episode.py.)
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import timing

args = sys.argv[1:]
if len(args) < 2:
    sys.exit(__doc__)
opt = lambda k, d: args[args.index(k) + 1] if k in args else d
name, shot_id = args[0], args[1]
jobs, scale = int(opt("--jobs", 1)), int(opt("--scale", 100))     # one job: on this Mac 3 parallel jobs were slower (10.5 vs 8 min per 100 frames)
mod = os.path.join(HERE, "..", "episodes", name + ".py")
m = re.search(r'^TIMING\s*=\s*["\'](.+?)["\']', open(mod).read(), re.M)
if not m:
    sys.exit(f"render_scene: {mod} has no TIMING line")
T = timing.load(m.group(1))
S = timing.shot(T, shot_id)
start, end = S["start"], S["end"]
out = os.path.join("renders", name)
frames_dir = os.path.join(out, "frames")
os.makedirs(os.path.join(out, "logs"), exist_ok=True)
power = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True).stdout
if "Battery Power" in power:
    print("WARNING: the Mac is on battery. Plug it in and keep the lid open, or the render pauses when it sleeps.", flush=True)
jobs = max(1, min(jobs, (end - start) // 10 or 1))
cuts = [start + round(i * (end - start) / jobs) for i in range(jobs + 1)]
per_job = max(b - a for a, b in zip(cuts, cuts[1:]))
expected = 60 + per_job * 6 * jobs          # seconds: about 6 s a frame in one job, slower when jobs share the machine
print(f"{T['id']} {shot_id}: frames {start}-{end - 1} in {jobs} job(s); expected about {expected / 60:.0f} min, stopped at {2 * expected / 60:.0f} min", flush=True)
t0 = time.time()
procs = []
for a, b in zip(cuts, cuts[1:]):
    log = os.path.join(out, "logs", f"{shot_id.lower()}-{a}-{b}.log")
    cmd = ["blender", "-b", "-P", os.path.join("renderer-blender", "render_episode.py"), "--", name, frames_dir, str(scale), str(a), str(b)]
    procs.append((subprocess.Popen(cmd, stdout=open(log, "w"), stderr=subprocess.STDOUT), log, a))
while any(p.poll() is None for p, _, _ in procs):
    if time.time() - t0 > 2 * expected:
        for p, _, _ in procs:
            p.kill()
        sys.exit(f"render_scene: stopped after {(time.time() - t0) / 60:.0f} min (twice the expected time). Read the logs in {out}/logs before trying again.")
    time.sleep(5)
for p, log, a in procs:
    txt = open(log).read()
    first = re.search(r"^FRAME (\d+)", txt, re.M)
    if not first or int(first.group(1)) != a:
        sys.exit(f"{log}: first frame is {first and first.group(1)}, expected {a}; stopping")
    if "Traceback" in txt or p.returncode != 0:
        sys.exit(f"{log}: the job failed; stopping")
missing = [f for f in range(start, end) if not os.path.exists(os.path.join(frames_dir, f"f_{f:04d}.png"))]
print(f"rendered {end - start} frames in {(time.time() - t0) / 60:.1f} min; missing {missing}", flush=True)
if missing:
    sys.exit(1)
subprocess.run([sys.executable, "-I", os.path.join(HERE, "finish_episode.py"), T["path"], frames_dir, out, shot_id], check=True)
clip = os.path.join(out, "scenes", f"{T['id']}-{shot_id}.mp4")
n = max(1, (end - start) // 10)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", f"select='not(mod(n\\,{n}))',scale=216:-1,tile=10x1", "-frames:v", "1",
                os.path.join(out, "scenes", f"{shot_id}-sheet.png")], check=True)
probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=duration,nb_read_frames",
                        "-of", "csv=p=0", clip], capture_output=True, text=True).stdout.strip()
print("CLIP", clip, probe, flush=True)
