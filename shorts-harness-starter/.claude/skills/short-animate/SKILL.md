---
name: short-animate
description: Prepare animation implementation and review preview for an approved storyboard; the Phase 1 starter has no renderer.
disable-model-invocation: true
---
# Short Animate
First run `python3 tools/approval_state.py sync EPISODES/<ID>`. Read approved storyboard and all gates, contract, motion rules, visual style, asset manifest, and handoff. Stop if storyboard approval is absent/invalidated. In Phase 1, produce an animation plan and missing-asset list only; do not claim to render. A plan is not an animation preview and cannot pass the preview approval gate. In a future approved Remotion phase, author React/TypeScript scenes, 24fps camera/parallax, character poses exposed on two-frame steps, synchronized audio, individual scene MP4s and preview. In a future renderer phase, show the actual preview file identity/version and ask for explicit approval; after the creator approves, record with `approval_state.py record --gate animationPreview`. Any storyboard change invalidates preview approval. Never publish.
