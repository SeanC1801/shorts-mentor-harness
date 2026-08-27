# Comprehension Gate — Design Document

**Status:** Validated by paper test. Not yet built.
**Working name:** placeholder. Candidates: `gate`, `understood`, `lumen`, `cartograph`.
**Date:** August 2026

---

## 1. The problem

Slop is not a property of code. It is the gap between what an agent produced and what the human understands.

The evidence for treating this as a real, named problem rather than a vibe:

- **Anthropic, *How AI Impacts Skill Formation*.** Randomized trial, 52 engineers learning a new library. The AI-assisted group finished in about the same time as the control group and scored 17 points lower on a follow-up comprehension quiz — 50% vs 67%. Largest declines in debugging. The researchers stress that *passive delegation* harms skill formation far more than active, question-driven use.
- **Addy Osmani, "Comprehension Debt: The Hidden Cost of AI-Generated Code"** (O'Reilly Radar). Names the failure mode. Key line of reasoning: surface correctness is not systemic correctness; tests cannot answer whether a change was necessary, only comprehension can.
- **Field evidence** — r/ExperiencedDevs "How to deal with juniors shipping AI slop code?" The complaint is never that the code is ugly. It is *"whenever I ask them why they made certain decisions, they just give me this blank look."* The failing artifact is the developer.

### The design consequence

> **The build artifact is understanding, not code.**

Code is done when tests pass. A slice is *done* when the author can explain it without looking.

---

## 2. What this is not

Positioning matters because the adjacent category is saturated. State this explicitly in the README.

**Not spec-driven development.** GitHub Spec Kit (~93k stars), OpenSpec (~52k), GSD (~61k), BMAD, Kiro, Cursor Plan Mode and Tessl all occupy the "write a spec, then generate against it" space. Building another one is building a worse Spec Kit.

→ **Use Spec Kit or OpenSpec for the spec half.** This project is the other half.

**Not a slop linter.** Prose-level anti-slop is the shallowest layer and the most crowded. Two findings from the source material argue against it directly:
- Suppressing one slop channel routes pressure into another (farwanderers' hydraulic finding — kill vocabulary and hedging, em dash density spikes).
- No anti-slop instruction fixes an incoherent thought underneath (Own_Pool_1369).

**Adjacent prior art, and the difference.** PR Quiz (GitHub Action) and Gater (GitHub App) both generate comprehension quizzes from pull requests. Both fire at **PR time**, on a **finished diff**, aimed at a **reviewer on a team**.

This fires **inside the authoring loop**, on **your own code**, **before the slice is finished**, while the design can still change. That is the wedge.

---

## 3. Core principles

1. **Hard boundaries beat more prose.** More instructions give the agent more semantic material to juggle. Validation gives it an actual edge. (pleblifeTV)
2. **One constraint, one owner, stated once, at the narrowest level that governs it.** Violating this is how `AGENTS.md` becomes a dumping ground and starts *causing* slop.
3. **Ceremony proportional to blast radius.** Gate the Spine, ignore the leaves. This is what makes the tool survive past week three.
4. **Every number must be a measurement, not a reward.** A score is allowed only if it cannot go up without understanding going up. This single rule kills streaks, XP, badges, levels, and leaderboards.
5. **Never blocked, always recorded.** Escape hatches must exist and must leave a visible mark.
6. **Gate on intent and consequence, never syntax.** Required for multi-language work. See §7.

---

## 4. The tier model

Derived from nmleart's spine / skeleton / organs framing, made operational. The quote as written ("never let the agent design anything by itself") is unsustainable; tiering is the fix.

| Tier | Contents | Gate behaviour |
|---|---|---|
| **Spine** | Data model, invariants, auth, money, anything expensive to reverse | Human-authored or line-by-line specced. Agent drafts nothing unprompted. Full gate before it lands. |
| **Organs** | Wiring between modules, integration boundaries, error handling | Agent drafts one slice. Contract stated first. Gate is a real explanation. |
| **Leaves** | Styling, copy, config, glue, throwaway scripts | Agent proceeds freely. Logged, never questioned. |

### Tiering heuristics (v1 — no language parsing)

Deterministic, driven only by git and path globs. Must work in languages the user has never seen.

1. **Path globs.** User-defined, per project. Seeded by a cold pass that the user corrects.
2. **Size promotion.** Past a threshold (~30KB), promote a file regardless of name. Nobody holds 40KB of logic in their head. *(Derived from the paper test: `board.js` at 46KB is the same size as the entire stylesheet.)*
3. **Orphan detection.** Files not referenced by any documented entry point are flagged, not tiered.
4. **Run-command reconciliation.** Compare the stated run command against what is actually present in the repo. *(This check alone caught a wrong mental model in the paper test before a single question was asked. Cheap, high yield, ships in v1.)*

### Known limits, accepted

- **Path names lie about data ownership.** In the test, `main.py` read as an entry point but actually holds the in-memory database — Spine, not Organs. No path heuristic catches this. User correction is the fix.
- **State is per-file, understanding is per-slice.** Slice-level state is unrenderable on a map. Accept the imprecision; record slice IDs alongside for later.

---

## 5. The state model

This is the project's own **Spine**. Human-authored, non-negotiable, expensive to reverse. Everything downstream — gate, map, ledger, decay — depends on it.

Lives in the repo. Committed to git. Survives session resets. Visible on GitHub.

### Per-file entry

| Field | Purpose |
|---|---|
| `path` | Key |
| `tier` | spine / organs / leaves |
| `state` | dark / taught / understood / stale / debt |
| `last_verified` | Timestamp, drives decay |
| `confidence` | Self-rated at last check: sure / think-so / guessing |
| `ladder_depth` | How far down the hint ladder the last pass required |
| `slice_ids` | Which slices touched this file |
| `concepts` | Concept IDs implicated in failures here |

### States

- **dark** — never explained
- **taught** — the answer was given, not derived. Short decay interval.
- **understood** — derived, with at most one hint
- **stale** — decayed past interval
- **debt** — override used. Red on the map. Does not decay, does not fade. Cleared only by passing the gate that was skipped.

### Concept registry — required, not optional

**This is the change the paper test forced.** Both failures in the test were the *same underlying misunderstanding* appearing twice: a string standing in where a reference belongs, failing silently. If the ledger only recorded "failed on `schemas.py`", it would miss that the same gap is waiting in `main.py` and `board.js`.

So: **failures are recorded per concept, not per file.** The recurrence rule (§9) counts concept hits, not file hits.

---

## 6. The gate

Fires after a Spine or Organs slice, before moving on. Maximum three questions.

### Question types

- **Counterfactual** — "What breaks if this is removed?" Hard to bluff, cannot be pattern-matched.
- **Trace** — "This input arrives; walk it to the response." Catches vocabulary-without-flow.
- **Boundary** — "What did we decide *not* to do here, and why?" Catches silent architectural drift, where the agent solved a different problem than the one posed.

Open-ended short answer. **Never multiple choice** — recognition is easy to fake and teaches nothing. This is the weak point in existing tools.

Graded against the real code, not a stored answer key, so a confident wrong answer gets caught.

### The hint ladder — mandatory in v1

Originally scoped as v2. **The paper test promoted it.** The user hit a wall on both questions; without descent, that session ends in frustration.

Failure never repeats the same question. It descends:

```
counterfactual
  → narrower counterfactual, one mechanism named
    → trace of just the relevant lines
      → the answer given directly; file marked TAUGHT, short decay
```

You never get stuck. You never get punished. The system records which rung you landed on.

### Fluency suppression

The user is Python-fluent and works across languages they don't know. Without this rule, the gate asks about unfamiliar syntax, the user fails constantly, feels stupid, and quits within ten days. **This is the most likely path to abandonment.**

Config declares fluent languages. Then:

| | Counterfactual | Boundary | Trace |
|---|---|---|---|
| Fluent language | ✅ | ✅ | ✅ |
| Learning language | ✅ | ✅ | suppressed until entries mature |

Justification: syntax fluency was never the goal. You can be entirely non-fluent in Rust and still know what a module is responsible for, what it must never do, what breaks if it's removed, and what you deliberately chose not to build. That understanding prevents 3am outages and it transfers across languages.

---

## 7. The override

**Chosen behaviour: hard stop by default, override available.**

The whole design rests on how the override behaves. Too painful and the user routes around it; too easy and it becomes the default path.

**Rule: never blocked, always recorded, the record is visible.**

- One command, one short reason. No friction, no guilt text, no confirmation dialog.
- Writes a `debt` entry. Renders **red** on the map.
- Does not decay. Does not fade. Sits there looking wrong.
- Cleared only by going back and passing the skipped gate.

The cost is not paid at the moment of use — that is when the user is under pressure and would resent it. It is paid every time the map is opened. Honest accounting, not punishment. Same logic as technical debt: fine to take on deliberately, dangerous to take on invisibly.

**Signal:** three or more Spine overrides visible at once means stop and run a comprehension session.

---

## 8. The map — v1 deliverable

Repo rendered as files, each lit or dark by state. Nothing is awarded; it is a picture of a true state.

Why this first: the map cannot be built without first answering *what is the unit of understanding and what states can it be in*. **"Map first" means "schema first,"** which is the correct starting point — everything else is downstream, and getting it wrong means rewriting in week three.

Also the demo. Open a repo, half of it is dark, run three slices, it lights. Fifteen seconds, whole pitch.

**v1 scope:** define the state model, hand-seed with real data from the paper test, render. No gate logic, no decay, no ladder automation. One to two days.

---

## 9. The ledger

Every failed gate and every agent drift writes one line: concept, file, ladder depth.

**Promotion rule:** a lesson becomes a project rule only after the **same concept** recurs three times.

Without this discipline the rules file bloats into exactly the `AGENTS.md` dumping ground that causes the original problem. The rules file has a hard ceiling: **one screen.**

---

## 10. Deferred to v2+

- **Calibration scoring.** Score self-assessment accuracy, not correctness. Confident-and-wrong is the worst outcome and the most useful signal. Quietly cheat-resistant: looking up the answer produces perfect calibration and a flat, boring number.
- **Decay queue.** Spaced repetition against your own codebase. Inverts the streak — instead of pressure to show up, an honest queue of what is going stale. Keeps the tool alive on days with no commits.
- **Cold open.** Rare, unannounced question about a Spine file from days ago. The only mechanic that measures retention rather than momentary comprehension. Once every few sessions.

---

## 11. Cost design

Constraint: free and token-efficient.

- Only skill **metadata** (name + description) is preloaded at startup. `SKILL.md` is read when relevant; bundled files only as needed. → **Tiny routing `SKILL.md`, `references/` per mode.** Never pay for gate logic while planning.
- **State lives in repo files, not conversation history.** Scripts read the state file; Claude only ever sees the handful of entries for the current slice.
- **Anything deterministic is a script, not a prompt** — which files changed, tier lookup, slice size, run-command reconciliation.
- **Question generation reads the diff, not the repo.** A slice-sized diff is small.
- **Run the gate on Haiku.** It reads a diff and grades a short answer; it does not architect.
- Context note: spec-driven workflows already run 20–40% higher token spend from re-reading spec/plan/tasks every turn. Do not stack prose on top of that.

---

## 12. Standards

### Success criteria — measurable, four weeks of real use

1. Can explain any Spine or Organs file cold, 24 hours later. Test: three at random, counterfactuals, score it.
2. Median time-to-gate-pass falls over time. If flat, the questions are noise.
3. Still in use in week four. Adoption by the author is the only adoption metric that matters at this stage.
4. Gate-fail rate on Leaves near zero. If Leaves fail, the tiering is wrong.
5. Calibration gap narrows. Confident-and-wrong should be common in week one and rare by week four. If not, the tool measures without teaching.

### Anti-goals

- Becoming a slop-word linter
- A rules file longer than one screen
- Gating anything without blast radius
- More than ~90 seconds of friction per slice
- Any notification, badge or number that appears on a day with no code written. **The tool has no opinion about whether you showed up.**

### Failure modes, stated honestly

| Risk | Mitigation |
|---|---|
| The gate is self-graded and cheatable | No technical fix. Counterfactuals *are* the learning mechanism, so cheating costs the only thing being built. Framing: gym, not exam. |
| Fatigue | Tiering + hard cap of three questions |
| Gate theater | Flat pass times in the ledger are the tell. If observed, kill it. |
| Language-fluency demoralization | §6 fluency suppression |

---

## 13. Build order

0. **Repo skeleton, MIT, public from the first commit.** The build log is part of the portfolio value.
1. **State model + map.** Hand-seeded from AeroFlow. Validates the schema before anything depends on it.
2. **Deterministic tiering scripts.** Zero dependencies. Path globs, size promotion, orphan detection, run-command reconciliation.
3. **Git pre-commit hook.** The hard stop. Free, universal, vendor-neutral.
4. **Tier 0 protocol document.** `PROTOCOL.md` — the loop runnable by hand in any agent. Ship this before any Claude-specific packaging; it is the product.
5. **Gate skill + hint ladder.** `SKILL.md` and the `AGENTS.md` variant. Ladder is not optional.
6. **Ledger with concept registry.**
7. **Override + debt rendering.**
8. **Plugin wrapper + marketplace manifest.** Convenience layer, last.
9. v2: calibration, decay, cold open.

**Dogfood:** build this using its own method. Tier its architecture, contract before each slice, gate on its own code. If the method cannot survive building its own tool, it is dead — and you lose a weekend rather than a month.

---

## 14. Packaging, portability and distribution

**License: MIT. Public from day one.**

### Plan availability — the constraint that shapes this

| Feature | Availability |
|---|---|
| **Skills** | Free, Pro, Max, Team, Enterprise (requires code execution enabled) |
| **Plugins** | Paid plans only (Pro, Max, Team, Enterprise) |

Skills are **not** paywalled. Plugins are. Therefore **no essential capability may live in the plugin layer.**

### Enforcement lives in git, not in the agent

The original draft put the hard stop in a plugin hook. That paywalls enforcement and ties it to one vendor. Corrected:

> **The hard stop is a git pre-commit hook.**

It reads the state file, sees a Spine file staged in state `dark`, and refuses the commit. Free, universal, works with any agent, any editor, any language, any plan — and it does not care whether an AI wrote the code at all.

This is stronger than an agent-side hook, and it satisfies Principle 1 more honestly: the boundary lives in tooling everyone already has.

### Three tiers — progressive enhancement

| Tier | Requires | Provides |
|---|---|---|
| **0 — Protocol** | Nothing. Markdown + scripts + git hook. | The full loop, run by hand or pasted into any agent: Claude free, Codex, Cursor, Gemini CLI, opencode. |
| **1 — Skill** | Free Claude plan, or Claude Code | Automatic invocation. Question generation, grading, hint ladder. |
| **2 — Plugin** | Paid plan | Marketplace install, one-command updates, `/gate` `/map` `/override` commands, agent-side hooks. |

**Hard rule: Tiers 1 and 2 remove friction only. They add no capability.** A free-plan user running Tier 0 with the git hook has the real product.

*Existence proof: the AeroFlow paper test (Appendix A) was executed entirely at Tier 0 — no tooling, protocol run by hand — and found a wrong run command, 46KB of orphan files, and a live Spine bug. Use this as the README demonstration.*

### Cross-agent support by construction

Tier 0 emits an `AGENTS.md` section alongside `SKILL.md`. Same protocol, different filename, read by Codex, Cursor and most current agents. Combined with the git hook, the tool is agent-agnostic by design rather than by porting effort.

### Distribution

- **Tier 0/1:** clone the repo, or drop `SKILL.md` into `~/.claude/skills/` (global) or `.claude/skills/` (project, committed so collaborators inherit it).
- **Tier 2:** the repo doubles as a plugin marketplace (`.claude-plugin/marketplace.json`). `/plugin marketplace add <owner>/<repo>` then `/plugin install`. Updates propagate on push. No hosting, no infrastructure, no cost.

### Two-repo boundary — hard rule

| Repo | Contents |
|---|---|
| **Tool repo** (public, MIT) | Protocol, scripts, skill, plugin. Universal. Knows nothing about any specific project. |
| **User's project repo** | `.gate/` — state file, tier globs, fluency config. Plus the git hook. Committed by the user. |

**Nothing project-specific ships in the tool.** This is the difference between something anyone can adopt and something that only works on the author's project.

### Constraints to design around

- **Installed plugins are copied to a cache.** Nothing inside can reference files outside its own directory via `../` paths. Everything must live within it.
- **Anthropic's guidance is to install skills and plugins only from trusted sources**, and plugins may include local MCP servers running with the user's own permissions. This project is asking to *be* that trusted source. Therefore: short scripts, no network calls, no local MCP server, no hidden file access — stated explicitly in the README. Auditability is a feature when strangers run your code inside their repos.
- **Zero runtime dependencies** in the Tier 0 scripts. Anything requiring an install is a barrier to the free-tier user this section exists to serve.

---

## Appendix A — Paper test results

**Subject:** AeroFlow. FastAPI + Jinja2 + vanilla JS Kanban board. 11 files, 187KB. Author's own project, half-built.
**Method:** manual loop, no tooling. Cold tiering from file manifest only, then two gate questions on one Spine file.
**Cost:** ~10 minutes, two files read.

### Cold tiering accuracy: 7/11

| Miss | Lesson |
|---|---|
| `main.py` tiered Organs, actually Spine (holds the in-memory DB) | Path names lie about data ownership |
| `update_layout.py` tiered Organs, actually an orphan | Path tiering has no concept of "not wired in" |
| root `index.html` unplaceable | Duplicate filenames across paths defeat path tiering |

### Findings — before a single question was asked

1. **Wrong run command.** Author believed the project ran via `npm run dev`. No `package.json` exists; it is `uvicorn main:app --reload`. Caught from the manifest and one config file.
2. **46KB of orphans** — root `index.html` and `update_layout.py` appear nowhere in the project's own README structure. ~25% of the codebase undocumented.
3. **README/author contradiction** on `state.js` — README describes a `BoardState` class, author described "a few constants." Unresolved; queued as a future gate.

### Gate results — `schemas.py` (Spine)

Confidence declared beforehand: **guessing**.

| Q | Type | Result |
|---|---|---|
| 1 | Counterfactual — `project_code: str = Field(default="DEMO-123")`, client omits the field | **Taught.** Three rungs. Author held "the field ends up empty" throughout; a default means the field can *never* be missing. |
| 2 | Boundary — `TaskUpdate` allows changing `project_code`, `ProjectUpdate` does not | **Understood.** One rung. Author independently reached referential integrity. |

**Calibration: accurate.** Declared guessing, was guessing. No dangerous overconfidence — the safe failure profile.

### Bug found by Q1

`"DEMO-123"` as a default on `TaskBase` means the field is never missing. A client that omits `project_code` gets no error and does not get the current board — the task is silently filed under the demo project, returns 200, and never appears where the user is looking. Only surfaces once real project codes exist. **Logged as a Spine finding.**

### Seed concept registry

| ID | Concept | Hits |
|---|---|---|
| `silent-default` | A default asserts the field can never be missing; every default is a decision about what happens on silence | 1 |
| `string-as-reference` | A plain string standing in for a reference has no integrity constraint; breakage is silent orphaning, not an error | 2 |

Both gate failures trace to `string-as-reference`. This is what forced concept-level rather than file-level ledger recording.

---

## Appendix B — Sources

- Anthropic, *How AI Impacts Skill Formation* — primary citation
- Addy Osmani, "Comprehension Debt: The Hidden Cost of AI-Generated Code," O'Reilly Radar
- Anthropic skill authoring best practices + `anthropics/skills` repo — format spec
- GitHub Spec Kit, OpenSpec — deliberately not rebuilt; cite in README
- PR Quiz, Gater — closest prior art; name them and state the positioning difference
- r/ExperiencedDevs "How to deal with juniors shipping AI slop code?" — field evidence
- r/codex "Has anyone solved slop?" — pleblifeTV on validation gates and constraint ownership
- r/ClaudeAI farwanderers, "anti-slop system prompts" — hydraulic suppression finding
