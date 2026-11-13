# Format tests
Creator decision, 2026-11-13: test each change before it becomes a channel rule. Nothing here is settled until its row says "kept" or "dropped". Topic branches are tracked separately in `branch-test-plan.md`.

## How a test is read
- **Baselines** (creator's analytics, 2026-11-13): EP003 65.4% stayed, 78% average viewed, 1.9K views. EP004 61.5% stayed, 63% average viewed, 1.1K views in its first 13 hours. EP002 41.0% stayed.
- **Measures:** stayed to watch, average percentage viewed, views at 24 hours and at 7 days, likes per view, subscribers gained.
- **One video is one sample.** At 1K to 2K views per video, a single result is a hint. A change is "kept" only after it has appeared in at least two episodes that beat the baseline, and "dropped" after two that do not.
- **Each episode's concept card states which tests it carries.** Its results are entered below at 24 hours and 7 days.
- **Topic changes with every episode,** so no test here is clean. Read each result next to that episode's topic.

## Register
| # | Change under test | Against | Cost to try | Status | Episodes and results |
|---|---|---|---|---|---|
| 1 | Stakes-first opening: premise and stakes in the first sentence, about ten words | anti-hook (understated, context-light) | script only | not started | |
| 2 | Title and first line say the same thing | title carries the half the hook withholds | script only | not started | |
| 3 | Short sentences (about 6 to 9 words), fragments allowed | story-chain paragraph (EP003 12.6, EP004 11.6 words per sentence) | script only | not started | |
| 4 | Second person ("you") | third person | script only | not started | |
| 5 | Ending that loops into the first line, or a callback joke, on a full picture | closing callback, then fade to black | script and finish | not started | |
| 6 | No fade-in: first frame lit with the first caption up | fade from black | finish only | not started | |
| 7 | Phrase captions (2 to 4 words), about twice the size, one highlighted keyword | one small white word at a time | finish only | not started | |
| 8 | A new picture every 2 to 3 seconds, hard cuts allowed | long continuous camera moves | storyboard and render | not started | |
| 9 | An on-screen object for each spoken number or key noun | captions only | storyboard and render | not started | |
| 10 | 3D characters (sphere head, painted face, bean body, thin limbs) | flat cutout cards | new character build | not started (look test not yet approved) | |
| 11 | Flat colour fills, two tones, darker and more saturated | painted textures, three tones (EP004 pale and bright) | new look | not started (look test not yet approved) | |
| 12 | Character in most shots, several faces per scene | character in about a third of views, one face per card | storyboard and render | not started | |
| 13 | Length of 60 to 90 seconds | 36 to 54 seconds | script | not started | |

## Suggested order (the creator decides)
Changes that cost nothing to produce come first, so the expensive ones are tested on a stronger base.
1. **Script group (1 to 4):** no production cost.
2. **Finish group (5 to 7):** no Blender render.
3. **Picture group (8, 9, 12):** storyboard and render time.
4. **Look group (10, 11):** needs an approved look test first.
5. **Length (13):** once the opening holds viewers.

Testing a group at once is faster but cannot say which change inside it mattered. If a group wins, its changes can be separated later.
