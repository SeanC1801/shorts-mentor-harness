# Render pipeline notes (from EP004)

How a scene goes from code to an approved clip, what it costs, what went wrong on EP004, and what to change for the next video.

## The pipeline, per scene

1. **Prepare (code only).** Set code goes in `renderer-blender/ep00N_sets.py`, and the views and events for the scene go in `ep00N_render.py`. New textures and kid cards come from `scripts/paint_textures_ep00N.py`. A no-render dry run (Blender with `render()` replaced by a report) checks framing and timing.
2. **Check stills (optional).** Render a few frames at reduced size, using `--frames a,b,c`.
3. **Full render.**
   - Command: `blender -b -P renderer-blender/ep00N_render.py -- OUT_DIR scale start end`.
   - The scene is split into 3 parallel jobs, each with its own start and end.
   - Each job:
     - builds every stage of the episode (about 3 min before its first frame)
     - for each frame: maps it onto the storyboard clock, picks the view, sets the camera, runs the scene's animation
     - renders 1080×1920 in EEVEE (32 samples, cel shading, Freestyle ink lines) and writes `f_NNNN.png`
4. **Check.** Look for missing frames and `Traceback` in the logs.
5. **Finish (seconds).**
   - `python3 -I renderer-blender/scripts/finish_ep00N.py FRAMES OUT S0N` adds captions and the narration slice, then encodes `EP00N-S0N.mp4`.
   - Then ffprobe the clip's length and frame count, and make a contact sheet.
6. **Present** the clip, then wait for "Approve S0N". Record the approval in the handoff.

**Measured cost (EP004, correct runs):**
- Each job spends about 3 minutes on setup.
- With 3 jobs in parallel on this Mac (8 cores), each job takes about 11–17 s per frame, so the effective rate is about 4–6 s per frame.
- A 3–5 s scene renders in about 10–15 minutes.
- Examples:
  - S01: 127 frames, 12 min
  - S03: 147 frames, 7 min
  - S09: 111 frames, 13.5 min

## EP004 production delay (2026-11-11 to 2026-11-13)

- **What happened.**
  - From S06 on, the full-render command was typed as a zsh loop, `for r in "606 639" ...; do set -- $r; blender ... $1 $2`.
  - zsh does not split `$r` into words, so each job received the single argument `"606 639"`.
  - The renderer did not recognise it as a number, so it silently fell back to its defaults: start at frame 0 and stop at the last scene built.
  - Every one of the 3 jobs therefore rendered the whole video so far, all at once and competing for the machine.
  - The tell-tale signs:
    - log names with a space, such as `s08-861 917.log`
    - logs that start at `FRAME 0`
- **Cost.**

  | Render | Wall time | Normal |
  |---|---|---|
  | S06 | 1 h 22 min | ~10 min |
  | S06 revision | 3 h 15 min | ~10 min |
  | S07 | 2 h 19 min | ~15 min |
  | S08 | 6 h 52 min | ~15 min |
  | S09, first try | stopped after 2 h 47 min | ~15 min |

  **About 16.5 hours in total, where about 1 hour was needed.** S01–S04 and the corrected S09 run were not affected.
- **Second cause: the Mac slept.** macOS logs (`pmset -g log`) show "Clamshell Sleep" on battery while renders were running. Blender stops while the Mac sleeps.
  - S08: 4 h 12 min of its 6 h 52 min was sleep (lid closed from about 16:24 to 19:54, plus a nap at 14:43), and 2 h 40 min was rendering. The rendering part was itself about 10× too long because of the bug.
  - S06 revision: 57 min of sleep.
  - S07 and both S09 runs: no sleep. The first S09 try (2 h 47 min) was the bug alone. Each job had reached about frame 580 of 1,140, so it would have needed about 5.5 h; the corrected run took 13.5 min.

  **Rule:** keep the Mac plugged in with the lid open during a render. Keeping it awake while idle does not stop sleep when the lid closes on battery.
- **Side effect.**
  - The saved frames 0–860 were re-rendered from newer code.
  - Rebuilding S01–S07 from them matched the approved clips within render noise: PSNR at least 40 dB, 126 frames bit-identical.
  - The approved clips were never touched.
- **Fixes in place.**
  - `ep004_render.py` now stops with an error if a frame range argument is not a number. It also prints the range it will render.
  - `scripts/render_scene.py` launches the jobs from Python with separate arguments (no shell word splitting). It then does the missing-frame and Traceback checks, the finish step and the ffprobe in one go.

## Make the next video faster

1. **Always launch through `scripts/render_scene.py`**, never a hand-typed shell loop. Before leaving a render running, check the first log lines: the first `FRAME` must equal the job's start.
2. **Watch the clock.** If a scene has not finished in about 2× its expected time (frames × 5 s + 3 min), stop and look at the logs rather than waiting.
3. **Build only the stage being rendered.** Every job currently builds every set in the episode, which is about 3 min per job and grows with each new set. Build the stage(s) the requested frames use, and nothing else.
4. **Measure parallel against single.** Time one 20-frame slice with 1, 2 and 3 jobs. The jobs share one GPU, so 3 jobs may not be 3× faster.
5. **Cheaper check stills.** Render check stills at 50% scale and 16 samples. Keep 100% and 32 samples for the final clip.
6. **Profile one frame.** Split each frame's time between EEVEE and Freestyle. If Freestyle dominates, limit ink lines to the objects that need them, or try the Line Art modifier.
7. **Render one scene while the creator reviews the last one only when the creator says so.** The approval gate stays per scene.
