---
name: short-review
description: Critique a Shorts episode against the quality rubric, factual support, retention, and handoff completeness.
disable-model-invocation: true
---
# Short Review
Run `python3 tools/approval_state.py sync EPISODES/<ID>` and, when `episode.json` exists, `python3 tools/validate_episode.py EPISODES/<ID>`. Then read current episode packet/state, checklist, feedback rubric, and relevant sources. Confirm versions and flag invalidated or missing approvals. Review hook honesty, clarity, emotional movement, pacing, visual storytelling, payoff, retention risks, factual citations, audio sync, frame ranges, assets, and export/handoff completeness. Give prioritized concrete edits with examples and uncertainty. Distinguish critique from approval: this skill cannot approve, advance gates, render, or publish. Log concise findings and next decision.
