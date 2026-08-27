# Friday — comprehension gate

This repo uses the Friday protocol. The build artifact is the developer's
understanding, not the code.

**Read `PROTOCOL.md` for the full procedure.** Summary of your obligations:

- Before writing Spine or Organs code, ask the developer for a one-sentence
  contract: what it does, what it must not touch, how they will know it worked.
- After the slice, run the gate: ask for a confidence rating, then at most
  three questions (counterfactual, boundary, and trace only in languages listed
  in `.friday/config.json`). Never multiple choice.
- Grade against the real code. On a wrong answer, descend the hint ladder —
  never repeat the same question.
- Record the outcome with `python3 .friday/friday.py mark <path> <state>`.
- Never gate Leaves. Never ask about syntax in a language the developer has not
  claimed fluency in.

A commit blocked by the pre-commit hook means a Spine or Organs file is staged
without being explained. Run the gate; do not suggest removing the hook.
