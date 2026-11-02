# Animation style notes: Ricks Clips (@RicksClips3000)

Notes on how these videos look and move, for making our own design decisions. They are **not** a template: don't copy his characters, layouts, or branding.

## v2: frame-by-frame analysis of three full Shorts (2026-11-01)

**Sources:** three files the creator downloaded and supplied (`videoplayback.mp4`, `videoplayback (1).mp4`, `videoplayback (2).mp4`). From the frames, they are the pirate cook pouring "storm oil", the horse race won by a milk cart, and the town built around a button. Each is 360x640 at 30 fps and about 64-66 s long, so they are YouTube's low-resolution download. Fine texture and small text could not be measured.

**Method:** every frame was decoded with OpenCV. I measured frame-to-frame pixel change, optical flow (how far the picture moves, and whether it zooms in or out), colour histograms compared 0.25 s apart (to find scene changes with any kind of transition), caption glyph size, and a k-means palette. I also looked at contact sheets (one frame per second) and frame-by-frame strips around transitions. The same measurements were run on our approved `EPISODES/EP002/animation-preview.mp4` for comparison.

**Limits:** these are low-resolution copies, so the numbers are approximate. The tools he uses are inferred from what the frames look like, not confirmed. I did not analyse the audio.

### Measured: Ricks Clips (three videos) vs EP002 preview v1
| Measure | Ricks Clips | EP002 v1 | Difference |
|---|---|---|---|
| Scene changes | 4.3-4.8 per 10 s | 2.3 per 10 s | about 2x as often |
| Median time on one view | 1.4-2.0 s | 4.25 s | about 2-3x shorter |
| Hard cuts | **0** detected in any video | 8 (every shot change) | he never hard-cuts |
| Median camera/picture motion | 30-36 px/s at 360 wide (~90-110 px/s at 1080) | 1.7 px/s at 360 wide (~5 px/s at 1080) | **about 20x more motion** |
| Frames that are nearly still | 10-14% | 61.5% | ours is mostly still |
| Frames with fast motion (>3 px/frame) | 23-31% | 1.3% | he whips the camera often |
| Frames zooming in / out | 45-61% in, 22-26% out | 8% in, 18% out | he is almost always pushing in |
| Frame rate | 30 fps, continuous | 24 fps, poses on twos | |
| Mean brightness (HSV value, 0-255) | 150-168 | 119 | ours is about 25% darker |
| Mean saturation (0-255) | 110-160 | 115 | similar, apart from the very saturated pirate video |
| Caption glyph height at 1920 tall | 38-41 px | 54 px | ours is about 1.4x larger |
| Caption word width | 18-22% of frame width | 29% | |
| Caption position (glyph rows) | about 61-71% of height | about 71% | similar |

**Palette (largest colour clusters).** Pirate: royal and ultramarine blue, rust red, warm orange, cream. Horse race: dark wine, olive, slate, terracotta, sky blue. Button town: indigo, grass green (`#5aae39`), warm grey, cream, amber. EP002: navy `#142539` and slate `#2d4a60` make up half of all pixels. **His frames span bright daylight to deep night within one video; ours stays in one dark blue mood throughout.**

### Observed: how the picture is made
1. **Real 3D sets, cartoon-shaded.** Ships, water, racetracks, grandstands, and towns are 3D environments with true perspective. The camera flies through them, orbits them, and looks down from above. They are toon-shaded, with painted textures (wood grain, brick, paper-like grain), ink outlines on the sets, depth of field, bloom, light shafts, and lamp glows. There are also effects simulations: water splashes, waves, rain, smoke, flying cash, confetti.
2. **Flat cut-out characters standing in 3D.** Characters are 2D drawings (white round heads, dot eyes, thick black outlines, stick limbs, tube bodies) placed as flat cards in the 3D set. When the camera orbits, they stay flat to the camera or turn as cards. Crowds are dozens to hundreds of these cards.
3. **Faces swap, bodies barely move.** Acting is mostly instant face swaps (brows, eye shapes, sweat drops, open-mouth laughs) and a few held arm poses. All the movement comes from the camera, not the character.
4. **The camera never stops.** Nearly every frame moves: slow push-ins on dialogue, fast whips and pans between subjects, overhead reveals of huge spaces, tracking alongside moving things (a horse, a cart).
5. **No hard cuts. Every change is one of three:**
   - **Follow-the-object.** The camera follows something into the next beat. Example (pirate, 0.6-3.3 s): oil pours from the pot, the camera rides the stream down the hull, it splashes, and the camera pans to reveal the pirate ship. Four beats in one move.
   - **Push through an object.** The camera dives into a lens, porthole, or window, then dissolves to what is seen through it (horse race, 12.5-13.2 s, through a magnifying glass).
   - **Short cross-dissolve while the camera keeps moving.** About 4-6 frames (0.15-0.2 s) (pirate, 5.9-6.1 s).
6. **Time of day and light change within a video.** Day becomes night, then sunrise; lamps switch on; a glowing ring in the sky. Lighting shifts mark story turns.
7. **Facts as objects, often in close-up.** Stopwatches (0047, 0048), odds boards, a "STORM OIL" can, a "FINISH" banner. The camera pushes in until the object fills the frame.
8. **Captions.** One or two words at a time, changing every ~0.2-0.4 s. White, heavy rounded sans-serif with a thin dark outline and soft shadow, centred, in the 61-71% height band. Smaller than ours.

### What this means for our style
The gap is mostly **motion and staging, not drawing**. Our flat-vector characters and props sit reasonably close to his character simplicity. The big differences:

| Area | EP002 now | Toward Ricks Clips |
|---|---|---|
| Space | Flat layered backdrops, small parallax | Deep 3D-feeling sets the camera can travel through |
| Camera | Slow eased creeps, mostly still | Always moving: push-ins, whips, orbits, overhead reveals |
| Changes | Hard cut per narration line (~4 s) | A new view every ~1.5-2 s, linked by follows, push-throughs, or 0.2 s dissolves |
| Holds | "Dead-still holds" (61% still frames) | Holds only on faces, and even then the camera creeps |
| Light | One dark navy mood | Light and time of day change per beat; brighter overall |
| Acting | Rig poses on twos | Fast face swaps; body stays simple |
| Captions | 54 px glyphs | About 40 px, 1-2 words per change |

**Conflict with current rules:** `motion-rules.md` and the 3D cartoon reference notes call for dead-still holds and poses on twos. This analysis shows a style built on near-constant camera motion. Changing the motion rules is the creator's decision, and they stay as they are until changed.

**What our Remotion setup can and can't do:** 2D layers can imitate most of this: bigger and faster camera moves, more layers with stronger parallax, an orbit faked with scaling and skew, push-through-object transitions, light-and-colour grading per beat, and particle effects. Real 3D sets with orbiting cameras would need a 3D tool, such as Three.js inside Remotion or Blender. That is a separate decision with real cost.

## v1 notes (2026-10-31, seven stills; kept for history)
- Simple characters in rich environments; role shown by accessories; scale contrast; light as story; facts on props and signs; bold word-by-word captions; saturated palette.
- v1 could not see motion; v2 above replaces its guesses about motion with measurements.

## Boundaries
- Do not copy his character shapes, accessories, colour combinations, scene layouts, or caption styling as a branded look. Create original characters (new ones need creator approval in `character-registry.md`) and our own design system.
- The tools he uses are inferred from frames, not confirmed.
- Do not claim this look drives views.
