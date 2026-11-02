# CHAR-PIGEON: character spec v3 (APPROVED 2026-10-31; registered in character-registry.md)

Text spec only. No art has been generated. Per `character-registry.md`, this is **not** registered until the creator approves a version. Not part of any approval gate; editing it does not invalidate the script or storyboard.

## Role
Lead character of EP002 and a candidate recurring mascot. A calm, slightly deadpan pigeon who takes a ridiculous job seriously. Carries the humor through understatement (see `me.md`: curious, lightly humorous).

## Design intent
- Readable at a glance in 1080x1920 vertical, including at small scale inside a large set (S02, S07, S08 use scale contrast).
- Flat, bright, clean cutout character in front of richer layered backgrounds, per `visual-style.md` and the Ricks Clips *craft* notes.
- **Original.** Deliberately different from the reference channel's characters: no egg/bean head with dot eyes and stick limbs. This pigeon is plump and feathered with large glossy eyes, so it reads as a bird first.

## Visual description (proposed)
- **Silhouette:** plump, rounded body, short neck, small head, fan tail, thick short legs. Strong, simple shape that still reads in black-and-white.
- **Palette:** soft blue-grey body; iridescent neck patch in teal-to-magenta; slightly darker wing bars; coral feet; cream beak with a darker nostril patch; warm orange iris. Dark navy outline, consistent weight.
- **Face:** large round eyes with a visible pupil and a heavy upper eyelid (the main expression driver: wide, half-lidded, squint). Beak opens and closes for peck and speech-free reactions.
- **Texture:** minimal; a few feather tick marks on the wing and tail only.

## Layer breakdown (for 2.5D cutout rigging)
Body, head, neck sheen, left wing, right wing, tail, left leg/foot, right leg/foot, beak (closed/open), upper eyelids (L/R), pupils/irises (L/R), optional accessory layer. Original layered source files are kept; exports listed in `assets/asset-manifest.json` only after approval.

## Pose and expression inventory (from storyboard v1)
| Pose ID | Used in | Description |
|---|---|---|
| POSE-PIGEON-ALERT | S01 | Upright, eyes wide, head slightly forward, locked on target; second pose: small head tilt |
| POSE-PIGEON-WATCH | S02 | Settled on perch, head bobbing between two positions, calm eyes |
| POSE-PIGEON-PECK | S03, S04 | Pose A head back, pose B head forward with beak down; neck and body lean |
| POSE-PIGEON-PROUD | S06 | Chest puffed, eyelids half-lowered, small chin lift; hold |
| POSE-PIGEON-DEFLATED | S07 | Shoulders and tail drop, eyes half-closed, body sags |
| POSE-PIGEON-DEADPAN | S08 | Level stare toward camera, flat beak, single blink |

All character motion is poses on twos (about 12 effective fps); camera and parallax move at 24 fps (`motion-rules.md`).

## Allowed variations
Eye state (wide, half-lid, squint, closed; visible only when shades are SLID DOWN or OFF), shades state (on, slid down, off), beak (closed/open), scale. No change to silhouette, palette, or outline without a new version.

## Creator decisions (2026-10-31)
Creator accepted the proposals for decisions 1-4:
1. Body shape: **plump and round**.
2. Accessory: ~~none~~ **revised in v3: cool shades** (see Shades section). Creator request, 2026-10-31.
3. Eye style: **large glossy eyes with heavy upper lids**.
4. Palette: **soft blue-grey body, teal-to-magenta neck sheen, coral feet, cream beak, warm orange iris, navy outline**.

5. Art method: **AI-assisted** (creator decision, 2026-10-31).

## Shades (v3 change)
- **Design:** small, wide, flat-topped sunglasses sized for a pigeon head, with dark navy-black lenses, a thin bright frame (coral or cream to match the palette), and a single white glint mark. Simple shapes, same navy outline weight. Original design, not modeled on any real brand or character.
- **Problem:** lenses hide the eyes and lids, which were the main expression driver. **Fix:** expression moves to the beak, head tilt, neck, body posture, and the shades themselves.
- **Shade states (swappable layers):**
  - ON: default.
  - SLID DOWN: shades slip to the beak tip so the eyes show above them, used for surprise, pride, or a key reaction beat.
  - OFF: held away or absent, optional for a single close-up of the eyes.
- **Glint:** an optional lens glint layer used for reveals (pairs with the radial-glow FX in S06).
- **Layers added:** shades frame, left lens, right lens, glint, optional shadow on the face.
- **Tone:** shades add instant identity and dry humor and fit the deadpan personality. Risk: they can flatten emotional range, so use SLID DOWN sparingly for the beats that need eyes.

## Pose impact (from storyboard v1)
| Pose ID | Shades state | Expression carried by |
|---|---|---|
| POSE-PIGEON-ALERT (S01) | ON | Forward lean, head tilt |
| POSE-PIGEON-WATCH (S02) | ON | Calm head bob |
| POSE-PIGEON-PECK (S03, S04) | ON | Neck and body motion; one pigeon hesitates by a head tilt |
| POSE-PIGEON-PROUD (S06) | SLID DOWN | Eyes visible above the shades, chest puffed |
| POSE-PIGEON-DEFLATED (S07) | ON, slightly crooked | Sagging body, tilted shades |
| POSE-PIGEON-DEADPAN (S08) | ON | Level stare; strongest pose for shades |

The approved storyboard v1 describes eye details in a few `visual` and pose-action lines (for example S01 "eyes locked on target" and S07 "eyes half-closed" in this spec's own pose table). Those lines remain valid as the story, but if you want the written storyboard to match the shades exactly, that would be a storyboard v2 and needs re-approval. Not required.

## Rights / provenance (AI-assisted workflow requirements)
Before any art is used, record for each asset: the tool and model/version, the prompts and any reference images used, the tool's licence/terms of use for commercial use, creation date, and the source file paths. Keep original outputs and layered working files; never overwrite them.
- AI-generated images need to be separated into rig layers (body, head, wings, etc.). This is extra work, so the first generation step should target clean, flat, layer-friendly shapes.
- Copyright protection for AI-generated material varies by jurisdiction and may be limited; the creator should check the tool's terms and local rules before treating the mascot as an exclusive brand asset. This is not legal advice.
- Do not use real artists' names or the reference channel's characters as prompts or references, per the originality rule in `production-standards.md`.
- No art is generated until the creator gives an explicit go-ahead.

## Approval
Version: v3. Status: **approved** by Sean Caling, 2026-10-31. Registered in `character-registry.md`. No art exists yet.
