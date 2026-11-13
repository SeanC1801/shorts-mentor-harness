---
name: short-animate
description: Build and render an approved storyboard in Blender scene by scene, then the full preview; stop for each scene's approval and for preview approval.
disable-model-invocation: true
---
# Short Animate
First run `python3 tools/approval_state.py sync EPISODES/<ID>`. Read the approved storyboard and all gates, `01_SPECS/document-contracts.md`, `02_CONTEXT/visual-style.md` (v4), `motion-rules.md` (v3), `character-registry.md`, `01_SPECS/render-pipeline-notes.md`, `03_TRACKING/format-tests.md` and the handoff. Stop if storyboard approval is absent or invalidated.

1. **Plan.** List the sets, characters, faces and poses the episode needs, and which already exist (`renderer-blender/toon_sets.py`, `toon3d.py`). New characters, new sets and new looks need the creator's approval, with stills, before they are used.
2. **Scene by scene.** For each scene: prepare the code, check framing and timing with a no-render dry run, then **ask the creator before any render** (check stills or the full scene) and say what will render and roughly how long it takes. An episode is one file in `renderer-blender/episodes/` (pattern: `motion_test.py`) whose timings come from `episode.json` views; render with `python3 -I renderer-blender/scripts/render_scene.py <episode> <shot>` and dry-run with `render_episode.py ... --dry`, never a hand-typed shell loop. Check the result (no missing frames, no errors, clip length), present the clip, and wait for "Approve S0N" before starting the next scene. Record each approval in the handoff.
3. **Preview.** After every scene is approved, assemble the full preview into its own folder, copy it to `EPISODES/<ID>/animation-preview.mp4`, run `approval_state.py sync`, and present it. Record the gate only after the creator types the exact approval phrase, with `approval_state.py record --gate animationPreview`.
4. **Title and hashtags.** With every approved preview, offer three to five title options and one hashtag set; record the creator's choice in the handoff.

Posted episodes are closed: never restyle them. Any storyboard change invalidates preview approval. The creator runs git and posts the video; never publish.
