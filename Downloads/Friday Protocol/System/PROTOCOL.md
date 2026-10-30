# The Friday Protocol

**The build artifact is your understanding, not the code.**

Code is done when tests pass. A slice is done when you can explain it without
looking.

This file is the whole product. It works with no tooling, in any agent, on any
plan. Everything else in this repo removes friction from it.

---

## Who this is for

Someone who uses AI to write code and has noticed they can no longer explain
what they shipped. Not someone trying to stop using AI.

The failure mode this targets is documented. Anthropic's *How AI Impacts Skill
Formation* found that engineers using AI finished tasks in about the same time
as a control group and scored 17 points lower on a comprehension test
afterward — 50% vs 67%, with the largest drop in debugging. The researchers
found that *passive delegation* is what does the damage, not AI use itself.

So this protocol does not slow down your typing. It changes one thing: it
makes you predict before you look, and explain before you move on.

---

## 1. Tier the repo

Not all code deserves the same ceremony. Gate the parts with blast radius,
ignore the rest. This is what makes the habit survivable.

| Tier | What lives there | Rule |
|---|---|---|
| **Spine** | Data model, invariants, auth, money, anything expensive to reverse | You write it or you spec it line by line. The agent drafts nothing unprompted. Gated. |
| **Organs** | Wiring between modules, integration boundaries, error handling | Agent drafts one slice. You state the contract first. Gated. |
| **Leaves** | Styling, copy, config, glue, throwaway scripts | Agent goes. Never gated, never questioned. |

Tiering runs off file paths and size only — never language parsing. That is
deliberate: it has to work in languages you have never seen.

**Two heuristics worth knowing:**

- **Size promotion.** Past ~30KB, a code file gets promoted regardless of its
  name. Nobody holds 30KB of logic in their head.
- **Path names lie about data ownership.** A file called `main.py` sounds like
  an entry point; it may be where your entire database lives. The cold pass
  will get this wrong. *Your correction is the point*, not a failure of the
  tool.

---

## 2. Contract before code

Before the agent writes anything in Spine or Organs, you write two or three
sentences:

- What this slice should do
- What it must not touch
- How you will know it worked

That is the whole ceremony. It is not a spec document — it takes twenty
seconds.

The pre-commitment is the mechanism. Prediction before reveal is what creates
learning; without it you are reading an answer key.

> **Use a real spec tool for the planning layer.** GitHub Spec Kit and OpenSpec
> already solve specification properly. This protocol is the other half.

---

## 3. The gate

After the slice, before you move on. **Maximum three questions.**

### Declare confidence first

Before you see the questions, say one of: **sure / think-so / guessing.**

This is not decoration. Confident-and-wrong is the dangerous state and the one
you cannot detect from the inside. Declaring first is the only way to measure
it.

### The three question types

**Counterfactual — "What breaks if this is removed?"**
Cannot be pattern-matched. Bluffing produces obviously generic answers.

**Trace — "This input arrives. Walk it to the response."**
Catches the case where you know the vocabulary but not the flow.

**Boundary — "What did we decide *not* to do here, and why?"**
Catches silent architectural drift, where the agent solved a different problem
than the one you posed. This is the one that finds real bugs.

**Never multiple choice.** Recognition is easy to fake and teaches nothing.
Answers are open-ended, in plain language, graded against the real code rather
than a stored answer key — so a confident wrong answer gets caught.

### The hint ladder

Failure never repeats the same question. It descends:

```
  rung 0   counterfactual, as asked
     ↓     wrong
  rung 1   narrower question, one mechanism named for you
     ↓     wrong
  rung 2   trace of just the three or four relevant lines
     ↓     wrong
  rung 3   the answer, given directly
           → file marked TAUGHT, short decay interval
```

You never get stuck. You never get punished. You descend until you find the
rung you can stand on, and the system remembers where that was.

**This is not optional.** A gate without a ladder is a wall, and walls are
where people quit.

### Language fluency

You will work in languages you do not know. Without this rule the gate asks
about unfamiliar syntax, you fail constantly, and you quit inside two weeks.

| | Counterfactual | Boundary | Trace |
|---|---|---|---|
| Language you know | ✅ | ✅ | ✅ |
| Language you are learning | ✅ | ✅ | suppressed at first |

Syntax fluency was never the goal. You can be entirely non-fluent in Rust and
still know what a module is responsible for, what it must never do, what breaks
if it is removed, and what you deliberately chose not to build. That is the
understanding that prevents 3am outages, and it transfers across languages.

---

## 4. States

| State | Meaning |
|---|---|
| `dark` | Never explained |
| `taught` | The answer was given, not derived. Short decay. |
| `understood` | Derived, with at most one hint |
| `stale` | Decayed past its interval |
| `debt` | A gate was skipped. Red. Does not fade. |

The `taught` / `understood` distinction matters: things you are told fade
faster than things you work out.

---

## 5. The override

**Never blocked. Always recorded. The record is visible.**

One command, one short reason. No friction, no guilt text, no confirmation
dialog. It writes a `debt` entry that renders red and does not decay. It clears
only when you go back and pass the gate you skipped.

The cost is not paid when you use it — that is when you are under pressure and
would resent it. It is paid every time you open the map. Honest accounting, not
punishment.

**Signal:** three or more outstanding overrides means stop and run a
comprehension session.

---

## 6. The ledger

Every failed gate records **a concept, not just a file.**

This matters more than it sounds. In the first real run of this protocol, two
separate failures traced to the same underlying gap — a plain string standing
in where a reference belongs, failing silently rather than erroring. Recorded
per file, that is two unrelated incidents. Recorded per concept, it is one
misunderstanding with two more instances waiting elsewhere in the codebase.

**Promotion rule:** a concept becomes a written project rule only after its
**third** hit.

Without that discipline your rules file bloats into the dumping ground that
caused the problem in the first place. Hard ceiling: **one screen.**

---

## Running this by hand

No tooling, any agent, any plan. Paste this into your session:

```
Run the Friday gate on the slice we just finished.

1. Ask me to declare confidence: sure / think-so / guessing.
2. Then ask at most 3 questions about the code you just wrote:
   one counterfactual, one boundary, and a trace only if this is a
   language I told you I know.
3. Grade my answers against the actual code, not against what you
   expect me to say.
4. If I get one wrong, do NOT repeat the question. Descend the hint
   ladder: narrower question → trace of the specific lines → tell me
   the answer outright and mark it TAUGHT.
5. At the end, name the *concept* behind any failure, not just the file.

Do not soften the grading. A wrong answer I believe is worse than a
wrong answer I know about.
```

That is the entire product. Everything else is convenience.

---

## Anti-goals

Things this protocol deliberately refuses to become:

- A slop-word linter. Prose style is the shallowest layer of this problem.
- A rules file longer than one screen.
- A gate on anything without blast radius.
- More than ~90 seconds of friction per slice.
- Streaks, XP, badges, levels, leaderboards.

That last one is a design rule, not taste:

> **A number is allowed only if it cannot go up without your understanding
> going up.**

Any score you can inflate by showing up, complying, or cheating will be
inflated, and you will have built a machine that rewards the exact behaviour it
exists to prevent.

---

## Honest limitations

- **The gate is self-graded and you can cheat it.** You can paste the question
  into a second agent. There is no technical fix and pretending otherwise would
  be dishonest. But counterfactual questions *are* the learning mechanism, so
  cheating costs you the only thing being built. This is a gym, not an exam.
- **State is per file; understanding is per slice.** File-level is what a map
  can render. The imprecision is accepted deliberately.
- **Path tiering cannot see what is wired in.** Orphaned files and duplicate
  filenames need a separate check.
