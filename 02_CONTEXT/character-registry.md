# Character registry
Add a character only after creator approval. Record stable ID, role, visual description, expression/pose inventory, source files, rights/provenance, allowed variations, and approval version. Keep original layered source files; list exports in `assets/asset-manifest.json`.

## Approved characters

### CHAR-KID3D (3D bean build, approved 2026-11-13)
- **Approval:** look test v1 ("I approve this look"), bean build ("Bean build (v2)") and motion test ("I approve it"), all by Sean Caling on 2026-11-13. Used from EP005; under test per `03_TRACKING/format-tests.md` row 10.
- **Role:** the channel's own kid rebuilt in 3D, the viewer's stand-in. One build serves as hero and as supporting characters through colour variants.
- **Visual description:** large egg head; tall oval eyes with a highlight and eye whites, short brows, small mouth, blush; brown hair with one tuft, or a cap; one long bean body with three white buttons; thin navy limbs, small ball hands, small shoes. Hero colours: off-white head `#F4EFE6`, yellow body `#F2B10C`, red shoes `#C9482F`, brown hair `#4A2C1A`.
- **Faces (10):** neutral, happy, laugh, surprised, worried, nervous, deadpan, smug, squint, blink.
- **Poses:** stand, wave, point_up, shock, shrug, think, walk, shield (`toon3d.POSES`); new poses are added as the same kind of entry.
- **Allowed variations:** skin tone, hair colour or cap, body colour, shoe colour, scale, turn. A change to proportions or the face design needs a new approved version.
- **Source:** built in code by `renderer-blender/toon3d.py` (`kid(..., build="bean")`); faces painted by `renderer-blender/scripts/paint_faces3d.py` into `renderer-blender/textures/faces3d/`. Original design; the reference channels supplied the construction method only.

EP002's pigeon and psychologist stand-in were episode-only characters; their record stays in `EPISODES/EP002/`.

Shared rules for the EP003 characters (look, outline, paper feel, contact shadow, acting, readability, how they differ from reference-channel characters) are in the full spec: `EPISODES/EP003/character-specs.md` v1.

### CHAR-KID (approved spec v1)
- **Approval:** spec v1 approved by Sean Caling on 2026-11-02 (explicit: "Approve character specs v1").
- **Role:** the viewer's stand-in in EP003 (unnamed, "a kid"). Not a channel mascot unless the creator decides later.
- **Visual description:** paper-cut chibi about 2.3 heads tall; skin-toned round head (`#C98E63`), tall oval eyes with highlights and small brows, tiny nose, blush dots; short messy dark hair with one crown tuft; orange hoodie (`#F28C28`), navy trousers, white sneakers with orange soles; mitten hands; soft navy-brown outline; painted-in shading.
- **Expressions:** neutral, wonder, delight, puzzled, meh.
- **Poses:** POSE-KID-CURTAINS, -LOOK-UP, -ARM-SWEEP, -SHRUG, -BACK-LOOK-UP.
- **Allowed variations:** face swaps; three location outfits (beach T-shirt and sun hat, base hoodie, far-north puffer and pom-pom hat), all with orange as the signature; scale; flip. Any change to silhouette, proportions or palette needs a new approved version.
- **Source files:** `02_CONTEXT/assets/characters/ASSET-CHAR-KID-MASTER-v001.svg` (front and back, base outfit) and `ASSET-CHAR-KID-FACES-v001.svg` (five face swaps); art batch 1 approved by Sean Caling on 2026-11-02 ("Approve batch 1"). Poses `ASSET-CHAR-KID-POSES-v001.svg` and outfits `ASSET-CHAR-KID-OUTFITS-v001.svg`: art batch 2 approved by Sean Caling on 2026-11-02 ("Approve batch 2"). Approved as drawn: ARM-SWEEP has the left arm out to the side (not on the hip), and the far-north knit hat hides the tuft.
- **Rights/provenance:** Claude-written layered SVG planned; record each kept asset in `assets/provenance-log.md`.

### CHAR-TRILOBITE (approved spec v1)
- **Approval:** spec v1 approved by Sean Caling on 2026-11-02 (explicit: "Approve character specs v1").
- **Role:** EP003 ancient witness on the seafloor (S09).
- **Visual description:** cute rounded oval, three lengthwise lobes, four or five soft segments, small fan tail, leg nubs; big tall-oval eyes on the head shield; sandy palette (`#D9A86C`, shade `#B9834A`); soft navy-brown outline.
- **Expressions:** neutral, wonder. **Poses:** POSE-TRILOBITE-LOOK-UP.
- **Allowed variations:** face swap, scale, flip. A cartoon trilobite, not a specific species.
- **Source files:** `02_CONTEXT/assets/characters/ASSET-CHAR-TRILOBITE-v001.svg`; art batch 3 approved by Sean Caling on 2026-11-02 ("Approve batch 3"). **Rights/provenance:** Claude-written layered SVG; see `assets/provenance-log.md`.

### CHAR-DINO (approved spec v1)
- **Approval:** spec v1 approved by Sean Caling on 2026-11-02 (explicit: "Approve character specs v1").
- **Role:** EP003 punchline for "long before the dinosaurs" (S09).
- **Visual description:** small round two-legged cartoon dinosaur, not a specific species; big round head, pear-shaped body, tiny arms, short tail; three soft yellow back plates (`#F2B84B`); green body (`#6BBF7A`), pale belly; soft navy-brown outline.
- **Expressions:** neutral, puzzled. **Poses:** POSE-DINO-STEP-A, POSE-DINO-STEP-B, POSE-DINO-LOOK-UP.
- **Allowed variations:** face swap, scale, flip.
- **Source files:** `02_CONTEXT/assets/characters/ASSET-CHAR-DINO-v001.svg`; art batch 3 approved by Sean Caling on 2026-11-02 ("Approve batch 3"). **Rights/provenance:** Claude-written layered SVG; see `assets/provenance-log.md`.

### CHAR-RAINKID (approved spec v2)
- **Role:** EP004 viewer stand-in ("a kid"); watches rain, reacts to the ocean draining, the glare and the cold night, returns to the window. EP004 only unless the creator decides it becomes recurring.
- **Visual description:** about 3 heads tall; plain white `#FFFFFF` egg-shaped head (wider at the bottom), about 45% of height, no nose, ears or neck; small dark-brown hair tuft `#4A3428`; vertical oval eyes with one highlight; thick short eyebrows that carry expression; mouth line, coral tongue `#FF7A6B` at peaks; small trapezoid body; thick navy `#232238` stick limbs with mitten nubs and rounded shoes; navy outline about 1% of frame height; flat fills with one cel shade band.
- **Outfits (by environment, no signature costume):** indoors sky-blue T-shirt and grey trousers; shore raincoat and boots; harsh sun pale-yellow T-shirt, orange shorts, red cap, sandals; cold night navy puffy jacket, red beanie and scarf.
- **Expressions:** curious, deadpan half-lidded, shocked, worried, squinting, shivering, wistful. **Poses:** window, point up, shock, shield eyes, shiver, shore look-out, fan self.
- **Allowed variations:** face swap, outfit swap, scale, flip.
- **Spec:** `EPISODES/EP004/character-specs.md` v2, approved by Sean Caling on 2026-11-10 ("Approve specs v2"). **Source files:** `02_CONTEXT/assets/characters/ASSET-CHAR-RAINKID-MASTER-v001.svg` (front, indoor outfit) and `ASSET-CHAR-RAINKID-FACES-v001.svg` (seven face swaps); art batch 1 approved by Sean Caling on 2026-11-11 ("Approve batch 1"). Poses `ASSET-CHAR-RAINKID-POSES-v001.svg` and outfits `ASSET-CHAR-RAINKID-OUTFITS-v001.svg`: art batch 2 approved by Sean Caling on 2026-11-11 ("Approve batch 2"). Character art is complete. **Rights/provenance:** Claude-written layered SVG planned; craft inspiration only (`source-analysis/character-style-notes-stick-cartoon-references.md`).
