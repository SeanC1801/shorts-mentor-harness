# Animation style notes: papercraft storybook reference (Paper Mario, N64 opening)

Source: one 12m24s gameplay capture of the opening of *Paper Mario* (Nintendo / Intelligent Systems, 2000), 640×360, 30 fps, supplied by the creator 2026-11-02. Measured with OpenCV at 2 samples/s (1,488 samples), plus full-resolution and 4× nearest-neighbour crops.

**Use:** craft principles for lighting, materials and depth only. Do not copy its characters, sets, props, logos, curtain frame design, or UI. All FooFilms characters and sets stay original.

## What to keep vs remove
| Keep (world look) | Remove (game HUD and game-only behaviour) |
|---|---|
| Flat cutout characters in 3D sets | Speech bubbles and dialogue boxes |
| Painted, soft-lit sets | HP/FP status bar, item counters, damage numbers |
| Per-scene colour mood | Menus, title card, "press start", end screens |
| Foreground framing layers | The game's static follow camera (see Camera) |
| Soft contact shadows | Pixel-art text font |

## Measured
| Segment | Lightness L* | L* spread | Saturation (0–255) | Warm/cool (b*) | Deep blacks | Clipped whites |
|---|---|---|---|---|---|---|
| Storybook prologue | 47.6 | 16.5 | 98 | −9.4 (cool) | 0.8% | 0.0% |
| Day exterior / town | 53.5 | 19.2 | 123 | +14.7 (warm) | 0.2% | 0.0% |
| Castle day interior | 57.3 | 17.0 | 94 | +10.5 (warm) | 0.1% | 0.0% |
| Castle night / boss | 39.7 | 20.0 | 105 | −0.7 (neutral-cool, a* +7) | 7.7% | 0.0% |
| **FooFilms EP002 3D v2** | 39.8 | 20.0 | 123 | — | 10.0% | — |

Edge density (Canny, share of pixels): reference day 9.7%, night 7.9%; EP002 3D v2 3.2%. The reference surfaces carry painted texture detail; ours are flat fills.

Camera (gameplay only): median motion 0 px/s; 59–76% of samples nearly still. This is a player-follow camera and is **not** the motion model for FooFilms.

## Observed
1. **Characters are flat paper sprites.** Always face camera, no real-time shading. Shading and highlights are painted into the art. Dark warm-brown/navy outline about 2–3 px at 360p (about 0.7% of frame height), slightly soft.
2. **Soft oval contact shadow** under every character's feet; floor is visibly darker directly under feet. No cast shadows from characters onto walls.
3. **Sets are 3D geometry with painted textures.** Wood grain, stone, plaster and cloth are painted with soft gradients and baked darkening in corners. Set geometry has **no ink outlines**; only characters are outlined.
4. **Lighting is soft and high-ambient.** No hard shadow edges anywhere. Walls fall off gently top-to-bottom. Whites never clip and blacks are rare in daytime.
5. **Mood comes from a whole-scene colour grade.** Day sets are warm (b* +10 to +15). Night sets drop about 15 L* and go blue-violet, with small warm point accents (candles, window glow).
6. **Skies are painted backdrops**: flat cloud and star paintings seen through windows and behind sets.
7. **Layered diorama depth.** A foreground strip (flowers, bushes, railings) along the bottom edge, a mid stage where characters stand, and a painted backdrop. Draped fabric (curtains, valances) frames the top.
8. **Storybook framing in the prologue.** The intro is staged as a theatre: proscenium curtain, side pillars, checker floor. This is the clearest "paper storybook" signal and suits openings.

## Implications for FooFilms (adopted in `visual-style.md` v2, 2026-11-02)
- Characters: keep original flat cutout cards with painted-in shading and a soft dark outline. Add a soft oval contact shadow on the floor under each.
- Sets: drop ink outlines from set geometry. Replace the hard two-step toon ramp with soft painted shading and subtle painted texture (grain, plaster mottling).
- Lighting: high ambient, soft or no cast shadows, no clipped whites. Grade each scene as a whole: day warm and lighter (target L* 52–58), night cool and darker (target L* 38–42) with warm practical accents.
- Depth: every set gets a foreground strip, a mid stage and a painted backdrop.
- Optional: open an episode on a storybook-stage frame of our own design.
- Camera and captions stay on Ricks Clips and Zack D. Films principles (`animation-style-notes-ricks-clips.md`, `narration-style-notes*.md`): continuous moves, a scene change every 1.4–2.0 s, no game HUD or speech bubbles, word-by-word captions in the lower third.
