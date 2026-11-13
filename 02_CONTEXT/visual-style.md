# Visual style (v4)

**Status:** v4 approved by the creator (Sean Caling) on 2026-11-13 for use from EP005 onward. Approvals, in order: look test v1 ("I approve this look"), the bean build ("Bean build (v2)"), dense sets with mood lighting ("Yes, dense and moody"), the motion test ("I approve it"). EP002, EP003 and EP004 are published and do not change.

**Under test:** the creator's rule is to test every change before it becomes permanent. v4 is the look the next episodes are made in, and its results are tracked in `03_TRACKING/format-tests.md` (rows 10, 11 and 14). If the results say so, v4 changes.

**One line:** a flat-colour cartoon world in 3D. Real 3D characters with painted, swappable faces act in dense, dressed sets, lit for mood, with one ink line over everything.

**Look tests:** `renders/lookdev-3d/`, `renders/lookdev-3d-v2/`, `renders/motion-test-3d/` (git-ignored). **Code:** `renderer-blender/toon3d.py` (shading, character, glow), `toon_sets.py` (shared sets and lighting states), `scripts/paint_faces3d.py` (faces).

## 1. Build
- **Sets are 3D** (Blender). The camera can travel through them, orbit and look down.
- **Characters are 3D too.** No flat cutout cards for characters: a card hides the ink lines behind its invisible rectangle (the "box" the creator saw in EP004) and slides when the camera moves.
- Delivery is 1080×1920 vertical. Keep the focal action and the captions inside the safe margins.

## 2. Characters (3D, bean build)
- Every character is original. A new one needs the creator's approval in `character-registry.md`. Reference channels show a construction method only; never copy their characters.
- **Build:** a large egg head (about a third of the height), one long bean body in a single colour with two or three details (buttons), thin dark limbs, small ball hands and small shoes, hair or a cap as a simple shape.
- **Face:** eyes, brows, mouth and cheeks painted on the front of the head and swapped per expression. Eye whites keep faces readable on every skin tone. Ten faces exist: neutral, happy, laugh, surprised, worried, nervous, deadpan, smug, squint, blink. No lip-sync.
- **Variants** are colour settings: skin tone, hair or cap, body colour, shoes.
- **Light:** characters take the scene's light and cast real shadows. Skin shadows are softened so the face stays clear.
- **Acting:** see `motion-rules.md`.

## 3. Sets (dense and dressed)
- **Flat colour fills.** No painted brush texture.
- **Dense with story props.** A set never starts from an empty floor: shelves, tools, furniture, plants and street furniture specific to the story.
- **Readable signs and labels inside the scene** carry facts (a shop sign, a jar label, a poster).
- **Skies are clean gradients** set per lighting state; stars, moon and sun are simple shapes.
- **Depth:** foreground objects near the lens, a mid stage for the characters, a background (wall, shopfronts, skyline).

## 4. Light, shading and colour
- **Two tones plus a highlight.** Each surface shows its fill colour, one hard-edged shadow tone tinted cool, and a brighter highlight where the light is strongest.
- **Ink outline on everything 3D,** sets and characters alike: navy-brown `#2B2238`, about 5 px on outer edges and 3 px on folds at 1080 wide. Not inked: glowing things (bulbs, neon, lit windows), signs' letters, the sky.
- **Mood lighting.**
  - Sun through blinds or windows draws stripes across the room.
  - Lamps, neon signs and lit windows glow (a glow pass) and tint what they light with their own colour.
  - At night only lamps, signs and windows reach the lit tone; everything else sits in the cool shadow tone.
  - Soft focus behind the subject on medium and close shots; a soft vignette.
- **Lighting states so far** (in `toon_sets.state`): warm interior, night street, plain studio. Each episode uses at least two states, and a change of light marks a story turn.
- **Colour targets** (measured on the look tests): mean saturation about 100–160 of 255; brightness about 50–70 of 100 for lit interiors and about 30–50 for night. Whites clipped on under 0.5% of pixels.

## 5. Clean frame
- **No game or app interface:** no speech bubbles, dialogue boxes, health bars, menus, title cards or watermarks.
- On-screen text appears in two ways:
  - **Captions.** The motion rules cover them.
  - **In-world objects:** signs, stamps, labels, screens or calendars.
  A third way, an on-screen number or icon for each spoken figure, is under test (`format-tests.md` row 9).

## Known limits (2026-11-13)
- Shop windows are flat bright panels.
- A face falls into the shadow tone when the only light is behind the character.
- With many lamps, Blender's shadow buffer fills and some lamp shadows may be missing.
- When the head turns far, the painted face slides toward the side of the head.

## References (craft only; never copy characters, sets, logos or branding)
- Frame-by-frame analysis of three reference channels: `source-analysis/reference-video-analysis-2026-11-13.md`.
- Earlier notes: `source-analysis/animation-style-notes-ricks-clips.md`, `animation-style-notes-3d-cartoon-reference.md`, `animation-style-notes-papercraft-reference.md` (the v2–v3 look).

## History
- **v3 (2026-11-03):** cel-shaded papercraft: flat cutout character cards in hand-painted 3D sets, three hard light bands, ink outlines on sets. Used for EP003 and EP004.
- **v2 (2026-11-02):** papercraft look: soft, gentle shading with no hard light-to-shadow line, and ink outlines only on characters and cutout props. Used for EP003 S01–S04 as first approved.
- **v1 (2026-10-31):** "Bright, clean, colorful illustrated cutout scenes with layered depth, expressive original characters, readable shapes, purposeful textures, and controlled parallax." It was used for EP002 and rendered in Remotion 2D, and later redone as a Blender 3D draft.
