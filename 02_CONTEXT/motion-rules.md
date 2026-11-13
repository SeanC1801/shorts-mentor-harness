# Motion rules (v3)

**Status:** v3 follows the creator's approval of the 3D motion test on 2026-11-13 ("I approve it") and applies from EP005. It changes the character rules for 3D characters and marks which camera and caption rules are under test (`03_TRACKING/format-tests.md`). The validator accepts 24 fps only for episodes made before v2.

These rules are based on measured Ricks Clips camera work and Zack D. Films / Ricks Clips caption and narration craft (`source-analysis/animation-style-notes-ricks-clips.md`, `narration-style-notes*.md`). Use them as craft principles, not a look to copy.

## Camera
| # | Rule | Target |
|---|---|---|
| 1 | **Frame rate.** The camera, effects and characters update every frame. | 30 fps |
| 2 | **The camera is always moving:** push, pull, pan, track, crane, orbit or whip. | Median motion about 90–110 px/s at 1080 wide; at most about 20% of frames nearly still |
| 3 | **Short views.** Each narration line gets 2–3 views: a new framing, a new subject or a reveal. | A new view every 1.5–2.5 s |
| 4 | **No hard cuts by default.** Join views by following an object into the next beat, pushing through an object (a window, lens or screen), a motion-blurred whip pan, or a 4–6 frame dissolve while the camera keeps moving. **Under test (row 8):** a new picture every 2–3 seconds with hard cuts allowed. Ricks Clips almost never cuts; Jaywalk and Afterhour Theory cut every 2–3 seconds. | At most 1 deliberate hard cut per episode, unless the episode carries test 8 |
| 5 | **Short holds.** Hold only on a face or fact beat, and even then the camera creeps. | At most about 0.5 s |
| 6 | **Use the depth.** Move past the foreground strip, track along the mid stage, reveal the backdrop. | Foreground occluders cross the frame in most moves |
| 7 | **Facts as objects.** Push in until the object that carries the fact fills most of the frame. | At least one per fact line |
| 8 | **Light tells the story.** Change the lighting state at story turns (see `visual-style.md`). | At least 2 lighting states per episode |
| 9 | **Effects only when the story needs them:** dust, sparks, smoke, splash, light shafts, depth of field. Use motion blur on whips. | Never over captions |

## Characters (3D, from the approved motion test)
- **Poses snap, then hold.** A pose change takes about 5 frames with a small overshoot, then the body is still. No idle sway.
- **Faces change through a blink:** two frames with the eyes shut, then the new face. A startle is the exception: it changes at once.
- **Idle blinks** of two frames, every two to three seconds, keep a held pose alive.
- **Big beats get a hop and a stretch:** the body lifts a few centimetres and stretches upward for about 8 frames.
- **Gestures land just before the word they support.**
- **The head can turn and tilt** toward what the character looks at. Keep turns under about 30 degrees so the painted face stays toward the camera.
- **A character is on screen in most shots** and acts out the line. Under test (row 12).
- Tools: `toon3d.pose_kid`, `face_kid`, `mix_pose`; poses in `toon3d.POSES`.

## Captions
- One word at a time (two for very short words), changing in sync with the narration audio.
- Heavy rounded sans-serif, white with a thin navy outline and a soft shadow. Each word pops in from about 86% to 100% scale over 3 frames.
- Glyphs about 40–45 px tall at 1920. Centred in the 62–72% height band, clear of faces and fact objects. **Under test (row 7):** captions about twice this size; phrases of 2–4 words with one highlighted keyword.
- Motion never hides captions or claims.

## Opening and ending (under test, rows 5 and 6)
- EP003 and EP004 faded in from black and out to black. The tests: a first frame that is already lit with the first caption up, and a last frame that is a full picture (a loop into the first line, or a callback).

## Timing
- Every timing is an integer frame. Sync to measured narration audio once it exists; until then, label timing as provisional.

## History
- **v2 (2026-11-02):** as v3, but for flat cutout characters: instant pose and face swaps held at least 2 frames, bodies simple, the camera carrying the energy. Used for EP003 and EP004.
- **v1 (2026-10-31):** 24 fps master; poses at 12 per second, each exposed for 2 frames; smooth camera and parallax; dead-still holds on important information; motivated transitions. Used for EP002.
- An earlier draft proposing 2.5D motion in Remotion was replaced by this file and removed.
