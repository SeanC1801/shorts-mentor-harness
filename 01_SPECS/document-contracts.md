# Document contracts

## Episode files
`idea.md`, `research.md`, `script.md`, `storyboard.md`, `episode.json`, `status.json`, and `handoff.md` travel together. (`PRODUCTION_PACKET.md` was required until 2026-11-13; only EP002 has one, and new episodes do not need it.) Never rely on chat-only decisions.

## Frame/timing contract
- Master is 30 fps at 1080×1920 (motion rules v2 and later; episodes made before v2 stay valid at 24 fps). Every shot has integer `startFrame` inclusive and `endFrame` exclusive; ranges are positive, begin at frame 0, contiguous, and end at `totalFrames`. Duration is `totalFrames / fps`.
- Narration uses integer milliseconds from the actual ElevenLabs file. Each shot contains `narrationSegments` with text and half-open start/end milliseconds. Shot narration intervals are ordered/contiguous when speech is continuous, within `syncToleranceMs` of the frame boundaries. Audio ranges are bounded by measured narration duration.
- From motion rules v3 (EP005 on), 3D characters and the camera update every frame at the master fps. Under v2 (EP003, EP004) cutout poses were held 2 frames, and 12 poses per second at legacy 24 fps. Captions and character actions have explicit shot-local frame intervals.
- Every shot identifies transition in/out, asset IDs, and synchronized audio cues. Exports list one preview and exactly one 1080×1920 MP4 per shot at the master fps. Asset references must resolve through `assets/asset-manifest.json`.

Run `python3 tools/validate_episode.py <episode-folder>` for schema and cross-field validation. The JSON Schema alone cannot express all relational rules. It is a data contract; the renderer is `renderer-blender/`. Making the renderer read its shot timings from `episode.json` is part of `01_SPECS/efficiency-plan.md`.
