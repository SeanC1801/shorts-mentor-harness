---
name: short-animate
description: Prepare animation implementation and review preview for an approved storyboard; the Phase 1 starter has no renderer.
disable-model-invocation: true
---
# Short Animate
First run `python3 tools/approval_state.py sync EPISODES/<ID>`. Read approved storyboard and all gates, contract, motion rules, visual style, asset manifest, and handoff. Stop if storyboard approval is absent/invalidated. In Phase 1, produce an animation plan and missing-asset list only; do not claim to render. A plan is not an animation preview and cannot pass the preview approval gate. In an approved renderer phase, build the episode in Blender per `visual-style.md` and `motion-rules.md` (v2): painted 3D sets, flat cutout characters with contact shadows, a 30fps camera that is always moving, poses held 2 frames, word-by-word captions, synchronized audio, individual scene MP4s and preview. In a future renderer phase, show the actual preview file identity/version and ask for explicit approval; after the creator approves, record with `approval_state.py record --gate animationPreview`. Any storyboard change invalidates preview approval. Never publish.
