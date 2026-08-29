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

One more thing before you finish this session: at the END of your work
(whether you complete the task, get stuck, or I tell you time's up),
produce TWO things so nothing about this session is lost — a handback
snapshot for resuming work, and a trajectory note for the submission
record. Use exactly this structure for both:

---
HANDBACK SNAPSHOT
Model: [your name/version]
What I did: [plain summary]
Files changed: [list, with the full final content of each — not a diff
  description, the actual content]
New CHANGELOG.md entries: [in the trigger/change/evidence/result/
  kept-or-reverted format above]
Eval result after my changes: [paste the actual harness output, or state
  clearly if you couldn't run it and why]
Open issue / where I stopped: [be specific — don't say "mostly done",
  say exactly what's untested or unfinished]
Anything I was unsure about: [flag it, don't silently guess]
---

---
TRAJECTORY NOTE
Model: [your name/version]
Session covers: [what phase/task this session was]
Instruction given: [the actual prompt/task you were given, in full or
  close to it — not paraphrased down to nothing]
What I did, turn by turn: [your reasoning and actions, in enough detail
  that someone unfamiliar with this session can follow how you got from
  the instruction to the result — this becomes trajectories/<your-model-
  name>-handoff-<phase>.md, a required disclosure item for this
  submission]
Feedback that changed my approach: [any point where an error, a test
  result, or a human correction changed what you did next — required,
  don't skip this even if it feels minor]
Human checkpoints: [any point you stopped and waited for approval before
  a consequential action, per the working agreement]
---

Give me both blocks every time you finish, even mid-task — the first
goes back to Claude (or forward to whichever model picks up next), the
second gets saved into this project's trajectories/ folder as required
disclosure evidence for the hackathon submission. Be as complete and
honest in the trajectory note as you'd want a work log to be if someone
else had to verify it later — this isn't a formality, it's literally
part of what gets judged.
```

---

## B. HANDBACK PROMPT — paste into Claude once quota resets

Take the "HANDBACK SNAPSHOT" block the other model gave you (Section A's
closing instruction) and paste it directly below this:

```
Quota reset — resuming. While you were unavailable I continued this
task with [ChatGPT / Gemini] under the same working agreement in
CLAUDE.md. Here's the HANDBACK SNAPSHOT it gave me:

[PASTE: the HANDBACK SNAPSHOT block]

Please review this like you'd review a collaborator's work: check it
actually follows our baseline/advanced distinction, check the changelog
entries are honestly evidenced (not just claimed), check the eval result
is real (not just claimed), and flag anything you'd have done
differently before we continue — especially anything listed under
"anything I was unsure about" or "open issue" above. Then let's proceed
with: [YOUR NEXT TASK]
```

Separately, save the TRAJECTORY NOTE block the other model gave you as
`trajectories/<model-name>-handoff-<phase>.md` — it doesn't need to go
through Claude, just file it directly per the naming convention in
`trajectories/README.md`.

---

## C. Chained handoffs (if a third model gets involved)

If the human needs to hand off again before returning to Claude — e.g.
Claude → ChatGPT → Gemini, because quota is still resetting — the next
model gets the SAME Section A prompt, but "current state" now includes
the previous model's HANDBACK SNAPSHOT instead of (or alongside)
CLAUDE.md/CHANGELOG.md. The snapshot format is designed to be handed to
literally any model, not just back to Claude, for exactly this reason.

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
- Requiring the trajectory note as part of the SAME handoff prompt (not a
  separate ask later) means it gets written while the work is fresh, by
  the model that actually did it — closer to a real log than a
  reconstruction from memory afterward.
