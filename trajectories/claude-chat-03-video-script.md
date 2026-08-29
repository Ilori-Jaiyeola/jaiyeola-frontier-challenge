# Trajectory: Video Script & Recording Setup (Phase 3)

**Agent:** Claude (claude.ai chat interface, free plan)
**Human:** Jaiyeola
**Phase covers:** writing the full word-for-word solution video script
against real results, building and testing an on-camera demo script, and
giving concrete free-tool recording/editing instructions.

---

## Turn 1

**Human:** Asked to move to video production.

**Claude:** Built `scripts/record_demo.sh` -- a runnable script that walks
through baseline output, the standout case-16 (adversarial) evidence and
result, and the full 16-case comparison, with pauses between sections so
the human doesn't have to remember command sequences while on camera.
Tested it end-to-end in the sandbox (auto-answering the pause prompts) to
confirm it runs clean with no errors before handing it over -- this
mattered because a broken demo script discovered live during recording
would waste the human's limited remaining time.

Wrote the full script text in `docs/video_script.md`, matching the
existing storyboard's timing (0:00-0:45 problem+baseline, 0:45-3:00 one
realistic run, 3:00-3:45 comparison, 3:45-4:30 changelog highlights,
4:30-4:50 biggest win + one removed, 4:50-5:00 close) but now with actual
narration text grounded in the real numbers and the real case-16 story
from Phase 2, rather than placeholder prompts. Chose case-16 (the
adversarial case) as the centerpiece of the "one realistic execution"
section specifically because it's the most honest and interesting
walkthrough available -- it shows a real failure and real fix, not just a
lookup succeeding.

Added concrete, free-tool-only recording instructions for macOS
(QuickTime Player for screen+audio recording, iMovie for trim/export) 
since the human is working within real budget constraints, plus a
pre-recording checklist.

---

## Notes for the judge

The demo script (`scripts/record_demo.sh`) is itself part of the
reproducibility story -- anyone can run it to see exactly what the video
shows, independent of watching the video itself.
