# Friday

**A comprehension gate for AI-assisted code.**

Code is done when tests pass. A slice is done when you can explain it without
looking. Friday holds that second line.

```
FRIDAY  AeroFlow

  SPINE
   ▲ main.py                          DEBT
   ● schemas.py                       understood   guessing, rung 1
   · static/js/state.js               dark

  ORGANS
   ● static/js/board.js               understood   think-so, rung 0
   · update_layout.py                 dark

  LEAVES  6 files, ungated

  ██████████████░░░░░░░░░░░░░░░░░░░░  2/5 understood (40%)
  2 dark   2 understood   1 debt
```

---

## The problem

Anthropic's *How AI Impacts Skill Formation* ran a randomised trial with 52
engineers. The AI-assisted group finished in about the same time as the control
group and scored **17 points lower** on a comprehension test afterward — 50% vs
67%, with the largest drop in debugging. Passive delegation is what does the
damage, not AI use itself.

Meanwhile the complaint from senior engineers is never that the code is ugly.
It is *"I ask them why they made certain decisions, and they give me this blank
look."*

The failing artifact is not the code. It is the developer.

## What Friday does

1. **Tiers your repo** into Spine, Organs and Leaves, so ceremony is
   proportional to blast radius. Styling never gets questioned; your data model
   always does.
2. **Gates commits** on Spine and Organs code you have not explained — via a
   git pre-commit hook, so it works with any agent, any editor, any plan.
3. **Asks you three questions** about the slice you just built: what breaks if
   this is removed, what did you deliberately not do, walk this input to its
   output. Graded against your real code.
4. **Descends a hint ladder** when you get one wrong, instead of repeating the
   question at you.
5. **Records concepts, not files** — because the same misunderstanding shows up
   in three places before you notice it is one misunderstanding.

## It found real bugs in ten minutes

Friday was validated by hand, with no tooling, on a half-finished FastAPI
project the author had built with AI. In one session it surfaced:

- **A wrong mental model.** The author believed the project ran with
  `npm run dev`. There is no `package.json`; it is a FastAPI app started with
  `uvicorn`. Caught from the file manifest alone.
- **46KB of orphan files** — a quarter of the codebase — referenced by nothing
  and absent from the project's own README.
- **A live bug in the data model.** A Pydantic default meant that any client
  omitting `project_code` got a silent success and its task filed under the
  demo project, invisible to the user who created it.

All three now reproduce automatically:

```
$ friday doctor --run "npm run dev"

  Run-command mismatch
    your claim says 'npm' — but none of package.json exist here.
    Your model of how this project starts is wrong.

  Duplicate filenames  (path tiering cannot tell these apart)
    index.html
      index.html                 19.2KB
      templates/index.html       22.7KB

  Orphans  (referenced by nothing else)
    update_layout.py             25.7KB
```

## Install

Zero dependencies. Python 3.8+. Works in any repo, any language.

```bash
curl -O https://raw.githubusercontent.com/<owner>/friday/main/scripts/friday.py
python3 friday.py init
python3 friday.py tier          # review the proposal
# correct the globs in .friday/config.json — this part matters
python3 friday.py tier --apply
```

**Correct the tiers before applying.** The cold pass gets things wrong on
purpose-built names — a file called `main.py` may be where your whole database
lives. Your correction is the point, not a failure of the tool.

## Three ways to run it

Nothing essential lives above Tier 0. Higher tiers remove friction; they add no
capability.

| Tier | Needs | Gives you |
|---|---|---|
| **0 — Protocol** | Nothing | The full loop, by hand or pasted into any agent: Claude free plan, Codex, Cursor, Gemini CLI, opencode. Git hook enforces. |
| **1 — Skill** | Free Claude plan, or Claude Code | `SKILL.md` — Claude runs the gate automatically |
| **2 — Plugin** | Paid Claude plan | Marketplace install, `/gate` and `/map` commands |

The paper test above was run entirely at Tier 0.

## Commands

```bash
friday init                            # scaffold + install the git hook
friday tier [--apply]                  # cold tiering pass
friday map [--all]                     # the understanding map
friday doctor --run "npm run dev"      # test your belief about the repo
friday mark <path> understood --confidence guessing --rung 1 --concept <id>
friday override <path> "reason"        # never blocked, always recorded
friday ledger                          # concept registry
```

## Design rules

Four that shaped everything else:

**Hard boundaries beat more prose.** More instructions give an agent more
semantic material to juggle. Validation gives it an actual edge. The gate is a
git hook, not a paragraph in a rules file.

**Ceremony proportional to blast radius.** Gate the Spine, ignore the Leaves.
This is the difference between a tool you use for a year and one you abandon in
week three.

**A number is allowed only if it cannot go up without your understanding going
up.** This kills streaks, XP, badges and leaderboards. A streak on a
self-graded gate creates pressure to cheat the gate.

**Never blocked, always recorded.** The override takes one command and no
guilt. It writes visible red debt that does not fade. The cost is paid every
time you open the map, not at the moment you are under pressure.

## What this is not

**Not spec-driven development.** GitHub Spec Kit, OpenSpec, Kiro and BMAD
already solve specification, and solve it well. Use one of them for the
planning half. Friday is the other half — it starts after the code exists.

**Not a slop-word linter.** Prose style is the shallowest layer of this
problem. Suppressing one stylistic tell just routes the pressure into another.

**Closest prior art** is [PR Quiz](https://github.com/marketplace/actions/pr-quiz)
and [Gater](https://usegater.app/), which generate comprehension quizzes from
pull requests. Both fire at PR time, on a finished diff, aimed at a reviewer on
a team. Friday fires inside the authoring loop, on your own code, before the
slice is finished — while the design can still change.

## Honest limitations

- **You can cheat it.** Paste the question into a second agent and you will
  pass. There is no technical fix. But counterfactual questions *are* the
  learning mechanism, so cheating costs you the only thing being built. Gym,
  not exam.
- **State is per file; understanding is per slice.** File-level is what a map
  can render. Deliberate trade.
- **Path tiering cannot see what is wired in.** That is what `doctor` is for.
- **Orphan detection is a substring search**, not a parser. It will produce
  occasional false positives in dynamically-loaded codebases.

## Trust

You are being asked to run this inside your own repo, so: no network calls, no
telemetry, no local MCP server, no dependencies. One Python file, ~600 lines,
readable in a sitting. Read it before you run it.

MIT licensed.
