# Kickoff — paste into this chat once the problem PDF drops

1. Upload `docs/problem.pdf` (or paste its full text) into the chat.
2. Paste this as your message alongside it:

---

Read the attached problem PDF in full, and here's our working agreement
(CLAUDE.md) for this repo: [paste current CLAUDE.md content, or just say
"same as before" if it's already in this conversation].

Before writing any code:
1. Summarize the problem in your own words: who the user is, what they're
   trying to do, what "correct" means here, and what the acceptance tests
   will likely check.
2. List the constraints (allowed languages/frameworks, dependency limits,
   any prescribed starter repo or test environment) exactly as stated.
3. Flag anything genuinely ambiguous in the spec rather than assuming —
   ask me before proceeding on those points only.
4. Propose the baseline approach (deliberately simple/naive) and a
   candidate direction for the advanced approach, with reasoning for why
   the advanced one is a meaningful (not cosmetic) improvement.

Wait for my go-ahead before writing `baseline/solution.py`.

---

3. Review the plan, correct anything off-base, say "proceed."
4. Work in short loops: Claude writes a full file or clear diff → you copy
   it into the local repo → you run `eval/harness.py` (or push and let
   GitHub Actions run it) → paste the output back into chat → decide next
   step together → log it in `CHANGELOG.md` before moving on.
5. If quota runs out mid-loop: use `docs/continuity_prompt.md` to hand off
   to ChatGPT/Gemini, then hand back to Claude once quota resets.
