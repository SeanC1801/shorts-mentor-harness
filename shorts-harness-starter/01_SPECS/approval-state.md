# Approval state helper

The helper records explicit user decisions and detects stale approvals by hashing artifact bytes. It does not make creative decisions or treat a command suggestion as consent.

## Check state before resuming
`python3 tools/approval_state.py sync EPISODES/EP001`

## Record only after the creator says yes to the shown artifact version
`python3 tools/approval_state.py record EPISODES/EP001 --gate idea --artifact-version v1 --approved-by "Creator" --confirm "I approve idea v1"`

Use `--gate script`, `storyboard`, or `animationPreview` at the corresponding gate. The command requires exact confirmation text, records artifact SHA-256 and prerequisite hashes, approver and timestamp, and refuses missing artifacts or unapproved prerequisites. Script hashes `research.md` and `script.md`; storyboard hashes `storyboard.md` and `episode.json`; preview hashes `animation-preview.mp4`. The preview artifact is unavailable until a future renderer creates it.

Run `sync` after edits and before resuming. If approved bytes change, the gate is marked `invalidated`; dependent approvals are invalidated on sync too. Reapproval must use the current artifact version. This is a local workflow guardrail, not tamper-proof access control.
