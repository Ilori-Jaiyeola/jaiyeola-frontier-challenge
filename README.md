# Vulnerability Scan Triage Assistant — micro1 Agentic Workflows Hackathon 2026

> Author: Jaiyeola · Individual entry · Aug 28–31, 2026

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

**The meaningful improvement:** 10/10 (100%) classification accuracy vs.
the baseline's 5/10 (50%) on the same 10 synthetic cases — see Section 5.
This isn't cosmetic: the baseline's failures are exactly the real-world
failure mode (trusting scanner prose over actual version data), and the
advanced solution's fixes are exactly the corresponding independent checks
a careful human analyst would actually perform.

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
| Accuracy (10 known-labeled cases) | 50% (5/10) | 100% (10/10) | +50 points |

**The one challenging case (per the brief's request):** Case-05 — a TLS
finding where the scanner flags TLS 1.0 support (technically true, and
within the known-affected version range), but the evidence itself shows
TLS 1.2 is negotiated by default. The naive baseline confirms it outright
(dangerous — this would go to a client as a live finding when it may not
be practically exploitable). The advanced solution's evidence-contradiction
check downgrades it to "Needs Verification" — correctly flagging it for a
human to check whether the weak protocol can actually be forced, rather
than either false-confirming or blindly dismissing it. This is also the
case that broke an earlier version of the verification logic (see
Iteration 3 in the changelog) — it's genuinely the hardest case in the set.

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

The verification logic is rule-based, not learned — it only classifies
correctly for vulnerability *patterns* it has an entry for in
`vuln_db.json` and *evidence phrasings* it has a pattern for in
`_DIRECT_EVIDENCE_PATTERNS`/`_CONTRADICTING_EVIDENCE_PATTERNS`. A
genuinely novel vulnerability class, or evidence phrased in an
unanticipated way, falls through to "Needs Verification" (the safe
default) rather than being classified confidently — which is the right
failure direction (never silently over-confirms something novel), but it
means the system's real-world coverage is only as good as the knowledge
base and pattern lists behind it, and both would need active maintenance
against a real, growing vulnerability landscape.

## 10. Hot take

The single highest-leverage change here wasn't a clever agent trick — it
was giving the system one piece of *ground truth context* (a real affected
version range) instead of asking it to parse confidence from prose. Most
of the accuracy gap closed the moment the system stopped trusting the
scanner's own wording and started checking a fact against it. The lesson
for building reliable agents generally: before reaching for more
sophisticated reasoning or orchestration, ask whether the agent actually
has access to the ground truth it needs to be right — a lot of apparent
"reasoning failures" are really "missing context" failures wearing a
disguise.
