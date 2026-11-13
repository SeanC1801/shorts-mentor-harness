# Format tests
Creator decision, 2026-11-13: test each change before it becomes a channel rule. Nothing here is settled until its row says "kept" or "dropped". Topic branches are tracked separately in `branch-test-plan.md`.

## How a test is read
- **Baselines** (creator's analytics, 2026-11-13): EP003 65.4% stayed, 78% average viewed, 1.9K views. EP004 61.5% stayed, 63% average viewed, 1.1K views in its first 13 hours. EP002 41.0% stayed.
- **Measures:** stayed to watch, average percentage viewed, views at 24 hours and at 7 days, likes per view, subscribers gained.
- **One video is one sample.** At 1K to 2K views per video, a single result is a hint. A change is "kept" only after it has appeared in at least two episodes that beat the baseline, and "dropped" after two that do not.
- **Each episode's concept card states which tests it carries.** Its results are entered below at 24 hours and 7 days.
- **Topic changes with every episode,** so no test here is clean. Read each result next to that episode's topic.

## Register
| # | Change under test | Against | Cost to try | Status | Episodes and results |
|---|---|---|---|---|---|
| 1 | Stakes-first opening: premise and stakes in the first sentence, about ten words | anti-hook (understated, context-light) | script only | not started. Note 2026-11-13: Ricks Clips opens on a concrete contradiction (the anti-hook family) and outperforms both stakes-first channels, so both styles are live | |
| 2 | Title and first line say the same thing | title carries the half the hook withholds | script only | not started | |
| 3 | Short sentences (about 6 to 9 words), fragments allowed | story-chain paragraph (EP003 12.6, EP004 11.6 words per sentence) | script only | not started | |
| 4 | Second person ("you") | third person | script only | not started | |
| 5 | Ending that loops into the first line, or a callback joke, on a full picture | closing callback, then fade to black | script and finish | not started | |
| 6 | No fade-in: first frame lit with the first caption up | fade from black | finish only | not started | |
| 7 | Phrase captions (2 to 4 words), about twice the size, one highlighted keyword | one small white word at a time | finish only | not started. Note 2026-11-13: Ricks Clips (4M to 34M views) uses one or two words at twice our size, so size may matter more than phrasing | |
| 8 | A new picture every 2 to 3 seconds, hard cuts allowed | long continuous camera moves | storyboard and render | not started. Note 2026-11-13: Ricks Clips almost never cuts (one video has no hard cut), so this is an open question, not a gap | |
| 9 | An on-screen object for each spoken number or key noun | captions only | storyboard and render | not started | |
| 10 | 3D characters (sphere head, painted face, bean body, thin limbs) | flat cutout cards | new character build | look test rendered 2026-11-13, awaiting the creator's review; not yet used in an episode | |
| 11 | Flat colour fills, two tones, darker and more saturated | painted textures, three tones (EP004 pale and bright) | new look | look test rendered 2026-11-13, awaiting the creator's review; not yet used in an episode | |
| 12 | Character in most shots, several faces per scene | character in about a third of views, one face per card | storyboard and render | not started | |
| 13 | Length of 60 to 90 seconds | 36 to 54 seconds | script | not started | |
| 14 | Dense, dressed sets with story props and readable signs; mood lighting (striped window light, glowing lamps and neon, soft focus) | sparse sets, even daylight | set build | look test v2 rendered 2026-11-13, awaiting review | |

## Suggested order (the creator decides)
Changes that cost nothing to produce come first, so the expensive ones are tested on a stronger base.
1. **Script group (1 to 4):** no production cost.
2. **Finish group (5 to 7):** no Blender render.
3. **Picture group (8, 9, 12):** storyboard and render time.
4. **Look group (10, 11):** needs an approved look test first.
5. **Length (13):** once the opening holds viewers.

Testing a group at once is faster but cannot say which change inside it mattered. If a group wins, its changes can be separated later.

## Look test, 2026-11-13 (rows 10 and 11)
- **Asked for by the creator:** "Prepare the look test for the 3D character and environment, provide plenty stills".
- **Code:** `renderer-blender/toon3d.py` (flat two-tone materials, gradient sky, the 3D character), `renderer-blender/lookdev_3d_style.py` (studio and outdoor set, 17 stills), `renderer-blender/scripts/paint_faces3d.py` (six swappable faces in `textures/faces3d/`).
- **Stills:** `renders/lookdev-3d/` (git-ignored): 17 full-size stills and four sheets (A character, B day, C outline test with sunset and night, D before and after against EP004).
- **Measured:** outdoor stills have saturation 94 to 160 and brightness 32 to 70 (references: 111 to 165 and 32 to 43; EP004: 98 and 55). The day stills are brighter than the references.
- **Outline test:** fence, tree and hill outlines run right up to the character's edge at both zoom levels; the card "box" does not occur.
- **Known limits:** still poses only (no animation rig yet); face features are low-contrast on the darkest skin tone; the shadow tone crosses the lower face; thin hill outlines cross the lawn; night medium shot is dull.
- **Status:** look test v1 **approved by Sean Caling, 2026-11-13 ("I approve this look")** as the direction. The creator asked for a comparison with Ricks Clips and a further round of character and environment stills before the animation and narration styles are finalized, so `visual-style.md` is not yet changed.

## Look test v2, 2026-11-13 (rows 10, 11 and 14)
- **Asked for by the creator:** compare with Ricks Clips frame by frame, "then send looks tests for the character and environment, provide me with plenty stills before finalizing the animation, narration styles".
- **Code:** `renderer-blender/lookdev_3d_style_v2.py`; `toon3d.py` gained a highlight tone, lamp-coloured light, a glow and vignette pass, set text, and a slimmer "bean" build; `paint_faces3d.py` gained eye whites and three faces (smug, nervous, laugh), nine in all.
- **Stills:** `renders/lookdev-3d-v2/` (git-ignored): 18 full-size stills and four sheets (A character, B workshop, C night street, D beside Ricks Clips frames).
- **Measured:** workshop saturation 105 to 156, brightness 49 to 69; night street saturation 100 to 146, brightness 27 to 53. Clipped whites under 0.3% except the vending-machine still.
- **Render time:** 18 stills in 110 s in one job: about 15 s to build the scene, then about 5.3 s a still at 1080×1920 with the glow pass. EP004's frames took 11 to 16 s each with three jobs running.
- **Known limits:** still poses only (no animation rig); shop windows are flat bright panels; faces fall into the shadow tone when the only light is behind the character; Blender warned that its shadow buffer was full, so some lamp shadows may be missing; the faces sheet stacks three rows, so lower bodies overlap.
- **Decision, 2026-11-13:** the creator chose the **bean build (v2)** to carry forward ("Bean build (v2)"): one long bean body, shorter legs, thinner limbs, small hands and shoes. The classic build from v1 is retired.
- **Decision, 2026-11-13:** the creator chose **dense, dressed sets with mood lighting** ("Yes, dense and moody"), as in the workshop and night-street stills: story props and readable signs, striped window light, glowing lamps and neon, lamp-coloured light, the glow pass and a soft vignette.
- **Look so far:** v1 direction approved; bean build; dense sets with mood lighting. These are the look the next episode tests (rows 10, 11 and 14); they become channel rules only after their episode results, and `visual-style.md` is unchanged until then.
- **Not yet built:** character motion (re-posing limbs and swapping faces frame by frame). Next: a short motion test clip, with the creator's go-ahead before any render.

## Motion test, prepared 2026-11-13 (code only, nothing rendered)
- **Asked for by the creator:** "Yes, prepare it" (the character motion test, code only).
- **Code:**
  - `toon3d.py`: limbs are rebuilt in place each frame (`tube_update`, `pose_kid`), poses blend (`mix_pose`), faces swap (`face_kid`).
  - `scripts/paint_faces3d.py`: a tenth face, `blink`.
  - `toon_sets.py`: the workshop and night-street sets and their lighting, moved out of the look-test script so both scripts share one copy.
  - `motion_test_3d.py`: the test clip (removed 2026-11-14; now `episodes/motion_test.py`, rendered by `render_episode.py`). It stops on a non-numeric frame argument, like the EP004 renderer now does.
- **The clip:** 100 frames (3.3 s) at 30 fps, the bean-build kid in the workshop, no captions or narration. Stand, glance toward the jar, think (worried), idea (points up with a hop and a stretch, surprised then happy), shrug (smug), then the jar flares and the kid jumps (nervous). Pose changes take 5 frames with a small overshoot and then hold; faces change through a 2-frame blink, except the startle; two idle blinks; the camera pushes in the whole time.
- **Checked without rendering:** `--dry` ran all 100 frames. Limbs move, the hop lifts the body, faces change on the right frames, the jar flares from frame 82, and the whole figure stays in frame. Both look-test scripts still build after the refactor.
- **Not checked:** how it looks. That needs the render.
- **Next:** ask before rendering. About 9 minutes in one job at about 5.3 s a frame.
- **Rendered 2026-11-13** ("Yes, render it"): `renders/motion-test-3d/motion-test-3d.mp4` (git-ignored), 100 frames, 1080×1920, silent; frames `m_0000`–`m_0099` and a strip `sheet.png`. Poses, hop, face swaps, blinks and the jar flare all show; the figure stays in frame. **Awaiting the creator's review.**
- **Approved by Sean Caling, 2026-11-13 ("I approve it")**: the motion test as rendered. The 3D character look is now approved to try in the next episode (rows 10, 11, 14); results still decide whether it becomes a channel rule.
