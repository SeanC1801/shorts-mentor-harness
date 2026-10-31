# Routing and operating protocol
Read only the smallest relevant context set.

| Need | Read |
|---|---|
| Creator preferences | `me.md` |
| Gates and versioning | `00_CORE/mentor-protocol.md`, `01_SPECS/document-contracts.md` |
| Production constraints | `01_SPECS/production-standards.md`, `quality-checklist.md` |
| Storytelling / look | `02_CONTEXT/channel-identity.md`, `storytelling-guide.md`, `visual-style.md`, `motion-rules.md` |
| Episode work | episode packet, `episode.json`, `status.json`, `handoff.md` |
| Prior learnings | load only relevant entries from `03_TRACKING/` |
| Skill details | the invoked skill's `SKILL.md` and named references only |

## Route
- `/short-ideate`: creator-seeded concept; stop for idea approval.
- `/short-storyboard`: source check, script and storyboard; separate script and storyboard approvals.
- `/short-animate`: after storyboard approval, make an animation plan/preview only as available; stop for preview approval.
- `/short-review`: critique and checklist; never approves, exports, or publishes on the user's behalf.
- `/short-mentor`: advice-only coaching for the creator or story; never advances approval gates.

Before resuming or advancing, run `python3 tools/approval_state.py sync EPISODES/<ID>`; run `python3 tools/validate_episode.py EPISODES/<ID>` before storyboard approval or render planning. Only record a gate with `approval_state.py record` after the creator explicitly approves the exact version shown. At session end update `handoff.md` with current stage, approved artifact IDs/versions, blockers, next user decision, and exact files. Keep logs append-only. Never copy whole transcript collections into core context.
