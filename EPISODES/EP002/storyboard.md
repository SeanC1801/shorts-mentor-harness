# EP002 Storyboard v2 (DRAFT, awaiting creator re-approval)

- Episode/version: EP002 / storyboard v2 (supersedes approved v1: same shots, visuals, and transitions; timing now measured from narration)
- Approved script version: v6 (approved 2026-10-31); approved idea version: v2
- Narration audio: `audio/EP002-narration-v1.mp3` (ElevenLabs, licensed/library voice per creator), **35.396 s measured**. Total 850 frames (35.42 s) at 24 fps, 1080x1920. Shot boundaries sit in the measured pauses; word times in `audio/word-timings-v1.json` (pause anchors, about +/-0.1 s per word). Audio tags [thoughtful] [short pause] [sighs] [chuckles] are delivery directions, not words; spoken wording matches script v6.
- Machine-readable plan: `episode.json` (passes `validate_episode.py`; the validator checks structure and timing only and does not verify media or render anything).
- Animation: renderer phases 1-3 done with provisional timing; phase 4 re-times to this storyboard. Preview approval is a separate gate.

## Style basis (creator preference)
Ricks Clips-inspired *craft*, per `animation-style-notes-ricks-clips.md`: simple flat expressive original characters over rich layered backgrounds, scale contrast, wide establishing plus close-up, glow for the reveal, in-scene props with readable text, large word-by-word captions in the lower half. Characters and designs are original and approved (CHAR-PIGEON spec v3, CHAR-SKINNER-STANDIN v1).

## Shot table
| Shot | Frames | Narration | Visual | Character / pose | Camera | Transition |
|---|---|---|---|---|---|---|
| S01 | 0–86 (0.00s–3.58s) | The U.S. government once paid to teach pigeons to aim. | Opening anti-hook image: ONE focal point. A single pigeon in close-up, eyes locked on a glowing target on a small screen in front of it; plain soft background, nothing else. No bomb yet. | CHAR-PIGEON / POSE-PIGEON-ALERT | Slow push-in toward the pigeon's eyes | cut → match-cut-to-wide |
| S02 | 86–188 (3.58s–7.83s) | Here's the setup: in the nose, a pigeon watches a screen showing the target. | Reveal wide: cutaway of a bomb nose cone. Tiny pigeon on a perch facing a glowing screen with a target; scale contrast (huge metal interior, small bird). Match the screen glow from S01. | CHAR-PIGEON / POSE-PIGEON-WATCH | Pull-back from close-up to wide cutaway, subtle parallax between interior layers | match-cut-to-wide → cut |
| S03 | 188–266 (7.83s–11.08s) | The bird pecks. The image shifts. The controls move. | Rule of three in one shot, three beats: (1) close-up beak pecks the screen target, (2) target image slides on the screen, (3) cutaway outside: a tail fin tilts. Each beat on its own hit, hard accents. | CHAR-PIGEON / POSE-PIGEON-PECK | Quick punch-ins on each beat; short whip between screen and fin | cut → cut |
| S04 | 266–371 (11.08s–15.46s) | One pigeon is a gamble, so the plan used three, and the majority would win. | Three pigeons in a row, each facing its own screen; a vote board above them with three lights. Two lights turn green, one stays off, showing majority. Wide frame, readable on-screen prop. | CHAR-PIGEON / POSE-PIGEON-PECK | Static wide with slow lateral drift; brief punch-in on the vote board | cut → cut |
| S05 | 371–473 (15.46s–19.71s) | This was World War Two, and the idea came from psychologist B. F. Skinner. | Period context: a simple 1940s lab with a table. Stylized stand-in character for the psychologist (no real likeness) beside a pigeon on the table; a name card prop reads 'B. F. Skinner' and a banner reads 'World War II'. | CHAR-SKINNER-STANDIN / POSE-STANDIN-GESTURE | Slow lateral drift with parallax across the lab layers | cut → cut |
| S06 | 473–600 (19.71s–25.00s) | And here's what nobody expected: in simulations, the trained birds kept the target centered. | Reveal: close on the screen with a bright radial glow as the target stays locked in the center of crosshairs; on-screen label 'SIMULATION'. Pigeon in foreground silhouette, pleased. Must not suggest a live flight. | CHAR-PIGEON / POSE-PIGEON-PROUD | Push-in on screen; glow pulse; slight parallax between pigeon and screen | cut → cut |
| S07 | 600–772 (25.00s–32.17s) | So why isn't this how missiles work? In 1944 it was cancelled so the military could focus on weapons it could use sooner. | Wide office: a huge desk, a calendar showing 1944, papers; a giant CANCELLED stamp comes down on a project folder. Tiny pigeon on the desk edge watches, deflated. Scale contrast again. | CHAR-PIGEON / POSE-PIGEON-DEFLATED | Static wide, then punch-in on the stamp at impact, ease back out | cut → cut |
| S08 | 772–850 (32.17s–35.42s) | The birds could aim. Nobody wanted to bet a war on them. | Closing image: the pigeon on a runway beside a huge bomb, small against it; pigeon looks at the camera, a beat of silence. Clean hold, no extra elements. | CHAR-PIGEON / POSE-PIGEON-DEADPAN | Slow pull-back revealing the bomb's size; final hold | cut → fade-out |

## Craft notes
- **Anti-hook:** S01 has one focal point (a pigeon and a target screen) and no bomb, so line 1's question stays open; S02's wide reveal answers "where".
- **Rule of three:** S03 holds three hard beats (peck, image shift, fin tilt).
- **Scale contrast:** a tiny pigeon in a huge nose cone (S02), a huge desk (S07), and a huge bomb (S08).
- **Honesty:** S06 carries an on-screen "SIMULATION" label and no flight imagery, per the claim ledger (C6). S07's "1944" and "CANCELLED" props rely on claim C4 (secondary-sourced).
- **Real person:** the psychologist is a stylized stand-in with a name card, not a likeness.
- **Captions:** `CAPTION-WORD-BY-WORD`, bottom, kept clear of the pigeon's face and the key action; the renderer would split words by measured narration timing.
- **Motion:** poses on twos (12 effective fps); camera and parallax at 24 fps.

## Continuity and retention notes
- The target screen's glow carries from S01 through S06 as a visual thread.
- Retention risk: S05 (context) is the flattest beat. Keep it to a quick lateral drift, and consider cutting to the stamp sooner if pacing drags.
- Closing hold in S08 is deliberately quiet; the creator may prefer a different last image.

## Assets (approved key frames S01-S08 in `02_CONTEXT/assets/scenes/`; see manifest)
Characters: pigeon (6 poses), psychologist stand-in. Props: target screen, fin mechanism, vote board, name card, simulation label, cancelled stamp, 1944 calendar, large bomb. Backgrounds: soft gradient, nose-cone cutaway, 1940s lab, wide office, runway. FX: radial glow. Audio: narration (ElevenLabs), SFX (soft tone, peck tap, fin click, vote chime, lock-on, stamp thump), ambience (metal hum, lab room).

## Open decisions for the creator
1. Pigeon design: original, expressive, and approved before any art (`character-registry.md`).
2. Whether the psychologist appears as a stand-in or only as a name card.
3. Closing image in S08.

## Storyboard approval (artifact version, decision, timestamp)
v1 approved by Sean Caling 2026-10-31 (provisional timing). v2 (measured timing): pending creator re-approval.
