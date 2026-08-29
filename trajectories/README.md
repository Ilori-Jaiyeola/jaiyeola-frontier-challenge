# Agent Trajectories

Single disclosed agent: Claude via the claude.ai chat interface. The
trajectory requirement here is satisfied by the exported chat transcript —
it already contains the instructions given, Claude's reasoning, any tool
calls (searches, file/code generation) and their results, the evidence that
shaped each next step, and every human checkpoint (your "proceed" / "wait,
change this" turns).

## How to capture

**Primary method — copy as you go (do this, don't wait for an export):**
claude.ai has no instant one-click "export this conversation" button. The
account-wide Settings → Privacy → Export Data option exports your *entire*
history, gets emailed as a link, and can take a while to process — too
slow to rely on mid-hackathon. Instead:

1. Periodically select and copy the conversation text (your prompts +
   Claude's responses, in order) into a local markdown file as you work —
   after each meaningful phase, not just at the very end.
2. Save it here as `trajectories/claude-chat-<phase>.md`, e.g.
   `claude-chat-baseline-build.md`, `claude-chat-advanced-iteration.md`.
3. If a quota handoff happened (see `docs/continuity_prompt.md`), the other
   model is instructed to generate its own `TRAJECTORY NOTE` block as part
   of the handoff prompt — save that directly as
   `trajectories/<other-model>-handoff-<phase>.md` (no manual reconstruction
   needed, it's already written in the right format), and note the handoff
   in the README's "Tools disclosed" section.

**Backup method — full account export:** Settings → Privacy → Export Data,
if you want a complete backup at the end. Don't depend on it as your only
copy — the processing delay makes it unsuitable as your live capture method.

## Before committing a transcript

- [ ] Scrub any API keys, tokens, or personal account details that
      appeared on screen
- [ ] Confirm it shows: the instruction given, Claude's plan/reasoning,
      the actual code or output produced, and at least one place where
      your feedback (a test failure, a correction) changed the next step
- [ ] Confirm any handoff-and-review moment (Section B of
      `continuity_prompt.md`) is included if it happened — that's strong
      evidence of engineering judgment, not something to trim out

## Naming convention

`claude-chat-<phase>.md` for the main agent; `<other-model>-handoff-<phase>.md`
for any quota-driven handoff sessions.
