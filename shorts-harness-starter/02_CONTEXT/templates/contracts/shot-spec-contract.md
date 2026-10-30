# Shot specification contract

`shot-spec.schema.json` defines the JSON shape; `shot-spec.example.json` shows timing and editor handoff fields. A sample episode is illustrative only. Use integer frames/milliseconds, stable IDs, explicit half-open ranges, no implicit defaults, and references to existing assets. Each shot carries timestamped narration segments, character/pose actions, camera motion, captions, transitions, visual description, asset IDs, and synchronized audio. Episode-level exports specify one preview and one MP4 per scene.

JSON Schema checks structure and types. Run `python3 tools/validate_episode.py EPISODES/<ID>` for cross-field checks: contiguous frames, narration/audio bounds, frame-to-audio tolerance, caption/segment containment, and one export per shot. The validator checks the packet only; no renderer is included.
