# [Project Name] — micro1 Frontier Engineering Challenge 2026

> Author: Jaiyeola · Individual entry · Aug 28–31, 2026

## 1. Who is this for, and what's their bottleneck?

<!--
Fill in once the problem PDF drops. Answer three things concretely:
- Who is the intended user? (a role, not "developers" — e.g. "a solo boutique
  tailor managing 40 client orders")
- What do they currently do, and where does it break down / cost them time?
- Why does solving this matter — what's the cost of the status quo?
-->

## 2. Approach at a glance

| | Baseline | Advanced |
|---|---|---|
| What it does | | |
| Key limitation / capability | | |
| Where it lives | `baseline/` | `advanced/` |

One paragraph: what's the *meaningful* improvement (capability, reliability,
efficiency, coverage, or engineering quality) — not a cosmetic variation.

## 3. Architecture

<!-- Diagram or short bullet list: components, data flow, where agents sit,
where human approval gates sit for any consequential action. -->

## 4. What existed before this competition vs. what I built

<!-- Rule book requires this distinction explicitly. Be specific about
libraries/templates/prior code vs. net-new work done Aug 28–31. -->

## 5. Improvement Changelog

See [`CHANGELOG.md`](./CHANGELOG.md) — every meaningful iteration, the
evidence that drove it, and the outcome.

## 6. Reproduction

See [`REPRODUCTION.md`](./REPRODUCTION.md) for exact setup + run commands.

## 7. Agent trajectories

See [`trajectories/`](./trajectories/) — one representative trajectory per
agent used, from instruction through tool calls through final result,
including retries and any human checkpoints.

## 8. Tools disclosed

- Coding agent: Claude, via the claude.ai chat interface (free plan). Not
  Claude Code — no local terminal/repo access by the agent.
- Model: <!-- e.g. Claude Sonnet 5 — check chat's model selector -->
- Execution: code authored in chat, copied into this repo by hand, tests
  run locally and via GitHub Actions CI (see `.github/workflows/ci.yml`).
- If a quota-driven handoff to another model occurred mid-project (see
  `docs/continuity_prompt.md`), disclose it here: which model, which
  changelog entries it produced, and confirm scope stayed within this
  working agreement.
- Any external services / APIs: <!-- -->

## 9. Main failure mode

<!-- The one thing most likely to break this, honestly stated. -->

## 10. Hot take

<!-- One paragraph, your genuine opinion formed from doing this work. -->
