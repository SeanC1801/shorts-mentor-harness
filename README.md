# Shorts Mentor Harness

A human-led workspace for making illustrated Shorts about weird technology, strange history, and scientific what-ifs. Claude can coach both the creator and the story—concept, hook, emotion, pacing, visual explanation, payoff, and retention—while the creator owns the premise and every approval.

> Use this README as the map. [`00_CORE/agents.md`](00_CORE/agents.md) is the authoritative routing guide.

## Contents

- [Principles](#principles)
- [Folder map](#folder-map)
- [Skills and status](#skills-and-status)
- [Quick start](#quick-start)
- [Approval workflow](#approval-workflow)
- [Episode contract](#episode-contract)
- [Current limits and next milestones](#current-limits-and-next-milestones)

## Principles

The creator supplies or chooses the original idea. The mentor suggests and critiques; it does not imitate a transcript creator, claim the creator's idea, infer approval, promise virality or revenue, or publish automatically. Approvals belong to specific versions. When an approved artifact changes, downstream approvals must be checked again.

## Folder map

```text
CLAUDE.md                         project rules
me.md                             creator preferences
.claude/skills/                   five manually invoked skills
00_CORE/                          routing and approval protocol
01_SPECS/                         production standards, contracts, checklists
02_CONTEXT/                       channel, storytelling, visual style, templates
02_CONTEXT/source-analysis/       attributed, selective transcript notes
02_CONTEXT/assets/                asset manifest and library plan (character,
                                  background, and prop art is not yet created)
03_TRACKING/                      learnings, bottlenecks, asset backlog
04_LOGS/                          concise session history
EPISODES/<episode-id>/            idea through production handoff
tools/                            episode validator and approval-state helper
```

Read [`00_CORE/agents.md`](00_CORE/agents.md) to find the relevant files for each task. Narration craft notes from four Ricks Clips transcripts are in [`02_CONTEXT/source-analysis/narration-style-notes-ricks-clips.md`](02_CONTEXT/source-analysis/narration-style-notes-ricks-clips.md). Animation-style observations from two Ricks Clips Shorts are in [`02_CONTEXT/source-analysis/animation-style-notes-ricks-clips.md`](02_CONTEXT/source-analysis/animation-style-notes-ricks-clips.md). Narration craft notes from four Zack D. Films transcripts are in [`02_CONTEXT/source-analysis/narration-style-notes.md`](02_CONTEXT/source-analysis/narration-style-notes.md). Reference-channel topic and title patterns (titles only, scripts not analyzed) are in [`02_CONTEXT/source-analysis/channel-reference-notes.md`](02_CONTEXT/source-analysis/channel-reference-notes.md). The transcript-derived mentor notes are in [`02_CONTEXT/source-analysis/mentor-source-notes.md`](02_CONTEXT/source-analysis/mentor-source-notes.md); they summarize selected advice rather than copying whole transcripts.

## Skills and status

All five skills are project-local and set to `disable-model-invocation: true`; call them explicitly in Claude Code.

| Skill | Use | Boundary |
|---|---|---|
| [`/short-mentor`](.claude/skills/short-mentor/SKILL.md) | Coach the creator or critique story choices | Advice only; does not advance approval gates |
| [`/short-ideate`](.claude/skills/short-ideate/SKILL.md) | Develop a concept from the creator's original seed | Stops for idea approval |
| [`/short-storyboard`](.claude/skills/short-storyboard/SKILL.md) | Research, draft narration, and create shot plan | Separate script and storyboard approvals |
| [`/short-animate`](.claude/skills/short-animate/SKILL.md) | Prepare an animation plan | No renderer or preview exists in Phase 1 |
| [`/short-review`](.claude/skills/short-review/SKILL.md) | Critique evidence, storytelling, and handoff | Does not approve or publish |

## Quick start

1. Open the repository root (the folder containing this README and `CLAUDE.md`) as the Claude Code workspace.
2. Read [`me.md`](me.md) and [`00_CORE/agents.md`](00_CORE/agents.md).
3. Copy [`EPISODES/EP001-example/`](EPISODES/EP001-example/) to a new episode ID and replace its placeholders.
4. For a focused coaching conversation, invoke `/short-mentor` with a question or episode ID. To begin a new story, provide your own seed:

   ```text
   /short-ideate EP002 "[your original idea seed]"
   ```

5. Continue one approval gate at a time:

   ```text
   /short-storyboard EP002
   /short-animate EP002
   /short-review EP002
   ```

The storyboard skill pauses for script approval and again for storyboard approval. In this phase, animate prepares a plan only; it cannot render a preview.

## Approval workflow

```text
creator seed → idea approval → script approval → storyboard approval
             → future animation-preview approval → human CapCut edit
```

Before resuming, check whether approved files have changed:

```bash
python3 tools/approval_state.py sync EPISODES/EP002
```

Record approval only after the creator explicitly approves the displayed artifact version. For example:

```bash
python3 tools/approval_state.py record EPISODES/EP002 \
  --gate idea --artifact-version v1 --approved-by "Creator" \
  --confirm "I approve idea v1"
```

The helper records artifact hashes, dependencies, version, approver, and timestamp. See [`01_SPECS/approval-state.md`](01_SPECS/approval-state.md).

## Episode contract

`episode.json` specifies a 1080×1920, 24 fps master with integer frames and half-open shot ranges. It describes timestamped narration, characters and poses, camera motion, captions, transitions, synchronized audio, individual scene MP4s, and a review preview. Character poses use two-frame exposures (about 12 effective fps); camera motion may update at 24 fps.

Validate the packet with:

```bash
python3 tools/validate_episode.py EPISODES/EP002
```

This checks schema and cross-field timing/export relationships; it does not render or verify media files. ElevenLabs audio timing should use the generated narration. CapCut editing remains human-led; there is no auto-publication.

## Current limits and next milestones

- The sample episode is a placeholder, not an approved or researched story.
- Three user-provided transcripts were selected for mentor notes: idea development, hook/visual focus, and retention critique. Other supplied files were not bulk-ingested. View, revenue, algorithm, upload-frequency, and policy claims are not verified by those notes.
- Next: review further selected sources if useful; develop original character art with creator approval; build a minimal Remotion renderer; make an approved pilot with separate scene clips and preview.
