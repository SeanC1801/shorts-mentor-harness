# EP004 set and background specs v1 (APPROVED by Sean Caling, 2026-11-11: "Approve set specs v1")

Covers the nine sets plus the props and effects in approved storyboard v1. No set art exists yet. Nothing is built until the creator approves this spec, and a look test comes before the full builds.

**Look:** `02_CONTEXT/visual-style.md` v3, the cel look approved for EP003 onward. Painted 3D sets get three hard light bands (warm light, neutral mid, cool violet shadow) multiplied over painted texture. Ink outlines in navy-brown `#2B2238` are about 5 px on outer edges and about 3 px on creases at 1080 wide. Skies, glows, haze and sparkles are not inked. The papercraft diorama principles from EP003's set spec still apply: toy-diorama shapes, painted textures, three layers and a scene-wide grade.

**Build:** new EP004 files only (`renderer-blender/ep004_sets.py`, `ep004_props.py`, `ep004_render.py`). EP003 is posted, so its files are not edited. The shared helper library `papercraft.py` may gain new functions, but its existing functions are not changed, so EP003 still renders exactly as approved.

**Character in the sets:** CHAR-RAINKID is a flat cutout card turned to the camera with a soft contact shadow. Its 1% outline is the heaviest line in the frame, so it reads in front of the inked sets.

## Lighting states (from the storyboard)
| State | Used in | Lightness target (L*) | Colour cast | Accents |
|---|---|---|---|---|
| LS1 grey rainy day | S01 V1–2, S04 V2 | 50–55 | cool grey-blue outside, warm lamp glow inside the room | wet glints on glass and roofs |
| LS2 warm sunny sea | S01 V3, S02 | 54–58 | warm cream and turquoise | sun disc, glints on waves |
| LS3 cool high sky | S03, S04 V1 | 52–56 | cool blue, white cloud | droplet sparkles |
| LS4 pale dawn shore | S05 | 45–50 | peach sky over cool ground | low sun on the horizon |
| LS5 bright dry day | S06–S09, S12 | 54–58 | pale blue sky, sandy ochre ground | thin wispy clouds only |
| LS6 harsh noon glare | S09 V2, S10 V3–4, S11 V1 | 56–60, no clipped whites | bleached yellow-white sky, hot ochre ground | sun flare, heat shimmer |
| LS7 cold clear night | S11 V2–3 | 38–42 | deep blue-violet | stars, frost glints |
| LS8 cool deep space | S10 V1–2 | 30–40 (deep blacks allowed) | black-blue | sun, bright cloud tops |

A change of light marks each story turn: rain to sun (S01 to S02), dawn drain (S05), noon glare (S09 "But"), and day to night (S11).

## Sets
| Set ID | Used in | Foreground strip | Mid stage | Painted backdrop | States |
|---|---|---|---|---|---|
| **BG-WINDOW-RAINY** | S01 V1–2, S04 V2, S12 | Outside the house: chunky window frame and sill, a dripping gutter at the top edge, rain streaks on the glass | The glass with the kid behind it (indoor outfit); behind the kid, the room: a warm lamp, a bookshelf, a striped curtain | Inside: painted room wall. Outside, when the camera tilts up: wet rooftops of neighbouring houses and a grey sky card | **Rainy** (LS1: drops on the glass, wet sill). **Dry** (LS5, S12: clean pane, bright thin sky, no drops) |
| **BG-SEA-SUNNY** | S01 V3, S02 | Big wave crests passing close to the lens | Open sea: low-poly wave surface with cel bands, slowly rolling, glinting | Sun disc low in a warm sky, a faint horizon line | One state (LS2) |
| **BG-HIGH-SKY** | S03, S04 V1 start | Cloud wisps drifting past the lens | Open air for the vapor curls, droplets and the forming cloud | High sky gradient card, the sea far below seen through gaps | One state (LS3) |
| **BG-COAST-TOWN** | S04 V1–V2 | Cloud wisps (above); treetops (as the camera drops) | Aerial coastline: sea, beach strip, a small town of 10–14 chunky houses, the kid's house marked by the same window and colours as BG-WINDOW-RAINY | Hills and a grey-blue sky card | **Clouds arriving** (LS3) to **raining** (LS1) |
| **BG-SHORE** (serves BG-SHORE-DRAINING and BG-SEABED-EMPTY) | S05, S06 | Dune grass, a short wooden fence, a beach bucket | A sloping beach and the seabed below it: wooden jetty posts, a small rowboat, rocks, shells, drying seaweed, sand ripples | Dawn sky card (S05); bright sky card (S06); the far rim of the empty seabed bowl | **Full sea** (water plane at the shoreline) → **draining** (water plane drops and slides away in S05) → **empty** (S06: damp sand fading to dry, boat on its side, no water). One Blender set with two storyboard IDs |
| **BG-INLAND** | S07, S08 | Reeds at the lake edge, clods of soil, a fence post | A small lake, a ploughed field with soil rows, one puffy tree, a low hill | Pale sky card with patchy clouds | **Green** (S07: lake full, tree leafy, field dark and moist) → **drying** (S08: lake shrunk with a dry rim, field cracking, tree leaves fewer and browner, plants drooping). LS5 throughout |
| **BG-DRY-PLAIN** | S09, S10 V4, S11 | Cracked clods and small rocks | A flat cracked plain, a few dry shrubs, one bare tree, a round boulder | Day: low flat-topped hills and a bleached sky card. Night: the same hills in silhouette and a star card | **Bright day** (LS5) → **noon glare** (LS6, heat shimmer) → **cold night** (LS7, frost glints, stars) |
| **BG-SPACE-EARTH** | S10 V1–V2 | Faint drifting dust specks near the lens (not inked) | Today's Earth: ocean and continents with a separate white cloud shell above the surface; at closer range, the cloud layer as a parasol with its shadow on the land | Star card; the sun as a bright disc at the frame edge | One state (LS8) |

Nine storyboard set IDs are covered: BG-WINDOW-RAINY, BG-SEA-SUNNY, BG-HIGH-SKY, BG-COAST-TOWN, BG-SHORE-DRAINING and BG-SEABED-EMPTY (one build), BG-INLAND, BG-DRY-PLAIN and BG-SPACE-EARTH.

## Props and effects
| ID | Used in | Description | Inked? |
|---|---|---|---|
| PROP-RAINDROP | S01, S04 | One hero raindrop: a clear teardrop with a white highlight and a soft refraction tint, big enough to read on the glass | Yes, thin |
| PROP-CLOUD | S03, S04, S07–S09 | Puffy cartoon cloud built from overlapping spheres, cel-banded white to lavender shade; it can thin out (spheres shrink and gaps open) | Yes |
| PROP-CLOUD-LAYER | S10 | A wide sheet of the same cloud style over the land, with a visible shadow beneath | Yes |
| FX-VAPOR-CURLS | S02, S03, S07, S08 | Faint, see-through rising curls with a shimmer (stylized: real vapor is invisible); they slow and sparkle into droplets in S03, and one fizzles out in S08 | No |
| FX-DROPLETS | S03 | Tiny sparkling beads that drift together and clump into PROP-CLOUD | No |
| FX-RAIN | S04, S08 | Rain streaks (heavy in S04, a sparse sprinkle in S08) | No |
| FX-WATER-DRAIN | S05 | The sea's water plane dropping and sliding away over 1 s, with a foam edge | Water edge only |
| FX-CRACKS | S08, S11 | Crack pattern that grows across the soil (texture reveal plus raised clods) | Yes, crease weight |
| FX-SUN-FLARE | S09 | Lens flare and glare bloom; a thin cloud slides across the sun and the light dims, then snaps back | No |
| FX-SUNBEAMS | S10 | Soft arrows of light: they bounce off cloud tops back to space, then pour through gaps onto the ground | No |
| FX-HEAT-SHIMMER | S10, S11 | Wavy distortion band above the ground | No |
| FX-STARS-FROST | S11 | Twinkling stars on the night card and small frost glints on the cracks | No |

## Acceptance checks (measured on look-test stills before full builds)
| Check | Target |
|---|---|
| Lightness L* per state | the targets in the table above |
| Mean saturation (HSV, 0–255) | 95–125 (LS6 glare may dip to about 85; LS8 space excluded) |
| Deep blacks, day sets | at most 2% of pixels |
| Clipped whites | 0% (the LS6 glare must still stay below clipping) |
| Ink outlines | about 5 px outer and 3 px creases at 1080 wide, navy-brown; none on skies, glows, haze or effects |
| Light bands | three hard tones visible on set forms |
| Character readability | CHAR-RAINKID reads at 150 px tall against each set, and its outline is the heaviest line in the frame |

## Look test (next step, needs its own go-ahead)
Default: **BG-WINDOW-RAINY in both states**, with the kid behind the glass. It's the first and last image of the episode, and the hardest mix: glass, rain, an interior and an exterior. A second still of **BG-SHORE draining at dawn** would test water and the LS4 grade.

## Decisions for the creator
1. **Kid's house colours:** soft yellow walls with a teal window frame (default), or name others. The same house must read from the air in S04.
2. **One shore set for S05 and S06** (default), as above.
3. **Look-test choice:** the window set in both states (default), with or without the second still of the draining shore.

## Status
Version: v1. Approved by Sean Caling, 2026-11-11 ("Approve set specs v1"); defaults kept: yellow house with a teal window frame, one shore set for S05 and S06, look test of the window set in both states. Next: the look test, with a separate go-ahead.
