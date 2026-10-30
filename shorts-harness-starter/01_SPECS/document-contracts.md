# Document contracts

## Episode files
`idea.md`, `research.md`, `script.md`, `storyboard.md`, `episode.json`, `status.json`, `PRODUCTION_PACKET.md`, and `handoff.md` travel together. Never rely on chat-only decisions.

## Frame/timing contract
- Master is 24 fps at 1080×1920. Every shot has integer `startFrame` inclusive and `endFrame` exclusive; ranges are positive, begin at frame 0, contiguous, and end at `totalFrames`. Duration is `totalFrames / fps`.
- Narration uses integer milliseconds from the actual ElevenLabs file. Each shot contains `narrationSegments` with text and half-open start/end milliseconds. Shot narration intervals are ordered/contiguous when speech is continuous, within `syncToleranceMs` of the frame boundaries. Audio ranges are bounded by measured narration duration.
- Keep character pose rate 12 fps / exposure 2 frames. Camera may update at 24 fps. Captions and character actions have explicit shot-local frame intervals.
- Every shot identifies transition in/out, asset IDs, and synchronized audio cues. Exports list one preview and exactly one 1080×1920/24fps MP4 per shot. Asset references must resolve through `assets/asset-manifest.json`.

Run `python3 tools/validate_episode.py <episode-folder>` for schema and cross-field validation. The JSON Schema alone cannot express all relational rules. It remains a data contract, not a working renderer.
