# Efficiency plan (v1, 2026-11-13, not yet built)

The plan for making an episode faster to produce, asked for by the creator on 2026-11-13. Nothing here is built. Each step is its own piece of work with a check, so it can be approved and built one at a time.

## Where the time goes now
Estimates from EP004 and the 2026-11-13 look and motion tests. Only the render figures are measured.

| Work | Time today | Why |
|---|---|---|
| Rendering one 4–5 s scene | 4–8 min | About 5 s a frame in the v4 look; one job |
| Start-up before a job's first frame | 15 s (test scene) to 3 min (EP004) | Every job builds every set in the episode |
| Preparing a scene whose set exists | 15–30 min | Camera, acting and timing are hand-written code per scene |
| Preparing a scene with a new set | 45–90 min | Each set is built from scratch in code |
| Full preview assembly | 23 min | Joins and captions drawn frame by frame in one process |
| Re-timing after narration changes | hours on EP004 | Shot timings live in four places (see step 1) |
| A 12-scene episode | about 6–12 hours | Mostly preparation, and mostly new sets |

## Goals
- A 12-scene episode in **3–5 hours** of production once the idea, script and storyboard are approved.
- No scene waits more than **10 minutes** on a render.
- A timing change is made in **one file**.
- No approved clip can be overwritten by accident, and no render can silently run the wrong frames.

## Steps, in build order
Each step lists what is built, how it is checked, and the saving expected.

### 1. One timing file drives everything
- **Now:** shot timings are written in `storyboard.md`, `episode.json`, the `VIEWS` list in the render script and `STARTS` in the finish script. EP004 also carried a second clock after its narration was re-timed.
- **Build:** the renderer and the finish step read shot start and end frames, joins and caption words from `episode.json` (already validated by `tools/validate_episode.py`). The render script keeps only what a shot looks like: its set, lighting state, camera path and acting.
- **Check:** change one shot boundary in `episode.json`; a dry run and the finish step both pick it up with no other edit.
- **Saves:** the re-timing work; removes a whole class of mismatch errors.

### 2. A shared renderer, one small file per episode
- **Now:** `ep003_*` and `ep004_*` are copies: about 5,000 lines, edited by hand each episode.
- **Build:** a shared `render_episode.py` (argument checks, frame loop, stage switching, dry-run mode) and a shared `finish_episode.py` (joins, captions, narration slices, preview). An episode supplies one file: its scenes, cameras and acting. The `--dry` mode from the motion test becomes standard.
- **Check:** the motion test re-rendered through the shared renderer matches its approved frames.
- **Saves:** setup time per episode; fixes land once instead of per copy.

### 3. Build only what a scene needs
- **Now:** every job builds every set (3 minutes per job on EP004, and growing with each set).
- **Build:** sets register themselves by name in `toon_sets.py`; a job builds only the sets its frame range uses.
- **Check:** a one-scene job's log lists one set, and its first frame arrives in under 30 seconds.
- **Saves:** about 3 minutes per job, more as the set library grows.

### 4. A set library
- **Now:** two sets exist in the v4 look (workshop, night street). Every new place is built from nothing.
- **Build:** reusable pieces (walls with window openings, shelves, benches, shopfronts, street furniture, trees, signs) and a few more whole sets the niche needs often: a bedroom or living room, a daytime street, a classroom or lab, open country, space with Earth. Each set takes colour and prop options, so one build serves several episodes.
- **Check:** a new interior is assembled from pieces in under 20 minutes and passes a stills review.
- **Saves:** the largest single cost: 45–90 minutes per new set becomes 10–20.

### 5. A pose and acting library
- **Now:** eight poses and ten faces; acting is keyed by hand per beat, as in the motion test.
- **Build:** more poses (sit, reach, hold an object, look back, run, cower, cheer), named acting beats that bundle a pose change, a face and a hop ("idea", "startle", "shrug it off"), and a short notation so a scene's acting is a list of beats on narration words.
- **Check:** the motion test's acting is rewritten as five beats and renders the same.
- **Saves:** 10–20 minutes per acting-heavy scene.

### 6. The scene launcher, generalized
- **Now:** `scripts/render_scene.py` is tied to EP004's file names.
- **Build:** it takes the episode and scene, reads the frame range from `episode.json`, splits the work, checks each job's first frame, missing frames and errors, runs the finish step and writes a contact sheet. It warns when the Mac is on battery, and it stops if a job runs past twice its expected time.
- **Check:** one command renders, checks and finishes a scene; a deliberately bad range is refused.
- **Saves:** manual checking; prevents a repeat of the EP004 delay.

### 7. Measure, then tune render speed
- **Build:** time one 20-frame slice with 1, 2 and 3 jobs; split a frame's time between the picture, the ink lines and the glow pass. Then apply what the numbers support: the best job count, ink lines only on objects in view, and 50% size with fewer samples for check stills.
- **Check:** the measurements are recorded in `render-pipeline-notes.md`, with the settings chosen from them.
- **Saves:** unknown until measured; check stills should become about four times cheaper.

### 8. Faster preview assembly
- **Now:** 23 minutes: 1,607 frames processed one at a time.
- **Build:** run the per-frame work in parallel, and reuse the frames already finished for each approved scene.
- **Check:** a full preview assembles in under 5 minutes and matches the scene clips.
- **Saves:** about 18 minutes per preview.

## Order and size
| Step | Depends on | Size |
|---|---|---|
| 1. One timing file | none | medium |
| 2. Shared renderer | 1 | medium |
| 3. Build only what is needed | 2 | small |
| 6. Scene launcher | 1, 2 | small |
| 4. Set library | 2 | large, grows with each episode |
| 5. Pose and acting library | 2 | medium |
| 7. Measure and tune | 2, 3 | small |
| 8. Faster preview | 2 | small |

Steps 1, 2, 3 and 6 are the base and are best finished before EP005 starts. Steps 4 and 5 can be built as EP005 needs them, so their first pieces are driven by a real story.

## What stays as it is
- The creator's approvals: ask before every render, one scene at a time, each approved before the next.
- Posted episodes: EP003 and EP004 keep their own scripts and are not converted.
- Changes to format and look remain tests (`03_TRACKING/format-tests.md`).

## Not decided
1. Whether the base (steps 1, 2, 3 and 6) is built before EP005's idea is chosen, or alongside it.
2. Which sets step 4 builds first; that depends on EP005's topic.
3. Whether scene approvals could be grouped for scenes that share a set. Today each scene is approved on its own.
