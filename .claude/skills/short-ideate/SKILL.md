---
name: short-ideate
description: Run the topic stage (seed list, five checks, title and first line), then develop the creator-selected seed into a concept card and stop at explicit idea approval.
disable-model-invocation: true
---
# Short Ideate
Read `me.md`, routing, mentor protocol, production standards, and channel identity. The creator owns the premise: a seed becomes the episode's seed only when the creator supplies it or explicitly selects it.

## 1. Topic stage
Run this first. Skip it only when the creator arrives with one chosen seed and says to go straight to the concept card.
1. **Seed list.** Gather 10 to 15 one-line seeds and label each with its source:
   - the creator's own seeds, kept verbatim
   - subjects that are timely in the next two to four weeks (check each with a source and access date before calling it timely)
   - comments on the channel's own videos (ask the creator to paste them)
   - the frame of the channel's best-performing video with a new subject (`03_TRACKING/branch-test-plan.md`)
   - big "you" questions in science branches not yet tested
   Seeds that Claude suggests are marked as suggestions. They are prompts for the creator, not premises. Reference channels show a method only; never copy a reference title, premise, or voice (`02_CONTEXT/source-analysis/channel-reference-notes.md`, `reference-video-analysis-2026-11-13.md`).
2. **Five checks** for each seed, answered yes or no with one line of reason:
   - Do strangers already care about the subject before the video says anything?
   - Can the stakes be said in about ten words that work as both title and first line?
   - Can it be told as "you"?
   - Is there a chain of at least six distinct pictures?
   - Is there an honest answer with sources that can be found?
3. **Title and first line** for the three strongest seeds.
4. Present the seed table and the three title and first-line pairs. The creator selects one, rewrites it, or rejects all. Stop here until they do. Their selection, in their words, is the seed.

## 2. Concept card
Preserve the seed verbatim. Develop up to three framings derived from it; show central question, working title and first line, hook promise, audience assumption, emotional shape, visual opportunity, payoff, research path, and risks. Cite any factual claims. State which format tests the episode carries (`03_TRACKING/format-tests.md`). Mentor critiques both concept and storytelling without imitating the transcript creator. Present a versioned concept card and ask for explicit approval/revision. Stop; do not script or advance state without approval. After explicit creator approval, run the documented `approval_state.py record` command for the exact displayed version and record the decision in episode files. Never record approval for ambiguous assent.
