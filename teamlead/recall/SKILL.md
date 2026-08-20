---
name: recall
description: "Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work."
---

# Recall

**Before you start or resume work, you rebuild the user's recent working context and hand back a tight capsule of where things stand now and what to do next.** Use for "recall my work on X", "catch me up", "what have I been working on", or "where did I leave off".

Keep it tight and on-topic. Read only what the in-scope threads need, then stop. The heavy reading fans out to parallel subagents. The main thread keeps only their findings and the final brief.

Context lives in two records. Chat history holds what the user and agents did and decided. The shared record includes
source control, issues, project memory, docs, production reports, and current repository state. A long-lived feature
usually needs both; do not reconstruct it from transcripts alone.

Common local transcript roots include `~/.claude/projects/`, `~/.pi/agent/sessions/`, and `~/.codex/sessions/`.
Formats differ. Search only the workspace, topic, harnesses, and time range the user approved. Never sweep unrelated
projects merely because the directory is readable.

1. Classify, then route. One specific prior chat to resume is `session-pickup`. Turning repeated habits into a skill
   is `capture-workflow`. If the user already supplied a full state capsule, use it and skip transcript mining.
2. Lock the scope before searching. Pin the window ("recent" is a real range, default the last 7 days), the topic if named, and the workspace (default the active one; never read another project's transcripts without being asked). State the scope back. Never quietly turn "all" into "recent N".
3. Fan out over large approved corpora with cheap read-only agents, one time slice or harness per agent. Order candidates
   by real modification time, grep the topic first, then read only matching chats and relevant regions. Skip the current
   chat plus obvious subagent, eval, and test noise. Each result reports topic, goal, decisions, open threads, user
   corrections, and artifacts with a transcript identifier. Keep raw transcript text out of the lead context.
4. Sweep the shared record when the topic names a feature, file, subsystem, or bug. Ask what the current state is,
   what was tried and reverted, and what users still report. Run independent sources in parallel when available. A
   missing source is a finding; do not invent access. Skip this for pure activity recall with no named target.
5. Verify against live state. A transcript or a stale ticket is history, not current truth, so take the PRs, branches, and tickets that the mining and the sweep surfaced and check them with `git` and `gh`. When the answer hinges on what an agent actually did (the tools it ran, files it read, errors it hit), read the full transcript, not just a trimmed local copy.
6. Write the brief to the contract below. Group by thread. Stay on the named topic.

## Output contract

Lead with the capsule, then the thread status, then the problems, then the next move. Deeper detail goes below or gets cut.

- **Capsule.** At most 5 bullets. What this work is and where it stands overall.
- **Threads.** One line each, prefixed with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. A thread with no tag is not done yet, so tag it.
- **Problems.** At most 5, the recurring ones. Include the symptoms users keep reporting and any fix that shipped and was reverted, so the next attempt starts where the last one failed.
- **Next move.** The single most useful next action, concrete.

An adjacent feature or ticket stays out unless it blocks this one. When the capsule outgrows a screen, cut detail
before threads. Cite transcript findings by identifier and shared findings by source. Sanitize private context before
any public output.

**Reply:** the brief, to the contract above.
