# Shorts Mentor Harness

A human-led workspace for making animated Shorts for the FooFilms channel: scientific what-ifs first, strange history second. Claude can coach both the creator and the story—concept, hook, emotion, pacing, visual explanation, payoff, and retention—while the creator owns the premise and every approval.

> Use this README as the map. [`00_CORE/agents.md`](00_CORE/agents.md) is the authoritative routing guide.

## Contents

- [Principles](#principles)
- [Folder map](#folder-map)
- [Skills and status](#skills-and-status)
- [Quick start](#quick-start)
- [Approval workflow](#approval-workflow)
- [Episode contract](#episode-contract)
- [Current state and next milestones](#current-state-and-next-milestones)

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
02_CONTEXT/assets/                asset manifest and the 2D art of EP002–EP004
renderer-blender/                 Blender renderer: toon3d.py (look and 3D character),
                                  toon_sets.py (shared sets), per-episode scripts
renders/                          render output (git-ignored)
03_TRACKING/                      learnings, branch and format tests, asset backlog
EPISODES/<episode-id>/            idea through production handoff
tools/                            episode validator and approval-state helper
```

Read [`00_CORE/agents.md`](00_CORE/agents.md) to find the relevant files for each task. Narration craft notes from four Ricks Clips transcripts are in [`02_CONTEXT/source-analysis/narration-style-notes-ricks-clips.md`](02_CONTEXT/source-analysis/narration-style-notes-ricks-clips.md). Art and motion notes from a 3D-cartoon style reference transcript are in [`02_CONTEXT/source-analysis/animation-style-notes-3d-cartoon-reference.md`](02_CONTEXT/source-analysis/animation-style-notes-3d-cartoon-reference.md). Animation-style observations from two Ricks Clips Shorts are in [`02_CONTEXT/source-analysis/animation-style-notes-ricks-clips.md`](02_CONTEXT/source-analysis/animation-style-notes-ricks-clips.md). Narration craft notes from four Zack D. Films transcripts are in [`02_CONTEXT/source-analysis/narration-style-notes.md`](02_CONTEXT/source-analysis/narration-style-notes.md). Reference-channel topic and title patterns (titles only, scripts not analyzed) are in [`02_CONTEXT/source-analysis/channel-reference-notes.md`](02_CONTEXT/source-analysis/channel-reference-notes.md). The transcript-derived mentor notes are in [`02_CONTEXT/source-analysis/mentor-source-notes.md`](02_CONTEXT/source-analysis/mentor-source-notes.md); they summarize selected advice rather than copying whole transcripts.

## Skills and status

All five skills are project-local and set to `disable-model-invocation: true`; call them explicitly in Claude Code.

| Skill | Use | Boundary |
|---|---|---|
| [`/short-mentor`](.claude/skills/short-mentor/SKILL.md) | Coach the creator or critique story choices | Advice only; does not advance approval gates |
| [`/short-ideate`](.claude/skills/short-ideate/SKILL.md) | Topic stage (seed list, five checks, title and first line), then a concept card from the seed the creator selects | Stops for the creator's selection, then for idea approval |
| [`/short-storyboard`](.claude/skills/short-storyboard/SKILL.md) | Research, draft narration, and create shot plan | Separate script and storyboard approvals |
| [`/short-animate`](.claude/skills/short-animate/SKILL.md) | Build and render the episode in Blender, scene by scene, then the preview | Asks before every render; stops for each scene and for preview approval |
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

The ideate skill starts with a topic stage and stops for your selection. The storyboard skill pauses for script approval and again for storyboard approval. The animate skill asks before every render and stops for each scene's approval and for preview approval.

## Approval workflow

```text
creator seed → idea approval → script approval → storyboard approval
             → scene-by-scene approvals → animation-preview approval
             → title and hashtags → human CapCut edit and posting
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

`episode.json` specifies a 1080×1920, 30 fps master (24 fps for episodes made before motion rules v2) with integer frames and half-open shot ranges. It describes timestamped narration, characters and poses, camera motion, captions, transitions, synchronized audio, individual scene MP4s, and a review preview. From motion rules v3, characters and camera update every frame.

Validate the packet with:

```bash
python3 tools/validate_episode.py EPISODES/EP002
```

This checks schema and cross-field timing/export relationships; it does not render or verify media files. ElevenLabs audio timing should use the generated narration. CapCut editing remains human-led; there is no auto-publication.

## Current state and next milestones

- **Posted:** EP002 (Project Pigeon), EP003 (Earth's rings) and EP004 (the ocean disappearing). They are closed and are not restyled. Results are in `03_TRACKING/branch-test-plan.md`.
- **Look from EP005:** visual style v4 and motion rules v3, approved 2026-11-13: 3D characters (bean build, painted swappable faces) in dense, dressed sets with mood lighting.
- **Test before finalizing:** changes to format, look and workflow are tests until their results are in. The register is `03_TRACKING/format-tests.md`.
- **Efficiency:** `01_SPECS/render-pipeline-notes.md` records how rendering works and what went wrong on EP004; `01_SPECS/efficiency-plan.md` is the plan to make production faster.
- **Limits:** the mentor notes come from three creator-supplied transcripts; view, revenue and algorithm claims in them are not verified. The example episode in `EPISODES/EP001-example/` is a placeholder to copy, not a story.
