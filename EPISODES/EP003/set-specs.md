# EP003 set and background specs v1 (APPROVED by Sean Caling, 2026-11-02: "Approve set specs v1")

**Superseded in part by visual-style v3 (cel look), approved 2026-11-03.** Sets and 3D props now carry ink outlines (about 5 px outer, 3 px creases), and light falls into three hard tones. This replaces shared rules 3 and 4 and the "Set outlines: none" check below. Everything else here still applies.

**Creator direction (2026-11-02):** "Background assets must have a similar aesthetic as the paper mario."

This spec turns that direction into checkable rules for EP003's sets. It follows `02_CONTEXT/visual-style.md` v2 and the measured reference in `02_CONTEXT/source-analysis/animation-style-notes-papercraft-reference.md`. It borrows the reference's **look principles** only: painted texture, soft light, scene-wide colour mood and diorama depth. Every set, prop and shape is our own design: no copied buildings, pipes, blocks, castles, logos or level layouts. No set art exists yet.

## Shared look for every set
1. **Toy-diorama shapes.** Chunky, simplified 3D forms with softly rounded edges (small bevels) and slightly exaggerated proportions: thick window frames, puffy trees, rounded roofs and rocks. Nothing razor-sharp or realistic.
2. **Painted, never plastic.** Every surface has a hand-painted texture:
   - wood grain on wood
   - plaster mottling on walls
   - sand speckle on beaches
   - brushy streaks on water and snow
   - soft cloud strokes in skies

   No flat untextured fills, no glossy or metallic highlights. Textures are painted images (made procedurally plus brush-stroke detail), not plain noise.
3. **No ink outlines on sets.** Only characters and printed cutout props (poster, paper stamp, timeline card, age tags) carry the soft navy-brown outline.
4. **Soft, high-ambient light.** Shading falls off gently, with corners slightly darker and walls fading top to bottom. There are no hard shadow edges and no clipped whites. Characters get only a soft contact shadow.
5. **Mood from a whole-scene colour grade**, set by the storyboard's lighting states (below). The light changes; the paint does not.
6. **Painted backdrops** for skies and far views: flat painted cloud, star and horizon cards behind the 3D set, seen through windows and past the mid stage.
7. **Three layers, every set:**
   - A **foreground strip** the camera moves past.
   - A **mid stage** where characters stand.
   - A **painted backdrop**.

   Draped fabric or beams may frame the top.
8. **Rich, friendly colour.** Saturated but not neon, with warm cream and amber in day scenes and blue-violet at night or in space. Deep blacks only in space.

## Acceptance checks (measured on test stills before full builds)
| Check | Target | Reference (measured) |
|---|---|---|
| Lightness L*, day sets (LS1) | 52–58 | 53.5–57.3 |
| Lightness L*, cool or night sets (LS2, LS5) | 38–45 | 39.7 |
| Mean saturation (HSV, 0–255) | 95–125 | 94–123 |
| Deep blacks, day sets | ≤ 2% of pixels | 0.1–0.2% |
| Clipped whites | 0% | 0% |
| Edge density (painted detail) | 6–10% | 7.9–9.7% (our earlier procedural test: 1.7–3.6%) |
| Set outlines | none | none |

Edge density is the main gap from our earlier test, which is why the textures must be painted images with brush detail, not plain noise.

## Sets (from approved storyboard v2)
| Set ID | Used in | Lighting state | Foreground strip | Mid stage | Painted backdrop |
|---|---|---|---|---|---|
| BG-BEDROOM-MORNING | S01, S10 | LS1 warm morning (S10: LS8 pale dawn) | Bedside shelf with the desk globe and a toy; thick fabric curtains | Window seat and floor where the kid stands; wallpaper with a soft painted pattern | Blue sky with painted clouds through the window |
| BG-ROOFTOPS-MORNING | S02 | LS1 | Chunky chimney and roof tiles crossing the frame | Rows of rounded rooftops seen from below | Bright sky backdrop; the rock ring in front of it |
| BG-BEACH-EQUATOR | S04 V1–V2 | LS1 | Puffy palm fronds | Sand with painted speckle, a few shells | Turquoise sea with brushy wave strokes, painted sky |
| BG-CITY-ROOFTOP | S04 V3–V4 | LS1 | Rooftop railing and potted plants | Flat rooftop with water tank and chimneys | Painted city skyline and sky with the ring's arch |
| BG-NORTH-TOWN-SNOW | S04 V5–V6 | LS5 cool low sun | Snow bank and a short wooden fence | Snowy lane with two or three rounded wooden houses | Pale painted sky low over hills; no ring |
| BG-SPACE | S03, S05–S09 | LS2 cool deep space (S06 V4: LS6 warm glow) | Drifting rock fragments (S06, S08) | The globes and the ring | Painted star field and soft nebula clouds |
| BG-SEAFLOOR | S09 V3 | LS7 teal ancient sea | Ferns, sponges and rounded rocks | Sandy seabed where the trilobite sits | Rippled water surface with the ring seen through it |
| BG-DAWN-PLAIN | S09 V4 | LS8 pale dawn | Tall grass clumps and a rock | Open plain where the dinosaur walks | Painted dawn sky, empty, with a soft sun glow |

## Key props in the same aesthetic
- **3D, painted, no outline:**
  - **PROP-GLOBE-DESK, PROP-GLOBE-PINS, PROP-GLOBE-ANCIENT:** painted globes with soft brushy continents. The ancient globe has unfamiliar landmasses and must not claim to be an accurate Ordovician map.
  - **PROP-ASTEROID:** a lumpy, rounded rock.
  - **PROP-ROCK-RING:** chunky tan-grey rock pieces.
- **Printed cutouts, outlined like characters:**
  - **PROP-SATURN-POSTER:** a painted Saturn with white icy rings.
  - **PROP-PAPER-STAMP:** "A STUDY SUGGESTS".
  - **PROP-TIMELINE-CARD:** "466 MILLION YEARS AGO".
  - **PROP-AGE-TAGS:** "466?".
- **Fabric:** PROP-CURTAINS are thick, soft painted fabric with gentle folds.
- **Effects:** FX-RING-FORM, FX-RING-FADE, FX-DEBRIS-FALL, FX-CRATER-DOTS, FX-GHOST-RING and FX-ICE-SUN-INSERT are soft, painterly glows and streaks. No realistic particle simulation.

## Proposed build order (each step needs the creator's go-ahead)
1. **Look test:** build BG-BEDROOM-MORNING with the kid card, render 2–3 stills, and run the acceptance checks above. The creator compares them with the reference.
2. **Remaining day sets:** rooftops, beach, city rooftop.
3. **Cool and ancient sets:** north town, space, seafloor, dawn plain.
4. **Props and effects.**

## Decisions for the creator
1. **Look test first** (recommended), before more character batches? Or finish character batch 2 first?
2. **Storybook opener frame** (an optional rule in visual-style v2): the storyboard has none. Keep it that way (default), or add one, which would change the storyboard?

## Status
Version: v1. **Approved** by Sean Caling on 2026-11-02 ("Approve set specs v1"). Decision 2 default stands: no storybook opener, so the storyboard is unchanged. Decision 1 (look test first or kid batch 2 first) is still open. Nothing has been built or rendered; each build step needs its own go-ahead.
