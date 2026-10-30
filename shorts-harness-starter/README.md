# Shorts Mentor Harness

A human-led workspace for developing and producing illustrated vertical Shorts about weird technology, strange history, and scientific what-ifs. Claude helps the creator shape the story—from concept and hook through emotion, pacing, visual payoff, and retention critique—while the creator owns the idea and every approval.

> This README is the orientation map. For authoritative routing and workflow rules, start with [`00_CORE/agents.md`](00_CORE/agents.md).

## Contents

- [Philosophy](#philosophy)
- [Folder map](#folder-map)
- [Skills and current status](#skills-and-current-status)
- [Quick start](#quick-start)
- [Workflow and approval gates](#workflow-and-approval-gates)
- [Episode contract and checks](#episode-contract-and-checks)
- [Current limits and next steps](#current-limits-and-next-steps)

## Philosophy

The creator supplies the original premise and makes every final creative decision. Claude can ask questions, research, recommend, draft, and critique; it does not invent a publishable premise, imitate a transcript creator's personality, infer approval, or publish automatically.

Approvals apply to a specific artifact version. If an approved upstream file changes, dependent approvals must be renewed. Episode files and handoffs keep decisions available to a fresh session without rereading a long conversation.

## Folder map

```text
CLAUDE.md                         project-wide operating rules
me.md                             creator preferences
.claude/skills/                   four manually invoked Claude Code skills
00_CORE/                          routing and mentor approval protocol
01_SPECS/                         production rules, contracts, rubric, approval guide
02_CONTEXT/                       channel identity, storytelling, visual direction,
                                  templates, transcript analysis, asset library plan
03_TRACKING/                      learnings, bottlenecks, asset backlog
04_LOGS/                          concise append-only session history
EPISODES/<episode-id>/            idea, research, script, storyboard, state, handoff
02_CONTEXT/assets/                asset manifest and library plan
tools/                            episode validator and approval-state helper
```

`00_CORE/agents.md` is the routing table. Read it to find the smallest relevant set of files for a task. The asset manifest currently lives at [`02_CONTEXT/assets/asset-manifest.json`](02_CONTEXT/assets/asset-manifest.json); no finished character artwork is included.

## Skills and current status

All four skills are project-local and set to `disable-model-invocation: true`; invoke them explicitly in Claude Code.

| Skill | Purpose | Current boundary |
|---|---|---|
| [`/short-ideate`](.claude/skills/short-ideate/SKILL.md) | Shape a creator-supplied seed into a concept card | Stops for explicit idea approval |
| [`/short-storyboard`](.claude/skills/short-storyboard/SKILL.md) | Research claims, draft narration, then build the shot plan | Stops separately for script approval and storyboard approval |
| [`/short-animate`](.claude/skills/short-animate/SKILL.md) | Prepare the animation plan and identify missing assets | Phase 1 has no renderer; a plan is not an animation preview |
| [`/short-review`](.claude/skills/short-review/SKILL.md) | Critique story, evidence, retention, and handoff quality | Reviews do not approve or publish |

The starter includes an episode schema and sample, an approval-state helper, a packet validator, and production templates. The Remotion engine, original character designs, generated narration, rendered clips, and pilot are future work.

## Quick start

1. Open the **project root containing this README and `CLAUDE.md`** as the Claude Code workspace. If placing this project at a repository root, put these files directly at that root rather than nesting the project folder inside another copy of itself.
2. Read [`CLAUDE.md`](CLAUDE.md), [`me.md`](me.md), and [`00_CORE/agents.md`](00_CORE/agents.md).
3. Copy [`EPISODES/EP001-example/`](EPISODES/EP001-example/) to a new ID such as `EP002`; replace the placeholder content and keep the files together.
4. Start with your own original idea seed:

   ```text
   /short-ideate EP002 "[your original idea seed]"
   ```

5. Continue one gate at a time, only after approval:

   ```text
   /short-storyboard EP002
   /short-animate EP002
   /short-review EP002
   ```

`short-storyboard` handles the script gate first, then the storyboard gate. `short-animate` can only prepare a plan in this phase; it cannot render a preview.

## Workflow and approval gates

```text
creator's idea → concept approval → script approval → storyboard approval
                → future animation preview approval → human CapCut edit
```

Before resuming an episode, check for edits to previously approved files:

```bash
python3 tools/approval_state.py sync EPISODES/EP002
```

After the creator explicitly approves the exact version shown, record that decision. Example for the idea gate:

```bash
python3 tools/approval_state.py record EPISODES/EP002 \
  --gate idea \
  --artifact-version v1 \
  --approved-by "Creator" \
  --confirm "I approve idea v1"
```

Use the corresponding gate name `script`, `storyboard`, or `animationPreview` at later stages. The helper records the artifact SHA-256, prerequisite hashes, version, approver, and timestamp. Run `sync` after edits; it marks approvals invalid when the hashed files or upstream approvals change. It is a workflow guardrail, not tamper-proof access control. See [`01_SPECS/approval-state.md`](01_SPECS/approval-state.md) for details.

## Episode contract and checks

`episode.json` describes 1080×1920 output at 24 fps with integer frame counts and half-open shot ranges `[startFrame, endFrame)`. It includes timestamped narration, character poses, camera motion, captions, transitions, synchronized audio, and one MP4 export per scene plus a review preview. Character pose changes use two-frame exposures (about 12 effective fps); camera motion may update at 24 fps.

Run the validator before treating a shot packet as complete:

```bash
python3 tools/validate_episode.py EPISODES/EP002
```

The validator checks the JSON schema and cross-field timing/export relationships. It does **not** render video or verify the contents of referenced media. ElevenLabs audio timing should come from the generated narration file. Final editing remains in CapCut; there is no automatic publication.

## Current limits and next steps

- The example episode is structural placeholder content, not a researched or approved story.
- Transcript lessons have not been ingested here. When files are available, triage by title, read only selected high-value transcripts, and save attributed summaries. Treat algorithm, earnings, and performance claims as unverified unless independently corroborated.
- Next milestones: selectively review transcript sources; develop original character art with creator approval; build and validate a minimal Remotion renderer; then produce an approved pilot with separate scene clips and a preview.
- A daily publishing cadence is an aspiration, not a production promise.
