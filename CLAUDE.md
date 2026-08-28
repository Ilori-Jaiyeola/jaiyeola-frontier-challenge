# Agent Instructions — micro1 Frontier Engineering Challenge

Single disclosed agent for this entry: **Claude, via the claude.ai chat
interface** (free plan — no Claude Code, no local terminal/repo access from
the agent). All code is authored in chat, copied into this repo by the
human, run and tested locally/on GitHub Actions by the human. This file is
the working agreement referenced at the top of every chat session — paste
it (or link the repo) at the start of a session so the agreement carries
over.

## Context

- Individual entry, micro1 Frontier Engineering Challenge, Aug 28–31 2026.
- Problem statement: `docs/problem.pdf` (added at kickoff — read it fully
  before writing any code).
- Every submission needs a **baseline** (`baseline/solution.py`) and an
  **advanced** solution (`advanced/solution.py`) that is a *meaningful*
  improvement, not cosmetic.
- Rule book requires: consequential actions gated behind a sandbox/simulation
  with human approval before execution; no real credentials or private data
  in the repo; every result claim must trace back to evidence in this repo.

## Tools disclosed

- **Agent:** Claude (claude.ai chat, free plan). No Claude Code, no other
  coding agent used.
- **Trajectory evidence:** the chat transcript itself (exported at
  submission time) plus the resulting git commit history.
- **Execution environment:** human copies chat-authored code into this
  local repo; tests run locally and via GitHub Actions CI
  (`.github/workflows/ci.yml`) — the agent does not execute code directly.

## Working agreement for this session

1. **Read `docs/problem.pdf` (once present) and the acceptance tests before
   writing code.** Summarize your understanding back before implementing —
   flag anything ambiguous rather than guessing silently.
2. **Build baseline first.** It should be the simplest correct approach —
   resist the urge to make it clever. It's the control group.
3. **Every meaningful decision goes in `CHANGELOG.md`** — trigger, change,
   evidence, result, kept-or-reverted. Don't wait until the end to
   reconstruct this; log it as you go, right after the evidence appears.
4. **Never fabricate a passing result.** If `eval/harness.py` shows a
   failure, say so and either fix it or log it as the known failure mode —
   don't paper over it.
5. **No secrets in the repo.** If a task needs an API key, read it from an
   environment variable and confirm `.env` is git-ignored.
6. **Any action that would affect a real system, send a real message, spend
   real money, or touch real user data**: stop and simulate it, or ask for
   explicit human confirmation first. Don't take these actions autonomously
   even if technically possible.
7. **Keep commits small and message-per-decision** so the git log itself is
   part of the trajectory evidence.
8. **Output full files or clearly-labeled diffs**, not partial fragments —
   the human is copying these by hand into the local repo, so ambiguity
   costs real time.
9. **If chat quota runs out mid-task**, use `docs/continuity_prompt.md` to
   hand off to another model and resume here once quota resets — see that
   file for the exact handoff/return prompts.

## Repo map

- `baseline/`, `advanced/` — the two solutions
- `eval/harness.py` — comparison runner (adapt `score_case()` to the real
  acceptance test once known)
- `eval/cases/` — test cases
- `trajectories/` — exported agent session logs (see trajectories/README.md)
- `CHANGELOG.md` — improvement log
- `REPRODUCTION.md` — exact run instructions for a judge
