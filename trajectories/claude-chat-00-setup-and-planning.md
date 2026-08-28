# Trajectory: Setup & Planning (Phase 0)

**Agent:** Claude (claude.ai chat interface, free plan)
**Human:** Jaiyeola
**Phase covers:** initial challenge briefing → repo scaffold → agent-tooling
decisions → GitHub CI setup → trajectory-capture method. This is
pre-kickoff prep work (before the problem PDF was released), not the
actual solution build.

---

## Turn 1

**Human:** Shared the full micro1 Frontier Engineering Challenge brief
(overview, rules, prizes, eligibility, evaluation criteria, submission
package requirements, rule book) and stated intent to participate, asking
for help winning.

**Claude:** Identified this as a legitimate hackathon-prep task. Since the
problem PDF wasn't released yet (kickoff 15:00 UTC, Aug 28), proposed doing
everything problem-agnostic in advance: lock an agent stack, prep a repo
skeleton (README/changelog/reproduction templates), decide the
baseline-vs-advanced pattern in the abstract, set up a generic eval
harness, storyboard the required 5-minute video, and re-read rule-book
constraints (sandbox/human-approval gating, legal/ethical data use, no
credentials in the repo) so they're baked in from commit one. Asked
whether the human wanted help building the README/changelog template and
harness scaffold immediately.

---

## Turn 2

**Human:** Confirmed yes, and asked two additional things: (1) whether
Claude could be used *as* Claude Code directly, or whether Claude Code
needed separate installation with a prompt to feed it; (2) to prepare the
system/architecture for testing with another agent plus GitHub.

**Claude:** Clarified the distinction — this chat is not Claude Code;
Claude Code is a separate CLI tool requiring local install
(`npm install -g @anthropic-ai/claude-code`, Node 18+, a paid Pro/Max/Team/
Console account) that gets direct local file/git access, which this chat
does not have. Then built the actual scaffold in Claude's own sandbox:
`README.md`, `CHANGELOG.md`, `REPRODUCTION.md`, a generic
`eval/harness.py` (baseline-vs-advanced comparison runner with pass rate,
mean score, latency stats), stub `baseline/solution.py` and
`advanced/solution.py`, `CLAUDE.md` (agent working agreement),
`docs/kickoff_prompt.md` (paste-in prompt for once the PDF drops),
`trajectories/README.md` (capture instructions), `docs/video_script.md`
(5-minute storyboard matching the required structure), and `.gitignore`.
Initialized git, committed, packaged as a zip and a tar.gz (with git
history), and presented both for download.

---

## Turn 3

**Human:** Asked which other free agentic coding tools could be used,
with Claude guiding setup throughout.

**Claude:** Searched current (Aug 2026) comparisons of free agentic coding
tools. Presented three real options with trade-offs — Aider (free,
open-source, git-native CLI), Cline (free VS Code extension, Plan/Act
modes), Gemini CLI (free daily quota, different model family for
disclosure diversity) — and asked which one the human wanted, rather than
picking unilaterally.

---

## Turn 4

**Human:** Asked Claude to recommend one.

**Claude:** Recommended Aider specifically because its auto-commit-per-edit
behavior produces trajectory evidence natively (no separate capture step
needed) and it's model-agnostic, supporting genuine tool diversity in the
disclosure. Gave the install command and a sample model-pointing command
using a free API tier. Added `.aider.conf.yml` (auto-commits on, reads
`CLAUDE.md` for shared working agreement) and
`docs/aider_kickoff_prompt.md` to the repo, committed, repackaged, and
re-presented the download. Proposed a two-agent plan (Claude Code as
primary builder, Aider as secondary) pending kickoff.

---

## Turn 5

**Human:** Stated they only have Claude Code's free version.

**Claude:** Searched current Claude Code pricing/access requirements and
found there is no genuinely free tier — Pro ($20/mo), Max, Team, or
Console access is required to authenticate at all; a 30-day trial requires
a card; a 7-day guest pass exists only via an existing Max subscriber
sending one. Explained this plainly rather than assuming a workaround
existed, and asked which situation actually applied (trial with card
possible / need fully free tools only / has Console credits) via a
multiple-choice prompt.

---

## Turn 6

**Human:** Asked whether Claude could instead be given direct access to
the human's terminal/git account, and if not, offered to subscribe to Max
if a no-card path existed.

**Claude:** Searched to confirm no card-free Max signup path exists (guest
passes require an existing Max subscriber to send one; all self-serve
paths require payment info at checkout). Clarified plainly that Claude
(this chat) has no connection to the human's local machine, filesystem, or
GitHub account — an architectural boundary, not a settings toggle.
Proposed the actual workable path: Claude via chat as the sole agent
(sandbox-based file authoring, human copies into local repo and runs
tests/CI), optionally paired with a genuinely free local tool. Asked
whether a second agent was still wanted given this constraint.

---

## Turn 7

**Human:** Chose option 1 (Claude via chat only) and asked whether a
second agent was still necessary.

**Claude:** Confirmed the rule book only requires disclosing whichever
tools are actually used — one agent, well-documented, is a fully valid
entry. Named the real constraints of the chat-only setup honestly (free
plan's ~5-hour usage reset windows; no direct local/GitHub write access;
no live terminal observation) rather than glossing over them, and proposed
a concrete workflow: Claude authors files → human copies into local repo →
human runs tests/CI and pastes results back → decisions get logged into
`CHANGELOG.md` together → the chat transcript itself becomes the
trajectory evidence.

---

## Turn 8

**Human:** Approved, and asked for three things: (1) update the repo for
the single-agent-via-chat workflow, (2) add a way to run tests
automatically on GitHub the moment code is pushed, (3) prepare a "clever"
continuation-prompt system so work could hand off to ChatGPT/Gemini if
Claude's quota ran out, then hand back to Claude afterward. Also made a
lighthearted aside about a reward for winning.

**Claude:** Acknowledged the aside briefly without dwelling on it, then
delivered all three technical asks:
- Rewrote `CLAUDE.md` and `README.md`'s "Tools disclosed" section to name
  Claude-via-chat as the sole agent, remove Claude Code framing, and
  describe the copy-in/human-executes workflow explicitly.
- Added `.github/workflows/ci.yml` — triggers on every push/PR, sets up
  Python, installs `requirements.txt`, runs `eval/harness.py`, uploads the
  JSON result as a downloadable artifact, and supports manual
  `workflow_dispatch` re-runs. Added a placeholder `requirements.txt` as
  its dependency source of truth.
- Wrote `docs/continuity_prompt.md`: a handoff prompt (carries the actual
  working-agreement rules — baseline discipline, changelog format,
  no-autonomous-consequential-actions — plus the real current files, not
  just a vague summary) for pasting into ChatGPT/Gemini, and a handback
  prompt that has Claude *review* the other model's work on return rather
  than blindly trust it.
- Removed the now-unnecessary Aider config files to avoid mixed signals
  since the human had settled on single-agent.
- Rewrote `docs/kickoff_prompt.md` for the chat-based workflow (replacing
  the Claude-Code-specific version).
- Committed each logical change separately, repackaged, re-presented.

---

## Turn 9

**Human:** Asked where to test chat export, and whether the scaffold
zip/tar.gz files already presented *were* the chat-export.

**Claude:** Searched current claude.ai data-export mechanics. Clarified
the scaffold files are project code, not a conversation transcript —
distinct things. Found there's no instant single-conversation export
button; the real feature (Settings → Privacy → Export Data) exports the
entire account's history and is processed/emailed, too slow for live
hackathon capture. Proposed "copy-as-you-go" as the practical primary
method instead, and asked permission to document that in
`trajectories/README.md`.

---

## Turn 10

**Human:** Confirmed yes, asked when to start copying, exactly what to
copy, and asked to proceed with GitHub repo setup — name and initial
upload/test.

**Claude:** Ran the eval harness locally in the sandbox first, to preview
what the first real GitHub Actions run would show (confirmed: clean 0.0
pass rate from caught `NotImplementedError`s, not a crash — the correct
pre-kickoff state). Rewrote `trajectories/README.md` to make copy-as-you-go
the primary capture method (with the account export named as a slower
backup only), with concrete phase-boundary triggers ("if it earned a
CHANGELOG entry, it earns its own trajectory file"). Recommended starting
the capture immediately, with this very setup conversation as
`claude-chat-00-setup-and-planning.md`. Suggested a repo name
(`micro1-frontier-challenge-2026`) and gave both `gh` CLI and manual
GitHub web + git push instructions, plus the exact CI verification steps
(check the Actions tab, expect green with 0.0 pass rate, check the
`eval-results` artifact).

---

## Turn 11

**Human:** Pasted the GitHub Actions "get started" screen, showing GitHub
had not detected any workflow file, and asked which template to pick.

**Claude:** Identified this meant no workflow file had reached the repo —
told the human to pick none of the suggested templates ("Skip this and set
up a workflow yourself"), and to check on GitHub's web UI whether
`.github/workflows/ci.yml` was present in the file listing, giving
separate remediation commands depending on whether it was missing or just
needed a trigger nudge.

---

## Turn 12

**Human:** Reported the likely cause: macOS Finder hides dotfiles, so
`.github`/`.gitignore` were probably left behind during manual extraction.

**Claude:** Confirmed this was almost certainly it. Gave the Finder
hidden-files toggle (`Cmd+Shift+.`) as a quick fix, and — as a more
reliable alternative — gave exact Terminal commands (`tar -xzf ...`,
`git ls-files`) to extract and verify without relying on Finder's display
at all. Ran `git ls-files` in Claude's own sandbox copy to give the human
a definitive expected-file checklist to compare against.

---

## Turn 13

**Human:** Said the `.git` folder specifically failed to upload to GitHub.

**Claude:** Explained that `.git` is never manually "uploaded" via a
website — it's git's own internal database, populated by running `git
push` from a real git client, not drag-and-drop. Gave the full correct
sequence: extract via Terminal, create an empty GitHub repo (no
auto-generated README), `git remote add origin ...`, `git push -u origin
main`, noting this single push carries every tracked file, dotfiles
included, in one operation. Asked for the output of `git status` after
extraction and the result of the push to diagnose further if needed.

---

## Turn 14

**Human:** Said they weren't using Terminal at all, and reported that
everything except `.git` uploaded — attaching the actual GitHub Actions
run output showing the workflow executed successfully with both baseline
and advanced returning a clean 0.0 pass rate from caught
`NotImplementedError`s, plus a successful `eval-results` artifact upload
and an informational Node.js version deprecation notice.

**Claude:** Read the pasted Actions output and confirmed this was in fact
full success, not a failure needing debugging: the workflow triggered
correctly, both stubs failed in the expected/correct controlled way (not
a crash), and the artifact was captured. Clarified the apparent "`.git`
didn't upload" concern was a misunderstanding of the UI — `.git` is never
shown as a browsable folder on GitHub regardless of tool used, while
`.github` (the actually-relevant visible folder holding the workflow) had
clearly succeeded, which the CI run itself proved. Summarized the current
state as fully ready (repo live, CI running automatically, correct
pre-kickoff stub behavior, trajectory/changelog conventions in place) and
asked how much time remained before kickoff.

---

## Turn 15

**Human:** Reported 9 hours to kickoff, and asked for this trajectory file
to be generated/highlighted for direct copy-paste into the repo's
`trajectories/` folder.

**Claude:** Produced this transcript.

---

## Notes for the judge

This phase is entirely pre-kickoff preparation: no problem-specific code
was written, since the problem PDF had not yet been released. What it
demonstrates is the working agreement, tooling constraints, and
engineering-judgment calls (free-tier limitations, single-agent scoping,
CI setup, trajectory-capture method) that shaped everything built
afterward. Real solution work begins in the next trajectory file, once
`docs/problem.pdf` is read.
