# Visual style (v3)

**Status:** v3 approved by the creator (Sean Caling) on 2026-11-03 ("Approve cel look"). The creator had asked earlier that day: "try and apply Cel Shading to every video now". They chose hard light bands plus ink outlines over the painted textures. v3 applies to EP003 onward. EP002 is published and does not change. Look test: `renders/ep003-cel-lookdev/`.

**One line:** a cel-shaded papercraft storybook world. Flat, original cutout characters stand in hand-painted 3D sets with hard cartoon light bands and ink outlines. The camera is always moving, and captions run word by word.

## 1. Build
- **Sets are 3D** (Blender). They are real spaces the camera can travel through, orbit and look down on.
- **Characters and printed props are flat cutout cards.** Draw them in 2D, place them in the 3D set, and keep them turned toward the camera.
- **Big story objects can be 3D models** built from their approved 2D designs. Examples: machines, vehicles, the key invention.
- Delivery is 1080×1920 vertical. Keep the focal action and the captions inside the safe margins.

## 2. Characters (cutouts)
- Every character is original. A new one needs the creator's approval in `character-registry.md`.
- **Readable shapes:** simple silhouettes, with the role shown by an accessory or prop.
- **Paint the shading into the art.** Cutouts get no scene lighting except the scene's colour grade.
- **Outlines:** a soft dark outline (warm brown or navy, never pure black) about 0.7% of the frame height. Characters keep the heaviest line in the frame, so they read in front of the inked sets.
- **Contact shadow:** a soft dark oval on the floor under every standing character or prop, around 35–40% opacity at the centre and fading to nothing at the edge. Never a hard cast shadow.
- **Acting:** instant face and pose swaps. Bodies stay simple, and the camera does most of the acting.

## 3. Sets (painted 3D)
- **Painted, not plastic.** Every surface carries soft painted texture: wood grain, plaster mottling, paper grain or fabric. There are no flat untextured fills and no glossy highlights.
- **Cel light (v3).** Light falls into three flat tones with hard edges between them:
  1. a warm light tone
  2. a neutral mid tone
  3. a cool violet shadow tone

  Ambient occlusion snaps to one contact-shadow step. Tones multiply the painted texture, so the paint shows through every band.
- **Ink outlines on 3D sets and props (v3).** Navy-brown `#2B2238`, never pure black.
  - Outer edges (silhouettes, borders) are about 5 px at 1080 wide.
  - Inner folds and creases are about 3 px.
  - Not inked:
    - painted backdrops (sky, clouds, stars)
    - glows, light shafts and sparkles
    - see-through rings and haze
    - the cutout cards themselves, which carry their own drawn outlines
- **Skies and far views are painted backdrops** (clouds, stars, horizons) seen through windows and behind the set.
- **Three-layer diorama, every set:**
  1. A **foreground strip** along the bottom or side edge, such as plants, railings, a desk edge or crates. The camera passes it for depth.
  2. A **mid stage** where the characters stand.
  3. A **painted backdrop**.
- Draped fabric, signs or beams can frame the top of the shot.
- **Optional storybook opener:** an episode can open on a stage or picture-book frame of our own design, then push through it into the story.

## 4. Light and colour
- **High ambient light.** Whites never clip. Deep blacks are rare in day scenes: at most about 2% of pixels.
- **Mood comes from a whole-scene colour grade, not from strong shadows.** Each episode uses at least two lighting states, and a change of light marks a story turn.

  | State | Lightness (L*, 0–100) | Colour cast | Accents |
  |---|---|---|---|
  | Day / interior | 52–58 | Warm (cream, amber) | Window light |
  | Night / dark interior | 38–42 | Cool blue-violet | Small warm practical lights: lamps, candles, screens |
  | Dusk / reveal | 45–50 | Orange sky over cool ground | Sun disc, runway or street lights |

- **Saturation:** rich but not neon. Mean HSV saturation is roughly 95–125 out of 255.
- **Starting points per pillar** (the creator chooses per episode):
  - **Weird Technology:** a workshop or lab by day with a cool screen glow, ending on a dramatic dark test.
  - **Strange History:** a warm period interior or a sunlit landscape, with a storybook opener where it fits.
  - **Scientific What-If:** a familiar daylight world, then a shift (night, space, extreme scale) once the "what if" happens.

## 5. Clean frame
- **No game or app interface:** no speech bubbles, dialogue boxes, health bars, counters, menus, title cards or watermarks.
- On-screen text appears in only two ways:
  - **Captions.** The motion rules cover them.
  - **In-world objects:** signs, stamps, labels, screens or calendars, with the camera pushed in until the fact fills the frame.

## References (craft only; never copy characters, sets, logos or branding)
- Lighting, materials and depth: `source-analysis/animation-style-notes-papercraft-reference.md`.
- Camera, transitions and staging: `source-analysis/animation-style-notes-ricks-clips.md`.
- Earlier 3D cartoon notes: `source-analysis/animation-style-notes-3d-cartoon-reference.md`.

## History
- **v2 (2026-11-02):** papercraft look: soft, gentle shading with no hard light-to-shadow line, and ink outlines only on characters and cutout props. Used for EP003 S01–S04 as first approved.
- **v1 (2026-10-31):** "Bright, clean, colorful illustrated cutout scenes with layered depth, expressive original characters, readable shapes, purposeful textures, and controlled parallax." It was used for EP002 and rendered in Remotion 2D, and later redone as a Blender 3D draft.
