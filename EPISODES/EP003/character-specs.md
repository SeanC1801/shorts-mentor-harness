# EP003 character specs v1 (APPROVED by Sean Caling, 2026-11-02: "Approve character specs v1")

Covers the three new characters in approved storyboard v2: **CHAR-KID**, **CHAR-TRILOBITE** and **CHAR-DINO**. No art exists yet. Nothing goes into `02_CONTEXT/character-registry.md` until the creator approves these specs, and no art is made without a separate go-ahead for each batch.

**Creator choices (2026-11-02):**
- **Kid style:** paper-cut chibi.
- **Kid identity:** neutral, so any viewer can project onto it.
- **Outfit:** orange hoodie.
- **Creatures:** cute, in the same simple style as the kid.

**Style sources:**
- **Characters:** Ricks Clips *principles* only. Very simple flat cutouts, acting through instant face swaps, and the role shown by one prop or outfit.
- **Sets:** the papercraft lighting and set principles in `visual-style.md` v2. Painted soft-lit 3D sets with no outlines, a foreground strip, and a painted backdrop.

## Shared rules (all three)
- **Flat paper cutouts** standing in the 3D sets and turned toward the camera. Shading is **painted into the art**: one soft shade tone and one small highlight per shape. Cutouts take no scene lighting except the scene's colour grade.
- **Outline:** soft dark navy-brown `#2B2238`, never pure black. Weight is about 0.7% of the frame height at the character's usual size, slightly thicker on the outer silhouette than on inner lines. Only characters and cutout props are outlined; the sets are not.
- **Paper feel:** a faint paper-grain texture inside the fills, at about 5% opacity, so the cutouts belong in the papercraft world.
- **Contact shadow:** a soft dark oval under the feet, about 35–40% opacity at the centre and fading to nothing. Never a hard cast shadow.
- **Acting:** expressions and poses swap instantly and hold at least 2 frames (motion rules v2). Bodies stay simple; the camera does most of the moving.
- **Readability test:** each character must still read when it is about 150 px tall in a 1080×1920 frame. In S04 V1 and S09 V3 they are small in the shot.
- **Build:** each character is a layered vector source with named parts (head, face parts, body, arms, legs, prop). Poses are made by moving and swapping parts on one rig, so proportions stay identical between poses.

## How these differ from Ricks Clips' characters (required: original designs)
| Ricks Clips signature (do not copy) | FooFilms EP003 |
|---|---|
| White round head | Skin-toned round head with a hair tuft |
| Dot eyes | Tall oval eyes with a highlight, plus small eyebrows that carry most of the expression |
| Thick black outline | Soft dark navy-brown outline, medium weight |
| Stick limbs and tube body | Small rounded body, short soft limbs, mitten hands |
| Role shown by accessories on the same body | Signature orange colour carried through every outfit |

Also avoid any resemblance to existing game or cartoon characters. For example: no caps with letters, no mustaches, and no copied creature designs.

---

## CHAR-KID
- **Role:** the viewer's stand-in. Opens the curtains (S01), visits three places (S04), and returns to the window for the callback (S10). Unnamed in the narration ("a kid").
- **Age and identity:** about 8–10 years old, neutral presentation, no gendered markers.
- **Proportions (chibi):** about 2.3 heads tall. The head is about 43% of total height. The body is a soft rounded rectangle, slightly wider at the hips. Legs are short with rounded sneakers. Hands are mittens, with no fingers drawn except a thumb nub.
- **Face:**
  - **Eyes:** two tall ovals set wide, each with one white highlight.
  - **Brows:** small arched brows that do the acting.
  - **Nose:** a tiny curved nose.
  - **Mouth:** a simple line mouth with swappable shapes.
  - **Cheeks:** a light blush dot on each cheek.
- **Hair:** short, messy, dark brown, with one tuft sticking up at the crown. That tuft is the silhouette signature: it must read in profile and from behind.
- **Base outfit (S01, S10):** orange hoodie with the hood down behind the neck, cream drawstrings and a kangaroo pocket. Navy trousers, and white sneakers with orange soles.
- **Location outfits for S04** (same kid, the default in the approved storyboard; orange stays the signature):
  - **Equator beach:** orange T-shirt, navy shorts, and a sun hat with an orange band. Barefoot or sandals.
  - **Mid-latitude city:** the base orange hoodie.
  - **Far-north town:** orange puffer coat, a knit hat with a pom-pom, and navy mittens.
- **Palette** (defaults; the creator can change them):
  - Skin `#C98E63`, shade `#AD7450`.
  - Hair `#3B2A24`.
  - Hoodie `#F28C28`, shade `#D46F17`.
  - Drawstrings and highlight `#FFF1D6`.
  - Trousers `#2E3A5C`.
  - Shoes `#FAFAF5` with soles `#F28C28`.
  - Blush `#E58B7B`.
  - Hat band `#F28C28`.
  - Puffer `#F28C28` with quilt lines in `#D46F17`.
- **Face library (instant swaps):**
  - **Neutral:** relaxed brows, small line mouth.
  - **Wonder:** brows up, eyes slightly bigger, small "o" mouth. Used whenever the kid looks up.
  - **Delight:** brows up, wide smile.
  - **Puzzled:** one brow up, mouth pulled to the side.
  - **Meh:** brows raised and flat, flat mouth. Used with the shrug.
- **Poses** (from storyboard v2):

  | Pose ID | Used in | Description |
  |---|---|---|
  | POSE-KID-CURTAINS | S01 V2 | Front three-quarter; both arms up and out, gripping curtains; face: delight to wonder |
  | POSE-KID-LOOK-UP | S01 V3, S04 V2 | Head tilted back, body leaning slightly back, arms loose; face: wonder |
  | POSE-KID-ARM-SWEEP | S04 V3 | One arm raised and swept along the arch, other hand on hip; face: delight. **New:** the storyboard text says the kid "sweeps an arm along it" but did not name a pose |
  | POSE-KID-SHRUG | S04 V6 | Shoulders up, both mittens out palm-up; face: meh |
  | POSE-KID-BACK-LOOK-UP | S10 | Seen from behind at the window, head tilted up; hair tuft and hood read in silhouette. **New:** S10 needs a back view |

- **Allowed variations:** face swaps; the three location outfits; scale; flipping left or right. The tuft always flips with the head. Any change to silhouette, proportions or palette needs a new approved version.

## CHAR-TRILOBITE
- **Role:** the ancient witness. Looks up at the ring from the seafloor (S09 V3).
- **Shape:** a cute rounded oval, wider at the head end. Two soft grooves run nose to tail and split the body into **three lengthwise lobes**, the real feature that gives trilobites their name. There are four or five gentle body segments with a small fan tail. Little legs show only at the edges as short nubs.
- **Face:** two big tall-oval eyes on top of the head shield, with highlights. Small brows. A tiny mouth under the head edge.
- **Palette:** shell `#D9A86C`, shade `#B9834A`, groove lines `#8F6236`, belly and highlight `#F6E2BE`. Underwater, the scene's teal grade (LS7) tints it.
- **Face library:** neutral, wonder.
- **Poses:**

  | Pose ID | Used in | Description |
  |---|---|---|
  | POSE-TRILOBITE-LOOK-UP | S09 V3 | Front three-quarter, head end tilted up off the sand, eyes up; face: wonder |

- **Allowed variations:** face swap, scale, flip. Not a specific scientific species; a cartoon trilobite.

## CHAR-DINO
- **Role:** the punchline for "long before the dinosaurs". Walks in under an empty dawn sky and looks up (S09 V4).
- **Shape:** a small, round, two-legged cartoon dinosaur, not a specific species. Big round head (about 40% of its height), a chubby pear-shaped body, tiny arms, short thick legs and a short tapering tail. A row of three soft rounded back plates gives it a silhouette signature.
- **Face:** tall-oval eyes with highlights, small brows, a wide friendly mouth line, two nostril dots.
- **Palette:** body `#6BBF7A`, shade `#4E9E5F`, belly `#E9F2C8`, back plates `#F2B84B`, cheeks `#E58B7B`.
- **Face library:** neutral, puzzled. It looks up at an empty sky, a "huh?" beat.
- **Poses:**

  | Pose ID | Used in | Description |
  |---|---|---|
  | POSE-DINO-STEP-A / POSE-DINO-STEP-B | S09 V4 | Side three-quarter walk: two alternating steps swapped on twos. **New:** the storyboard says it "walks in" |
  | POSE-DINO-LOOK-UP | S09 V4 | Stops, head tilted up, tiny arms raised slightly; face: puzzled |

- **Allowed variations:** face swap, scale, flip.

---

## Rights and provenance
- **Method:** Claude-written layered SVG, the same method used for EP002. No AI image tool, no reference images, and no artists' or channels' names in requests.
- **Recording:** each kept asset gets a row in `02_CONTEXT/assets/provenance-log.md` (model, request, date, file path, approval) and an entry in `asset-manifest.json`.
- **Commercial use:** check Anthropic's current terms for commercial use of outputs before publishing. Copyright protection for AI-assisted art varies by jurisdiction (not legal advice).

## Proposed art batches (each needs its own go-ahead and approval)
1. **Kid master:** front three-quarter and back view, base outfit, with the face library sheet.
2. **Kid poses and outfits:** the five poses, plus the beach and far-north outfits.
3. **Creatures:** trilobite (with face library and pose) and dinosaur (two step poses, look-up, and face library).

## Decisions for the creator
1. **Skin tone:** the default is a medium warm brown `#C98E63`. Change it if you prefer.
2. **Name:** keep the kid unnamed (default), or give it a name for future episodes. A recurring kid would be a channel-level choice.
3. **New poses:** POSE-KID-ARM-SWEEP, POSE-KID-BACK-LOOK-UP and POSE-DINO-STEP-A/B only make explicit what the approved storyboard already shows. Confirm they're fine; they don't change the storyboard.
4. **Art method:** Claude-written SVG (default), or another method.

## Status
Version: v1. **Approved** by Sean Caling on 2026-11-02 ("Approve character specs v1"). The four decisions above were not changed, so the defaults stand: skin tone `#C98E63`, the kid stays unnamed, the added poses are confirmed, and the art method is Claude-written SVG. The characters are recorded in `02_CONTEXT/character-registry.md`. Art waits for a go-ahead on batch 1.
