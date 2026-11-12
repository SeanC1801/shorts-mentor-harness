# EP003 Storyboard v3 (DRAFT, awaiting creator approval)

- Episode/version: EP003 / storyboard v3. Only S01 V1 changed from approved v2 (kept as `storyboard-v2.md` and `episode-v2.json`). The creator asked on 2026-11-03: "Instead of making the opening a globe, just make it the actual Earth on space surrounded by rocks".
- Approved script version: v2 (approved 2026-11-02); approved idea version: v2
- Narration audio: `audio/EP003-narration-v2.mp3` (ElevenLabs voice "Shorts Voice", a voice clone made by the creator), **52.506 s measured**. Total 1575 frames (52.50 s) at 30 fps, 1080x1920. Shot boundaries sit in the measured pauses between sentences; word times in `audio/word-timings-v2.json` (pause anchors, about ±0.1 s per word; sentence boundaries measured, a few pauses interpolated).
- Machine-readable plan: `episode.json` (checked by `validate_episode.py`, which checks structure and timing only and does not verify media or render anything).
- Look and motion: `visual-style.md` v2 and `motion-rules.md` v2 (30 fps, Blender 3D sets, flat cutout characters, always-moving camera, no hard cuts).
- Animation preview is a separate gate; nothing has been built or rendered.

## Shot table (grouped by story beat)
| Shot | Frames | Narration | Transition in → out |
|---|---|---|---|
| S01 | 0–162 (0.00s–5.40s) | Put a ring around Earth like Saturn's, and a kid opening the curtains would see a stripe across the sky. | fade-in → push-through |
| S02 | 162–313 (5.40s–10.43s) | It couldn't be ice, because ice wouldn't last this close to the Sun, so say it's rock. | follow → whip |
| S03 | 313–385 (10.43s–12.83s) | Where you stand decides what you see. | whip → follow |
| S04 | 385–671 (12.83s–22.37s) | At the equator, the ring is a thin line straight overhead. Farther north, it stretches into a wide arch. Far enough north, it never rises above the horizon. | follow → follow-pull-back |
| S05 | 671–737 (22.37s–24.57s) | But Earth might not need a what-if. | follow-pull-back → dissolve |
| S06 | 737–983 (24.57s–32.77s) | A study suggests that 466 million years ago, an asteroid passed too close, and Earth's pull tore it apart into a ring. | dissolve → follow |
| S07 | 983–1122 (32.77s–37.40s) | The clue is in the craters: twenty-one from that era all formed near the equator. | follow → dissolve |
| S08 | 1122–1306 (37.40s–43.53s) | You see, a ring doesn't last forever. Its pieces slowly fall back, and near the equator is where they'd land. | dissolve → dissolve |
| S09 | 1306–1511 (43.53s–50.37s) | Some experts doubt the crater ages, but if the study is right, Earth once wore a ring, long before the dinosaurs. | dissolve → fade-through |
| S10 | 1511–1575 (50.37s–52.50s) | A what-if that may have been real. | whip → fade-out |

## Views (every view has camera motion)
| View | Frames | Lighting state | What we see | Camera | Joins next by |
|---|---|---|---|---|---|
| S01 V1 | 0–60 (2.0 s) | LS2 cool deep space | Today's Earth floating in space; rocks close in from a wider orbit and settle into a ring around it. | Slow push-in on Earth as the rocks settle | push-through Earth toward the window |
| S01 V2 | 60–112 (1.7 s) | LS1 warm morning | Bedroom, foreground curtains. A kid pulls the curtains open with both hands; bright window. | Push-in on the kid's hands, curtains sweep across the lens | push-through the window gap |
| S01 V3 | 112–162 (1.7 s) | LS1 warm morning | Outside the window: a pale stripe cuts across a blue sky; the kid looks up (POSE-KID-LOOK-UP). | Push through the window into the sky, then tilt up the stripe | follow the stripe |
| S02 V1 | 162–215 (1.8 s) | LS1 warm morning | Rooftops from a low angle; the stripe resolves into a ring of tan-grey rock chunks. A Saturn poster pinned beside the window shows white icy rings for comparison. | Tilt up along the ring; slow drift past a rooftop in the foreground | whip pan to the Sun |
| S02 V2 | 215–265 (1.7 s) | LS1 warm morning | A chunk of white ice beside a blazing sun fizzles and shrinks. | Whip in, then slow push on the ice as it fizzles | follow the sun glare |
| S02 V3 | 265–313 (1.6 s) | LS1 warm morning | A rock chunk next to the sun stays whole; the ice chunk is gone. | Slow push on the rock chunk, sun flare crossing the lens | whip to the globe |
| S03 V1 | 313–350 (1.2 s) | LS2 cool deep space | A globe floats in space with three glowing pins: equator, middle, far north. | Whip in and settle; slow orbit around the globe | follow the pins |
| S03 V2 | 350–385 (1.2 s) | LS2 cool deep space | The pins light up one by one, equator first; the camera closes on the equator pin. | Push in on the equator pin | push-through the pin to the beach |
| S04 V1 | 385–435 (1.7 s) | LS1 warm morning | Equator beach, palm fronds in the foreground. The ring is a thin bright line straight overhead. | Tilt up following the line to the zenith | follow the line to the kid |
| S04 V2 | 435–487 (1.7 s) | LS1 warm morning | The kid on the sand looks straight up (POSE-KID-LOOK-UP); the thin line passes right above. | Low angle, slow push-in, line crossing overhead | whip pan along the ring |
| S04 V3 | 487–530 (1.4 s) | LS1 warm morning | Mid-latitude city rooftop, railing in the foreground. The ring is a wide arch over the southern sky; the kid sweeps an arm along it. | Pan across the arch, parallax past chimneys | follow the arch down |
| S04 V4 | 530–573 (1.4 s) | LS1 warm morning | The arch comes down to the horizon over the rooftops. | Follow the arch down to the horizon | whip pan north |
| S04 V5 | 573–620 (1.6 s) | LS5 cool low sun | Far-north snowy town, fence and snow bank in the foreground. The sky is empty. | Crane up to a wide, empty sky | push to the dotted line |
| S04 V6 | 620–671 (1.7 s) | LS5 cool low sun | A faint dotted line marks where the ring would be below the horizon; the kid shrugs (POSE-KID-SHRUG). | Rest on the dotted line, slow drift | pull back to space |
| S05 V1 | 671–705 (1.1 s) | LS2 cool deep space | Pull back from the town to a globe floating in space; the ring vanishes, leaving a plain Earth. | Pull back from the ground to a wide space view | dissolve to the ancient globe |
| S05 V2 | 705–737 (1.1 s) | LS2 cool deep space | The globe tilts; a ghost ring shimmers faintly around it; a question mark glints. | Slow orbit and tilt toward the ghost ring | dissolve |
| S06 V1 | 737–800 (2.1 s) | LS2 cool deep space | An in-world paper with the stamp 'A STUDY SUGGESTS' (a hypothesis, not a fact); the globe turns behind it. | Push in on the stamp | whip to the timeline card |
| S06 V2 | 800–849 (1.6 s) | LS2 cool deep space | A timeline card slides back to '466 MILLION YEARS AGO' over a plain ancient globe. | Push in on the card as the globe turns behind it | whip to the asteroid |
| S06 V3 | 849–905 (1.9 s) | LS2 cool deep space | A lumpy asteroid sails toward Earth, passing close; foreground rock fragments streak past. | Fast tracking move following the asteroid in | follow the asteroid as it stretches |
| S06 V4 | 905–983 (2.6 s) | LS6 warm orange glow | The asteroid stretches, cracks and splits; the pieces spiral into a ring around the globe; warm glow at the break. | Orbit the globe as the ring forms; motion blur on the pieces | follow the pieces to the surface |
| S07 V1 | 983–1035 (1.7 s) | LS2 cool deep space | Ancient globe with an equator line; dots pop onto the surface one by one with a counter 21. | Push in following the first dots, slow orbit | follow the dots |
| S07 V2 | 1035–1080 (1.5 s) | LS2 cool deep space | More dots pop on; the counter races to 21. | Orbit and push across the surface | pull back along the equator |
| S07 V3 | 1080–1122 (1.4 s) | LS2 cool deep space | Pull back: all 21 dots sit in a narrow band along the equator; the band glows. | Pull back and orbit to show the band | dissolve to the falling ring |
| S08 V1 | 1122–1189 (2.2 s) | LS2 cool deep space | The ring around the globe slowly thins and dims; a pair of pieces drift off its edge. | Slow orbit with a gentle push | follow the loose pieces down |
| S08 V2 | 1189–1250 (2.0 s) | LS2 cool deep space | Pieces fall slowly toward the surface, streaking; foreground fragments pass the lens. | Follow the pieces down in a long tracking move | follow them to the surface |
| S08 V3 | 1250–1306 (1.9 s) | LS2 cool deep space | The pieces land in a band along the equator, small flashes; the band glows. | Pull back along the equator | dissolve to the craters |
| S09 V1 | 1306–1371 (2.2 s) | LS2 cool deep space | Three craters with age tags flicker '466?'; a tiny question mark rises from each. | Quick push in, slight handheld drift on the tags | dissolve to the ring |
| S09 V2 | 1371–1414 (1.4 s) | LS2 cool deep space | A ring materializes around the ancient globe; the paper stamp 'A STUDY SUGGESTS' glints beside it. | Orbit and push toward the ring | dissolve to the seafloor |
| S09 V3 | 1414–1460 (1.5 s) | LS7 teal ancient sea | Ancient seafloor, ferns and rocks in the foreground. A small trilobite looks up through shallow water at a ring arching across the sky. | Crane up from the trilobite to the ring | dissolve to a plain |
| S09 V4 | 1460–1511 (1.7 s) | LS8 pale dawn | The ring fades out; a small cartoon dinosaur walks in under an empty sky and looks up. | Slow pull back to a wide | whip to the bedroom |
| S10 V1 | 1511–1575 (2.1 s) | LS8 pale dawn | The kid's bedroom window at dawn; the sky is empty with the faintest stripe fading. Final hold, then fade to black. | Slow push-in toward the window, a gentle push over the last frames | fade-out |

## Motion-rule check (v2)
- **Views:** 31 views in 52.5 s, average 1.7 s (range 1.1–2.6 s). Views over 2.5 s: S06 V4; the camera keeps moving in each.
- **Hard cuts:** 0. Joins are push-through, follow, whip and dissolve, plus a fade-in at the start and a fade-out at the end.
- **Holds:** none; the final window view (S10) pushes in slowly through the fade-out.
- **Lighting states:** LS1 warm morning, LS5 cool low sun, LS2 cool deep space, LS6 warm orange glow at the asteroid break, LS7 teal ancient sea, LS8 pale dawn.
- **Depth:** each set has a foreground strip (shelf, curtains, rooftops, palm fronds, railing, snow bank and fence, rock fragments, seafloor ferns), a mid stage and a painted backdrop. Sets are 3D in Blender; characters and printed props are flat cutouts with contact shadows.
- **Facts as objects:** the paper stamp "A STUDY SUGGESTS", the timeline card "466 MILLION YEARS AGO", the counter "21" and the age tags "466?" fill the frame.

## Story-chain notes (script v2)
- **Hook (S01):** the premise is staged as rocks settling into a ring around Earth in space, then the kid at the window. The outcome (what the stripe is, who sees it) is withheld.
- **Context (S02):** rock versus ice, shown with one fizzling ice chunk next to the Sun.
- **Rule and escalation (S03–S04):** three places in rule-of-three order: thin line, wide arch, empty sky; the shortest sentences carry the turns.
- **Reversal (S05) and evidence (S06–S07):** "But Earth might not need a what-if" is a pull back and a dissolve into deep time; the study is shown as a stamped paper (C7); the craters as a counter (C8).
- **Reveal (S08):** "You see, a ring doesn't last forever": the ring thins, its pieces fall, and they land along the equator (C11).
- **Honest limit and payoff (S09):** "466?" age tags carry the doubt (C9); trilobite and dinosaur carry "long before the dinosaurs" (C10).
- **Callback (S10):** back to the kid's window at dawn with an empty sky: "A what-if that may have been real."
- **Honesty labels:** S01–S04 are a hypothetical scenario; the study is always shown as a paper stamped "A STUDY SUGGESTS"; nothing implies the ring is proven.
- **Caption style:** `CAPTION-WORD-BY-WORD`, one word at a time, lower third (about 66% of the height), clear of faces and fact objects; the renderer splits words with `word-timings-v2.json`.

## Retention notes and risks
- **Length:** 52.5 s, 13 s longer than v1. S04 (9.5 s, six views) and S06 (8.2 s, four views) are the longest shots.
- **Geometry (S04):** thin line, wide arch and empty sky are my own calculation and still need an independent check before art is built.
- **Ice versus rock (S02):** popular-science sources only (C3).
- **Sound:** soft whooshes on each whip, ring settle, curtain swish, ice fizz, pin pops, paper stamp, asteroid pass, crack and rumble, dot pops, debris fall, question flicker, shallow-sea ambience, dinosaur steps, one soft music bed. The creator picks and edits sound in CapCut.

## Assets (all planned; none exist yet)
Characters (new, need creator approval before any art): CHAR-KID (poses: curtains, look-up, shrug), CHAR-TRILOBITE (look-up), CHAR-DINO (look-up). Sets: bedroom, rooftops, beach, city rooftop, snowy north town, space, seafloor, dawn plain. Props/FX: Earth in space (opener), rock ring, Saturn poster, ice-and-sun insert, pins globe, ghost ring, ancient globe, timeline card, paper with stamp, asteroid, ring-formation FX, crater dots and counter, ring-fade and debris-fall FX, age tags. See `episode.json` for the per-shot asset IDs.

## Open decisions for the creator (defaults stand if unanswered; a change after approval invalidates this storyboard)
1. **Characters:** approve (or change) the kid, the trilobite and the dinosaur before any art is made.
2. **A "WHAT IF" tag** on the opening scene, or keep S01 clean (default: clean).
3. **Ending:** v2 ends on the kid's window and the callback line (the dinosaur appears in S09). Keep, or end on the dinosaur?
4. **Same kid in three places (S04):** the same character in three outfits (default), or three different small locals.

## Storyboard approval (artifact version, decision, timestamp)
Pending. Not approved.
