# Vulnerability Scan Triage Assistant — micro1 Agentic Workflows Hackathon 2026

> Author: Jaiyeola Ilori · Individual entry · Aug 28–31, 2026

## 1. Who is this for, and what's their bottleneck?

**User:** A junior penetration tester / security analyst who just ran a
vulnerability scanner (Nessus/OpenVAS/Nmap-style) against a client network
and now has a stack of raw findings to turn into a client report.

**Bottleneck:** Scanners over-report. Findings are generated from
signatures and banners, not real verification — a huge share are false
positives (an old-looking banner on a service that's actually patched) or
under-verified true positives (config issues a scanner can detect the
*possibility* of, but not confirm). Manually re-checking every finding
against the actual affected version range and the strength of the
evidence is slow, and skipping it risks either reporting an embarrassing
false positive to a client, or rubber-stamping something that was never
actually proven.

**Why it matters:** A junior analyst's time is the scarce resource here,
and a wrong call in either direction costs credibility — either with the
client (false positive) or with the actual security posture (missed real
issue treated as noise).

## 2. Approach at a glance

| | Baseline | Advanced |
|---|---|---|
| What it does | Keyword-matches the scanner's own description text ("is vulnerable" → Confirmed, "may be" → Needs Verification, else defaults to trusting the scanner) | Looks up each finding's actual affected version range in a vulnerability knowledge base, applies different verification logic for version-dependent vs. config-class issues, checks whether evidence text contradicts exploitability, and remembers findings already triaged this session |
| Key limitation / capability | Never checks version against a real affected range; trusts scanner wording at face value; no memory | Independently verifies version range + evidence quality before confirming anything; distinguishes vulnerability classes; deduplicates repeat findings |
| Where it lives | `baseline/solution.py` | `advanced/solution.py` |

**The meaningful improvement:** 16/16 (100%) classification accuracy vs.
the baseline's 9/16 (56.25%) on 16 synthetic cases — see Section 5. The
eval set was deliberately expanded beyond an initial 10 cases specifically
to include a knowledge-base miss, an unparseable version, a genuine
duplicate (to actually exercise the memory feature), a boundary version,
and one adversarial case designed to try to break the verification
heuristic. That last one succeeded at breaking it on the first pass — see
Section 5 for what that revealed and how it was (partially) addressed.

## 3. Architecture

```
raw finding (host, port, service, version, plugin_name, evidence)
        │
        ▼
┌─────────────────────────────────────────────┐
│ ADVANCED PIPELINE (advanced/solution.py)     │
│                                               │
│  1. MEMORY: seen this host+plugin before     │
│     this session? → reuse prior result        │
│                                               │
│  2. TOOL/CONTEXT: look up plugin_name in       │
│     local vuln knowledge base                  │
│     (eval/knowledge_base/vuln_db.json)         │
│     → affected version range, vuln class,      │
│       known false-positive patterns             │
│                                               │
│  3. VERIFICATION (branches by vuln class):     │
│     • config-class (version-independent):      │
│       requires DIRECT exploitation evidence     │
│       to confirm (a real login, a real          │
│       unauthenticated command executing)        │
│     • version-dependent: confirm on version     │
│       match UNLESS evidence text contradicts     │
│       exploitability (e.g. a secure protocol     │
│       negotiated by default)                    │
│                                               │
│  4. OUTPUT: label + plain-English reason        │
│     tied to the specific evidence used          │
└─────────────────────────────────────────────┘
        │
        ▼
{label: Confirmed | Likely False Positive | Needs Verification, reason}
```

No consequential/external action is taken by this pipeline (it's a
read-only classification and write-up step) — nothing needs a
sandbox/simulation gate under the rule book. The intended real-world
deployment is: agent triages → human analyst reviews the
"Needs Verification" and "Confirmed" bucket before anything goes in an
actual client report — the human stays the final approver, per the rule
book's "qualified human reviewer" requirement.

## 4. What existed before this competition vs. what I built

**Existed before (general knowledge / prior scaffolding):** The repo
scaffold (README/CHANGELOG/reproduction templates, generic eval harness
shape, GitHub Actions CI structure, continuity-prompt system) was built in
the pre-kickoff prep window (Aug 28, before 15:00 UTC), before the problem
statement was known — it's problem-agnostic tooling, not project-specific
work.

**Built after kickoff (this project specifically):** The actual problem
choice, the synthetic vulnerability knowledge base
(`eval/knowledge_base/vuln_db.json`), the 10 synthetic test cases with
known-correct labels (`eval/cases/cases.json`), the naive baseline
(`baseline/solution.py`), the agentic advanced solution
(`advanced/solution.py`), and every entry in `CHANGELOG.md` — all written
after reading this problem PDF.

## 5. Improvement Changelog

See [`CHANGELOG.md`](./CHANGELOG.md) for the full iteration-by-iteration
story, including one iteration that was tried and reverted.

**Headline result:**

| Metric | Baseline | Advanced | Change |
|---|---|---|---|
| Accuracy (16 known-labeled cases) | 56.25% (9/16) | 100% (16/16) | +43.75 points |
| Cases requiring manual follow-up ("Needs Verification") | — (baseline doesn't distinguish this reliably) | 3/16 correctly flagged for human review, 0 silently wrong | Advanced surfaces genuine ambiguity instead of guessing |
| Cost per task | $0 | $0 | No API calls in either — local knowledge base only |

**The one challenging case (per the brief's request):** Case-16 — designed
adversarially, after the fact, specifically to try to break the
verification logic. A TLS finding describes "TLSv1.2 negotiated by
default... but a forced downgrade attack to TLSv1.0 succeeded." The
Iteration 4 heuristic (added to correctly handle case-05, a similar-looking
TLS finding that really was a false alarm) fires on "negotiated by
default" and incorrectly downgrades this to "Needs Verification" — even
though this one describes a genuine, demonstrated exploit. The fix
(Iteration 6) added a narrower override for explicit exploitation language
("downgrade attack succeeded," etc.) checked before the general
contradiction pattern. **This closes the specific gap case-16 exposed, but
it is still keyword matching** — a differently-worded adversarial case
could plausibly slip past both pattern lists. This is the real, honest
edge of what this approach can do; see Section 9.

## 6. Reproduction

See [`REPRODUCTION.md`](./REPRODUCTION.md) for exact setup + run commands.
No API keys or network access required — the knowledge base is local and
synthetic.

## 7. Agent trajectories

See [`trajectories/`](./trajectories/) — the setup/planning phase is
already captured in `claude-chat-00-setup-and-planning.md`; this build
phase is captured in `claude-chat-01-triage-solution-build.md`.

## 8. Tools disclosed

- Coding agent: Claude, via the claude.ai chat interface (free plan). Not
  Claude Code — no local terminal/repo access by the agent; all code was
  authored in chat and copied into this repo by hand.
- Model: Claude Sonnet 5 (per chat's model selector at time of writing).
- Execution: code authored in chat, tested by Claude in its own sandbox
  during development (see trajectory), then copied into this repo by the
  human; tests also run via GitHub Actions CI
  (`.github/workflows/ci.yml`).
- No quota-driven handoff to another model occurred during this phase (see
  `docs/continuity_prompt.md` for the process if one becomes necessary).
- External services / APIs: none. The vulnerability knowledge base is a
  local, synthetic, bundled JSON file — no live API, no key, no network
  dependency, by design (maximizes reproducibility per ground rule 10).

## 9. Main failure mode

The verification logic is rule-based keyword/pattern matching, not
semantic understanding — and this isn't hypothetical, it's demonstrated:
case-16 was built specifically to attack the Iteration 4 heuristic, and it
worked on the first attempt (see `CHANGELOG.md`, Iteration 6). The
override added to fix it is itself just another, narrower pattern list —
it closes that specific gap but doesn't change the underlying limitation.
A sufficiently different adversarial phrasing could plausibly defeat both
pattern lists at once. More generally: the system only classifies
correctly for vulnerability *patterns* present in `vuln_db.json` and
evidence *phrasings* present in the pattern lists in `advanced/solution.py`
— coverage is bounded by both, and both would need active, ongoing
maintenance against a real, evolving vulnerability and evidence-wording
landscape. The safe default (falling through to "Needs Verification"
rather than confidently guessing) limits the damage of this limitation,
but doesn't eliminate it.

## 10. Hot take

Two lessons, and the second one is the sharper one. First: the single
highest-leverage change here wasn't a clever agent trick — it was giving
the system one piece of ground-truth context (a real affected version
range) instead of asking it to parse confidence from prose. Most of the
initial accuracy gap closed the moment the system stopped trusting the
scanner's own wording and started checking a fact against it.

Second, and more important: a 100% score on a self-designed eval set is a
yellow flag, not a green one. This project hit 100% on 10 hand-built
cases, and the honest move was to then try to break it — which took one
deliberately adversarial case to succeed. The lesson for building reliable
agents generally isn't "add more rules until nothing fails" — it's that
your own eval set is part of what you're building, and if you only ever
design cases your system already handles, your measured improvement
number is measuring your own blind spots back at you. Red-teaming your
own eval, even briefly, produces more trustworthy evidence than a bigger
green checkmark.
