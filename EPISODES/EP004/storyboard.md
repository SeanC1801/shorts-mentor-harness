# EP004 Storyboard v2 (DRAFT, awaiting creator approval)

- Episode/version: EP004 / storyboard v2 (re-timed to the script v2 narration; v1 kept as `storyboard-v1.md` and `episode-v1.json`). Shots, views, cameras, lighting, characters and assets are unchanged from approved v1; only the frame ranges, narration text and cue times moved.
- Approved script version: v2 (approved 2026-11-11); approved idea version: v3
- Narration audio: `audio/EP004-narration-v2.mp3` (ElevenLabs voice "Shorts Voice", a voice clone made by the creator; stability 61, similarity 75, v4), **53.551 s measured**. Total 1607 frames (53.57 s) at 30 fps, 1080x1920. Shot boundaries sit in the measured pauses between sentences; word times in `audio/word-timings-v2.json` (pause anchors, about ±0.1 s per word).
- Machine-readable plan: `episode.json` (checked by `validate_episode.py`, which checks structure and timing only and does not verify media or render anything).
- Character: CHAR-RAINKID (spec v2; art batches 1–2 approved). Faces and outfits swap per view.
- Look and motion: the EP003 cel look (Blender EEVEE, cel bands and ink lines), `visual-style.md` v2 and `motion-rules.md` v2 (30 fps, 3D sets, flat cutout characters, always-moving camera, no hard cuts).
- Animation preview is a separate gate; nothing has been built or rendered.

## Shot table
| Shot | Frames | Narration | Transition in → out |
|---|---|---|---|
| S01 | 0–120 (0.00s–4.00s) | Follow the rain on a window backwards far enough, and it leads to the sea. | fade-in → follow |
| S02 | 120–254 (4.00s–8.47s) | Sunlight warms the ocean, and water rises off it as invisible vapor. | follow → follow |
| S03 | 254–401 (8.47s–13.37s) | High up, the vapor cools into tiny droplets, and the droplets gather into clouds. | follow → follow |
| S04 | 401–543 (13.37s–18.10s) | Wind carries those clouds over land, and they fall as rain on that same window. | follow → whip |
| S05 | 543–606 (18.10s–20.20s) | Now drain the ocean overnight. | whip → follow |
| S06 | 606–672 (20.20s–22.40s) | Nothing rises from the empty seafloor. | follow → dissolve |
| S07 | 672–861 (22.40s–28.70s) | A little water still lifts off lakes, soil and plants, so the clouds wouldn't vanish at once. They'd thin out. | dissolve → follow |
| S08 | 861–1029 (28.70s–34.30s) | Less cloud means less rain, and less rain means drier ground with even less water to give. | follow → follow |
| S09 | 1029–1140 (34.30s–38.00s) | A clearer sky sounds calmer. But clouds do a second job. | follow → push-through |
| S10 | 1140–1401 (38.00s–46.70s) | It turns out they're the planet's sunshade, bouncing sunlight back to space before it lands, so with fewer of them, more sun would pour onto the bare ground. | push-through → follow |
| S11 | 1401–1526 (46.70s–50.87s) | Hot, bright days, then cold, clear nights, like a desert. | follow → dissolve |
| S12 | 1526–1607 (50.87s–53.57s) | The sky was running on the ocean all along. | dissolve → fade-out |

## Views (every view has camera motion)
| View | Frames | Lighting state | What we see | Camera | Joins next by |
|---|---|---|---|---|---|
| S01 V1 | 0–42 (1.4 s) | LS1 grey rainy day (indoor, cool) | Close on one raindrop sliding down a rainy window; the kid's face behind the glass, softly out of focus (POSE-RAINKID-WINDOW, curious). | Slow push-in on the drop | follow the drop |
| S01 V2 | 42–81 (1.3 s) | LS1 grey rainy day (indoor, cool) | The drop rewinds: it slides back up the glass and lifts off into the grey sky over wet rooftops. | Tilt up following the drop | follow the drop into the cloud |
| S01 V3 | 81–120 (1.3 s) | LS2 warm sunny sea | The drop rewinds through a cloud and down to a sunlit sea, landing back in the water. | Dive down with the drop to the sea surface | follow (camera stays on the water) |
| S02 V1 | 120–184 (2.1 s) | LS2 warm sunny sea | Sunny open sea; sunlight glints across the waves as they warm. | Low glide over the waves toward the sun | follow the glints up |
| S02 V2 | 184–254 (2.3 s) | LS2 warm sunny sea | Faint, shimmering curls rise off the surface (stylized: real vapor is invisible, so it is drawn as a faint heat-haze shimmer). | Crane up with the rising curls | follow the curls up |
| S03 V1 | 254–301 (1.6 s) | LS3 cool high sky | High up, the sky turns cooler blue; the curls slow down and turn into tiny sparkling droplets. | Keep rising, slow orbit around the curls | push in on the droplets |
| S03 V2 | 301–351 (1.7 s) | LS3 cool high sky | The droplets drift together and clump. | Push in as they gather | pull back |
| S03 V3 | 351–401 (1.7 s) | LS3 cool high sky | Pull back: a fluffy white cloud has formed over the sea. | Pull back to a wide of the cloud | follow the cloud on the wind |
| S04 V1 | 401–471 (2.3 s) | LS3 cool high sky | Wind streaks push the clouds off the sea, over the coastline and toward a small town. | Track alongside the clouds, coast passing below | follow the rain down |
| S04 V2 | 471–543 (2.4 s) | LS1 grey rainy day (indoor, cool) | Rain falls on the town; one drop lands on the kid's window (POSE-RAINKID-WINDOW, curious). The loop is complete. | Follow one drop down onto the glass, then settle on the kid | whip to the sea |
| S05 V1 | 543–576 (1.1 s) | LS4 pale dawn shore | Night turns to dawn in a fast time-lapse while the whole sea drains away from the shore, leaving the beach high and dry. | Whip in, then a fast pull up and back | follow down to the kid |
| S05 V2 | 576–606 (1.0 s) | LS4 pale dawn shore | The kid on the shore in a raincoat flings both arms up (POSE-RAINKID-SHOCK, shocked). | Quick push-in on the kid | follow the kid's gaze out |
| S06 V1 | 606–640 (1.1 s) | LS5 bright dry day | The empty seafloor: damp sand, shells, a boat on its side. Nothing rises from it. | Low drift across the seabed | follow to the shore |
| S06 V2 | 640–672 (1.1 s) | LS5 bright dry day | The kid seen from behind at the shore (POSE-RAINKID-SHORE), the empty bowl of the seabed ahead, a bare sky above. | Slow crane up behind the kid | dissolve inland |
| S07 V1 | 672–727 (1.8 s) | LS5 bright dry day | Inland: a lake; a few faint curls lift off it. | Pan across the lake | pan on to the field |
| S07 V2 | 727–774 (1.6 s) | LS5 bright dry day | A field and a tree; faint curls rise from the soil, then the plants (one by one on the words). | Continue the pan, slight push-in | tilt up to the sky |
| S07 V3 | 774–818 (1.5 s) | LS5 bright dry day | Above: a cloud still forms, but it is small and patchy. | Tilt up and push toward the cloud | follow down to the kid |
| S07 V4 | 818–861 (1.4 s) | LS5 bright dry day | The clouds thin, gaps opening; the kid points up (POSE-RAINKID-POINT-UP, worried). | Low angle, slow push-in | follow the gaps |
| S08 V1 | 861–918 (1.9 s) | LS5 bright dry day | A thin cloud drops only a sparse sprinkle. | Follow a few drops down | follow them to the ground |
| S08 V2 | 918–975 (1.9 s) | LS5 bright dry day | The ground dries; cracks spread across the field; plants droop. | Push across the cracking ground | crane up |
| S08 V3 | 975–1029 (1.8 s) | LS5 bright dry day | One faint curl tries to rise from the cracked ground and fizzles out; above, the sky is nearly clear. | Crane up past the fizzling curl to the clear sky | follow up to the bright sky |
| S09 V1 | 1029–1091 (2.1 s) | LS5 bright dry day | A calm, clear blue sky; the kid, now in sun clothes, stands deadpan (POSE-RAINKID-STAND from the outfit sheet). | Slow push-in on the kid | tilt up to the sun |
| S09 V2 | 1091–1140 (1.6 s) | LS6 harsh noon glare | A thin cloud slides across the sun and the ground dims under it; it slides off and the glare snaps back. | Tilt up to the sun, flare crossing the lens | push through the glare to space |
| S10 V1 | 1140–1204 (2.1 s) | LS8 cool deep space | Earth from space: sunbeams (drawn as soft arrows of light) hit bright cloud tops and bounce back out to space. | Slow orbit around Earth | push down toward the clouds |
| S10 V2 | 1204–1269 (2.2 s) | LS8 cool deep space | Closer: the cloud layer works like a parasol, its shadow cooling the land beneath. | Push down through the cloud layer | follow the beams |
| S10 V3 | 1269–1335 (2.2 s) | LS6 harsh noon glare | The clouds thin; beams pour through the gaps and hit the ground, warming it. | Follow the beams down | follow to the ground |
| S10 V4 | 1335–1401 (2.2 s) | LS6 harsh noon glare | Bare cracked ground under a blazing sky; heat shimmer rises. | Low push across the ground | follow to the kid |
| S11 V1 | 1401–1449 (1.6 s) | LS6 harsh noon glare | Harsh glare: the kid shields the eyes (POSE-RAINKID-SHIELD, squinting), then fans itself (POSE-RAINKID-FAN). | Push-in on the kid | whip the sun down |
| S11 V2 | 1449–1488 (1.3 s) | LS7 cold clear night | The sun drops and the sky snaps to a starry night; the kid in winter clothes shivers (POSE-RAINKID-SHIVER). | Quick pull back as the light flips | pull back further |
| S11 V3 | 1488–1526 (1.3 s) | LS7 cold clear night | Wide: a desert-like plain under stars, frost glinting on the cracks; the kid small in frame. | Slow pull back to a wide | dissolve to the window |
| S12 V1 | 1526–1568 (1.4 s) | LS5 bright dry day | The kid's window again (POSE-RAINKID-WINDOW, wistful); a dry pane and a thin, bright sky outside. | Slow push-in on the kid | pull back |
| S12 V2 | 1568–1607 (1.3 s) | LS5 bright dry day | Pull back from the window to the town under the bright sky; fade to black. | Slow pull back through the fade-out | fade-out |

## Motion-rule check (v2)
- **Views:** 32 views in 53.6 s, average 1.7 s (range 1.0–2.4 s). The two shortest views (1.0 s and 1.1 s) are the trigger reaction (S05 V2) and the kid at the shore (S06 V2), both turn beats.
- **Hard cuts:** 0. Joins are follow, push-through, whip and dissolve, plus a fade-in at the start and a fade-out at the end.
- **Holds:** none; the final window views push in and pull back through the fade-out.
- **Lighting states:** LS1 grey rainy day, LS2 warm sunny sea, LS3 cool high sky, LS4 pale dawn shore, LS5 bright dry day, LS6 harsh noon glare, LS7 cold clear night, LS8 cool deep space. Day states sit near luminance 52–58, night near 38–42, dawn 45–50 (`visual-style.md`).
- **Depth:** each set has a foreground strip (window frame and sill, wave crests, cloud wisps, coastline, beach debris, reeds by the lake, cracked clods, rocks), a mid stage and a painted backdrop.

## Story-chain notes (script v1)
- **Hook (S01):** one raindrop on the kid's window, then the drop rewinds to the sea. The outcome (what happens without the sea) is withheld.
- **Context, setup and rule (S02–S04):** one loop, shown once: sea → vapor → droplets → cloud → wind → rain on the same window.
- **Trigger (S05):** "Now drain the ocean overnight." The sea drains in one move; the kid's shock pose is the turn.
- **Escalation (S06–S08):** the same path runs empty: nothing rises, a little rises from lakes, soil and plants (rule of three), the clouds thin, the ground cracks, one curl fizzles.
- **Reversal (S09):** "A clearer sky sounds calmer" is played deadpan; "But" lands as a cloud sliding off the sun and the glare snapping back.
- **Reveal (S10):** "It turns out": sunbeams bouncing off cloud tops in space, then pouring through the gaps onto bare ground (C9).
- **Consequence (S11):** hot, bright days and cold, clear nights, framed as "like a desert" (C10, a comparison, not a forecast).
- **Callback (S12):** back at the kid's window with a dry pane and a thin, bright sky: "The sky was running on the ocean all along."
- **Honesty labels:** everything after S04 is a hypothetical. The vapor is drawn as a faint shimmer because real vapor is invisible. No number, study or expert appears on screen. The heat beat shows sunlight reaching the ground, not a thermometer or a "hotter planet" claim.
- **Caption style:** `CAPTION-WORD-BY-WORD`, one word at a time, lower third, clear of the kid's face; the renderer splits words with `word-timings-v2.json`.

## Retention notes and risks
- **Opening:** the first image is a single drop on glass. It is calm; the rewind in V2 (about 1.5 s in) is the first surprise. If the opening feels slow in the preview, the rewind can start earlier.
- **Middle (S07–S08):** 11.4 s of the loop running down. Each view changes subject (lake, field, cloud, kid, sprinkle, cracks, fizzle) to keep it moving.
- **Sound:** rain patter, a rewind whoosh, waves, sparkle and cloud puff, wind, drop tap, drain glug, empty wind, soft pops, sprinkle, crackle, fizzle, a soft sting on "But", shimmer and beam zings, sizzle, night wind, a soft chime, and one music bed. The creator picks and edits sound in CapCut.

## Assets (sets and effects are planned; none exist yet)
- **Character (approved art):** CHAR-RAINKID: POSE-RAINKID-WINDOW, -SHOCK, -SHORE, -POINT-UP, -STAND (standing figure from the outfit sheet), -SHIELD, -FAN, -SHIVER; faces curious, shocked, worried, deadpan, squint, shiver, wistful; outfits indoor, rain, sun, night.
- **Sets (need set specs and a look test before building):** BG-WINDOW-RAINY (kid's room window; the same set dry in S12), BG-SEA-SUNNY, BG-HIGH-SKY, BG-COAST-TOWN, BG-SHORE-DRAINING, BG-SEABED-EMPTY, BG-INLAND (lake, field, tree), BG-DRY-PLAIN (day and night), BG-SPACE-EARTH.
- **Props and effects:** PROP-RAINDROP, PROP-CLOUD, PROP-CLOUD-LAYER, FX-VAPOR-CURLS, FX-DROPLETS, FX-RAIN, FX-WATER-DRAIN, FX-CRACKS, FX-SUN-FLARE, FX-SUNBEAMS, FX-HEAT-SHIMMER, FX-STARS-FROST.
- See `episode.json` for the asset IDs per shot.

## Open decisions for the creator (defaults stand if unanswered; a change after approval invalidates this storyboard)
1. **Ending image (S12):** a dry pane under a thin, bright sky (default, matches the script's beat map), or the real world back again: rain on the window and clouds over the sea.
2. **Standing pose in S09:** reuse the standing figure from the approved outfit sheet (default), or a new pose (needs an art batch).
3. **Space view (S10):** today's Earth with clouds and ocean (default, since it explains what clouds do now), or the drained Earth.

4. **CHAR-RAINKID on screen:** the narration no longer mentions anyone (script v2). Keep the kid visible behind the window and in the outdoor scenes (default, as approved in v1), or an empty window and no character.

## Changes from v1
- Re-timed to the script v2 narration: shot boundaries moved by up to 7 frames (S01 now 0–120, S12 1526–1607); view boundaries scaled inside each shot; sound cues moved with them.
- Narration text in S01, S04 and S10 follows script v2. Nothing else changed.

## Storyboard approval (artifact version, decision, timestamp)
Pending. Not approved.
