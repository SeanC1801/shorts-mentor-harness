# EP004 character specs v2 (APPROVED by Sean Caling, 2026-11-10: "Approve specs v2")

Covers one new character, **CHAR-RAINKID**, which replaces EP003's paper-cut chibi kid for EP004 at the creator's request ("Change the character design", 2026-11-10). No art exists yet. Nothing goes into `02_CONTEXT/character-registry.md` until the creator approves this spec, and no art is made without a separate go-ahead for each batch. EP003 and its kid are posted and stay unchanged.

**Style sources:**
- **Characters:** the craft principles in `02_CONTEXT/source-analysis/character-style-notes-stick-cartoon-references.md`, drawn from the creator's screenshots (Set A, and Set B from TheOdd1sOut). We use principles only: a big acting head, a minimal body, thick outlines and flat fills. (Identity through one costume piece is **not** used: creator, 2026-11-10.)
- **Sets:** the EP003 cel look (Blender EEVEE, cel bands and Freestyle ink lines).

## CHAR-RAINKID
- **Role:** the viewer's stand-in. Watches rain on the window (sentence 1), reacts as the ocean drains and the clouds thin, squints in the glare, shivers at night, and returns to the window for the callback. Unnamed in the narration ("a kid").
- **Age and identity:** about 8–10 years old, neutral presentation, no gendered markers.
- **No signature costume (creator, 2026-11-10).** The kid wears clothes that fit each environment. Identity comes from the head, face, hair and line, which never change.
- **Hair:** a small, short dark-brown tuft on top of the head (`#4A3428`), neutral and not gendered. It keeps the head recognisable when the outfit changes.

### Shape and proportions
- **Total height:** about 3 heads.
- **Head:** about **45% of the height**. It's an **egg shape, wider at the bottom** (not a circle), filled **plain white** `#FFFFFF` (creator, 2026-11-10). There is no nose, no ears and no neck. The hair tuft sits on top.
- **Body:** a small rounded trapezoid, about 25% of the height. The outfit is drawn on this one shape.
- **Arms and legs:** **thick single strokes**, the same colour and weight as the outline. The arms end in round mitten nubs, and the legs end in **rounded shoes**, which change with the outfit. The legs are about 30% of the height.

### Face (the acting surface)
- **Eyes:** medium **vertical ovals, each with one white highlight**, set wide and slightly low on the face. They're bigger than Set A's dots and smaller than Set B's giant eyes.
- **Eyebrows:** short, thick, rounded bars. They carry most of the emotion and can lift and tilt independently.
- **Mouth:** a short line by default. At peaks it opens to a dark shape with a **coral tongue** `#FF7A6B`.
- **Cheeks:** two small soft blush ovals `#FFB8A8` that show only in warm emotions.

### Colour and line
| Part | Colour |
|---|---|
| Outline and limbs | dark navy `#232238` (never pure black) |
| Head | plain white `#FFFFFF`, cel shade band light cool grey `#E4E6EE` |
| Hair tuft | dark brown `#4A3428` |
| Outfits | see the outfit table below; each colour gets one cel shade band about 15% darker |

- **Outline weight:** about 1% of the frame height when the character is at its usual size. That's thicker than EP003's kid, so it reads like the references at phone size. The line wobbles slightly, as if hand-drawn.
- **Shading:** flat fills plus **one cel shade band** per shape on the side away from the key light, matching the cel look. Only a small highlight on the hair.

### Outfits by environment (EP004)
| Where (script sentences) | Outfit | Colours |
|---|---|---|
| Indoors at the rainy window (1, 4, 14) | T-shirt, trousers, socks | sky-blue shirt `#6FB7E8`, grey trousers `#7A7F8C` |
| Outside on the shore and drained seabed (5–9) | Raincoat with hood down, rubber boots (it's still drizzling) | yellow coat `#FFC83D`, blue boots `#3A6FD8` |
| Harsh sun on bare ground (12–13, day) | T-shirt, shorts, cap, sandals | pale yellow shirt `#FFE27A` (not white, so it stays separate from the head), orange shorts `#F08A3C`, red cap `#D9483B` |
| Cold clear night (13, night) | Puffy jacket, beanie, scarf | navy jacket `#3B4A7A`, red beanie and scarf `#D9483B` |

Outfits are drawn as swappable layers over the same body, so proportions never change. The storyboard decides exactly where each outfit appears.

### Expressions (face sheet)
1. **Curious:** eyebrows raised, small mouth (watching the rain).
2. **Deadpan, half-lidded:** the dry-humour default, used for "A clearer sky sounds calmer."
3. **Shocked:** eyes widen, eyebrows fly up, mouth open with the tongue (the ocean drains).
4. **Worried:** eyebrows tilted up in the middle (the clouds thin).
5. **Squinting in the glare:** eyes squeezed into arcs, mouth gritted (harsh sun).
6. **Shivering:** a wavy mouth, eyebrows pinched (the cold night).
7. **Wistful:** soft half-lids and a small smile (callback at the window).

### Poses
1. At the window, mittens on the sill, looking out.
2. Pointing up at the sky.
3. Arms flung out in shock.
4. Shielding the eyes with one arm.
5. Hugging itself and shivering.
6. Standing at the shore, looking out at the empty seabed.
7. Fanning itself in the heat.

## How it differs from the references (required: original design)
| Reference signature (do not copy) | CHAR-RAINKID |
|---|---|
| Set A: plain white **circle** head, dot eyes, smug default | White **egg** head (wider at the bottom) with a hair tuft, oval eyes with highlights, curious default |
| Set A: capsule torso with long stick legs | Small trapezoid body, short legs, rounded shoes |
| Set A: brown-black outline | Navy outline |
| Set A: role shown by a costume (office, pirate, police) | No role costume; clothes fit the environment |
| Set B: merged **white bean** body and giant eyes | Separate head and body, medium eyes. Both references use white heads too, so the egg shape, hair tuft, eyes and navy line must carry the difference |

No resemblance to existing cartoon characters in any outfit (for example no famous raincoat bear or duck). Check the first drafts for this.

## Build
- A layered vector source with named parts (head, hair tuft, eyebrows L and R, eyes L and R, mouth set, blush, body, arms L and R, legs L and R, outfit layers per environment, shoes). Poses come from moving and swapping parts on one rig, so proportions stay identical.
- In Blender it stands as a flat cutout card in the cel sets, as EP003's kid did. Poses hold for 2 frames (motion rules v2).
- Readability test: the character must still read at about 150 px tall in a 1080×1920 frame.

## Decisions for the creator
1. **Hair tuft.** A small dark tuft (default), or a bald head like both references.
2. **One-episode or recurring character?** Clothes already change with the environment, so the character could become FooFilms' recurring guide with the head, face and line fixed. Default: EP004 only, decided later.
3. **Outfits.** The four outfits above, or changes.

## Status
Version: v2. Approved by Sean Caling, 2026-11-10 ("Approve specs v2"); creator defaults kept: hair tuft, EP004 only (recurring decided later), four outfits. Next: the creator approves or revises this spec. Then **art batch 1** (master front view plus the face sheet) only with a separate go-ahead.

## Changes from v1
- Removed the signature costume (yellow rain gear) at the creator's direction; clothes now fit each environment (four outfits).
- Added a neutral hair tuft so the head stays recognisable across outfits.
- Head changed from cream to plain white at the creator's direction.
- Version: v2.
