# Solution Video — Script & Recording Guide (≤5 min)

Real numbers, real script. Run `scripts/record_demo.sh` on camera for the
terminal parts — it prints clear section headers and pauses so you never
have to remember which command comes next.

## Full script (read roughly as written, adjust to your natural voice)

### 0:00–0:45 — Problem + baseline

> "A junior pentester runs a vulnerability scanner and gets back a pile
> of findings. The problem: scanners over-report. A lot of what they flag
> is a false positive, and figuring out which ones are real means
> manually checking version numbers and evidence for every single
> finding — slow, and easy to get wrong under time pressure.
>
> Here's the naive approach — just trust the scanner's own wording."

`[run: section 1 of scripts/record_demo.sh — baseline output]`

> "That's the baseline: keyword-matching the scanner's description text.
> No version check, no evidence check. It gets about half of these wrong."

### 0:45–3:00 — One realistic run, start to finish (the standout case)

> "Here's the case that actually broke my first version of the fix, so
> it's the most honest one to walk through. This finding says TLS 1.2 is
> negotiated by default — which sounds safe — but the same sentence
> describes a real, successful downgrade attack."

`[run: section 2 — show the case-16 evidence text and expected label]`

> "My first verification rule looked for exactly that phrase — 'negotiated
> by default' — as a signal the vulnerability wasn't really active. That
> rule was built to correctly handle a different, genuinely-safe case. But
> it fired here too, and got this one wrong, because it can't tell the
> difference between 'mentioned defensively' and 'mentioned right before
> describing a real exploit.'"

`[run: the advanced/solution.py output on case-16]`

> "After finding that failure, I added a narrower check — specific,
> explicit exploitation language that overrides the general rule. That's
> what you're seeing now: it correctly confirms this one."

### 3:00–3:45 — Final comparison

> "Here's the full picture — baseline against the improved solution,
> across all 16 test cases, including that adversarial one and a few
> other edge cases I added on purpose: an unparseable version, a
> knowledge-base miss, a duplicate finding."

`[run: section 3 — full harness comparison table]`

> "Baseline: 56%. Advanced: 100% — but not because I designed easy cases.
> I deliberately tried to break it partway through, and it broke. That's
> what the changelog documents honestly."

### 3:45–4:30 — Changelog highlights

> "Three moments actually mattered. First: giving the system a real
> vulnerability lookup instead of trusting the scanner's prose — that
> alone fixed most of the false positives. Second: splitting the logic by
> vulnerability type, because a weak-credentials finding needs different
> proof than a version-based one. Third — the one I already showed you —
> finding that my own verification rule could be fooled by wording, and
> having to add a narrower, more specific check on top of it."

### 4:30–4:50 — Biggest win + one thing removed

> "The single biggest win was the vulnerability lookup — that one change
> did more than anything else. The thing I tried and removed: I initially
> made every finding require direct proof of exploitation, no exceptions.
> That broke two legitimate cases where a version match alone was already
> good evidence. I had over-applied one rule to two different kinds of
> problems."

### 4:50–5:00 — Close

> "Main failure mode, honestly: this is still keyword matching under the
> hood. It closes the specific gap I found, but a more cleverly-worded
> adversarial case could probably still slip past it. That's the real
> edge of what this approach can do."

---

## How to actually record this (macOS, free tools only)

1. **Screen + audio recording — QuickTime Player** (already installed,
   free): File → New Screen Recording → click the dropdown arrow next to
   record → select your microphone → record.
2. **Terminal on screen, script visible on a second window/monitor if
   possible** — or just keep this file open in a text editor next to your
   terminal and glance over as you go. You don't need to memorize it.
3. **Run `bash scripts/record_demo.sh`** for every terminal segment — it
   handles the exact commands and pauses for you between sections so you
   can narrate without rushing.
4. **Trim/export — iMovie** (free, pre-installed on macOS): drag the
   QuickTime recording in, trim the front/back, export as .mp4 (File →
   Share → File, 1080p is plenty).
5. **Check the runtime** — aim for 4:30–5:00, not right at the 5:00 cap;
   a few seconds of buffer avoids any risk of disqualification for length.

## Before you hit record

- [ ] Run `scripts/record_demo.sh` once, off-camera, so you know what the
      output looks like and there are no surprises
- [ ] Close other apps/notifications (Do Not Disturb on)
- [ ] Increase terminal font size so scan findings/output are readable on
      a judge's screen, not just yours
- [ ] Have this script open for reference, but don't read it verbatim —
      natural pacing beats a perfect read
