# Continuity Prompts — quota handoff between models

Claude's free plan resets on a rolling ~5-hour window. If you hit the limit
mid-task, don't lose momentum: hand off to ChatGPT or Gemini using the
template below, keep working, then hand back to Claude once quota resets.
Disclose any handoff in the README per `CLAUDE.md`'s tools-disclosed section.

The trick to a clean handoff is never trusting your memory of "what we were
doing" — hand off the actual files, since they're the ground truth.

---

## A. HANDOFF PROMPT — paste into ChatGPT or Gemini

Copy this, then paste in the actual current content of the four files it
references (CLAUDE.md, the last ~3 CHANGELOG.md entries, the relevant
solution.py, and the last eval/harness.py output) right below it.

```
I'm mid-way through a solo software engineering hackathon
(micro1 Frontier Engineering Challenge) and my primary agent (Claude,
free plan) just hit its usage quota. I need you to continue the SAME
work, in the SAME style, so I can hand back to Claude later with no
drift in approach.

Ground rules (from our working agreement, CLAUDE.md):
- Baseline solution must stay deliberately simple/naive — it's the
  control group. Don't "improve" it.
- Advanced solution must be a MEANINGFUL improvement (capability,
  reliability, efficiency, coverage, or engineering quality) over
  baseline — not cosmetic.
- Every meaningful decision gets logged: trigger (what evidence
  prompted it) → change made → evidence → result → kept or reverted.
  Write your changelog entries in that exact format so they slot
  into our existing CHANGELOG.md without reformatting.
- No secrets/credentials in any code you write.
- Any action affecting a real system/message/payment/real user data
  must be simulated or explicitly gated behind human approval — never
  autonomous.
- Output full files or clearly labeled diffs — I'm copying by hand.

Here is our current state:

[PASTE: current CLAUDE.md]

[PASTE: last 3 entries from CHANGELOG.md]

[PASTE: the solution.py file(s) you're currently working on]

[PASTE: the most recent eval/harness.py output — pass/fail, scores, errors]

My immediate next task: [DESCRIBE WHAT YOU WERE ABOUT TO DO]

Please: (1) confirm you understand the current state and the specific
next task, (2) flag anything ambiguous before writing code, (3) do the
work, (4) give me a changelog entry in the format above for what you did.
```

---

## B. HANDBACK PROMPT — paste into Claude once quota resets

```
Quota reset — resuming. While you were unavailable I continued this
task with [ChatGPT / Gemini] under the same working agreement in
CLAUDE.md. Here's what changed:

[PASTE: the new CHANGELOG.md entries the other model produced]

[PASTE: the current state of any file(s) it modified]

[PASTE: the latest eval/harness.py output]

Please review this like you'd review a collaborator's work: check it
actually follows our baseline/advanced distinction, check the changelog
entries are honestly evidenced (not just claimed), and flag anything
you'd have done differently before we continue. Then let's proceed with:
[YOUR NEXT TASK]
```

---

## Why this works

- Files, not summaries, cross the handoff — so nothing gets lost in
  paraphrase between models.
- The same rules (baseline discipline, changelog format, no-autonomy-on-
  consequential-actions) travel with the prompt, so a different model
  produces compatible, not divergent, work.
- The handback step makes Claude *review* rather than blindly trust the
  other model's output — this catches drift before it compounds, and
  gives you an honest "kept or reverted" moment if something needs fixing.
- Every handoff is itself evidence for your submission: it shows real
  engineering judgment under a real constraint (limited free-tier access),
  which is exactly what the challenge says it's evaluating.
